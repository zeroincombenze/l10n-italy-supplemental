# -*- coding: utf-8 -*-
#    Copyright (C) 2017-2018 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
#
import logging
from datetime import date

import odoo.release as release
from odoo import api, fields, models
from odoo.exceptions import UserError, Warning
from odoo.tools.translate import _

from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)
try:
    import codicefiscale
except ImportError as err:
    _logger.debug(err)

# TODO: Use module for classification
EU_COUNTRIES = [
    "AT",
    "BE",
    "BG",
    "CY",
    "HR",
    "DK",
    "EE",
    "FI",
    "FR",
    "DE",
    "GR",
    "HU",
    "IE",
    "IT",
    "LV",
    "LT",
    "LU",
    "MT",
    "NL",
    "PL",
    "PT",
    # 'GB',
    "CZ",
    "RO",
    "SK",
    "SI",
    "ES",
    "SE",
]


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    communication_type = fields.Selection(
        [
            ("XX19", "Esterometro 2019"),
            ("2018", "Spesometro 2018"),
            ("2019", "Spesometro 2019"),
            ("NO", "Escluso"),
        ],
        "Tipo comunicazione",
        help=u"Tipo di comunicazione a cui è assoggettata la fattura\n",
    )

    @api.onchange("partner_id", "date")
    def onchange_set_einvoice_commtype(self):
        if not self.partner_id or not self.date:
            return
        year = max(int(self.date[0:4]), 2017)
        iso = self.partner_id.vat[0:2] if self.partner_id.vat else False
        if (
            hasattr(self, "fatturapa_attachment_out_id")
            and self.fatturapa_attachment_out_id
        ) or (
            hasattr(self, "fatturapa_attachment_in_id")
            and self.fatturapa_attachment_in_id
        ):
            exclude_invoice = True
        elif self.journal_id:
            exclude_invoice = (
                self.journal_id.einvoice
                or self.journal_id.rev_charge
                or self.journal_id.proforma
                or self.journal_id.anom_sale_receipts
            )
        else:
            exclude_invoice = False
        if not iso and self.partner_id.country_id:
            iso = self.partner_id.country_id.code
        if exclude_invoice:
            communication_type = "NO"
        elif iso in EU_COUNTRIES and year < 2019:
            communication_type = "%d" % year
        elif iso == "IT" and year < 2019:
            communication_type = "%d" % year
        elif iso != "IT" and year >= 2019:
            communication_type = "XX19"
        else:
            communication_type = "NO"
        self.communication_type = communication_type

    @api.multi
    @api.depends("partner_id", "date")
    def set_einvoice_commtype(self):
        for invoice in self:
            invoice.onchange_set_einvoice_commtype()
        return True


class AccountVatCommunication(models.Model):
    def _get_error(self, error, context):
        if context.get("no_except", True):
            return error
        else:
            raise UserError(error)
        return False

    def _get_eu_res_country_group(self):
        eu_group = self.env.ref("base.europe", raise_if_not_found=False)
        if not eu_group:
            raise Warning(
                _(
                    "The Europe country group cannot be found. "
                    "Please update the base module."
                )
            )
        return eu_group

    @api.model
    def _get_default_soggetto_codice_fiscale(self):
        if self.company_id.vat:
            return self.company_id.vat[2:]
        return False

    _name = "account.vat.communication"

    name = fields.Char("Descrizione")
    type = fields.Selection(
        [
            ("XX19", "Esterometro"),
            ("2019", "Spesometro 2019"),
            ("2018", "Spesometro 2018"),
            ("2017", "Spesometro 2017"),
        ],
        "Tipo",
        required=True,
        help="Tipo di comunicazione\n",
    )
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.user.company_id
    )
    soggetto_codice_fiscale = fields.Char(
        "Codice fiscale contribuente",
        size=16,
        required=True,
        default=_get_default_soggetto_codice_fiscale,
        help="CF del soggetto a cui riferiscono i dati " "della liquidazione.",
    )
    codice_carica = fields.Many2one(
        "italy.ade.codice.carica",
        "Codice carica",
        help="Codice carica responsabile trasmissione",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "Open"),
            ("confirmed", "Confirmed"),
        ],
        "State",
        readonly=True,
        default="draft",
    )
    period_ids = fields.One2many("date.range", "vat_commitment_id", "Periods")
    account_vat_communication_dte_line_ids = fields.One2many(
        "account.vat.communication.dte.line",
        "commitment_id",
        "Sale invoices",
        help="Sale invoices to export in VAT communication",
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
            "confirmed": [("readonly", True)],
        },
    )
    account_vat_communication_dtr_line_ids = fields.One2many(
        "account.vat.communication.dtr.line",
        "commitment_id",
        "Purchase invoices",
        help="Purchase invoices to export in VAT communication",
        states={
            "draft": [("readonly", False)],
            "open": [("readonly", False)],
            "confirmed": [("readonly", True)],
        },
    )
    attachment_ids = fields.One2many(
        "ir.attachment",
        "res_id",
        "Attachments",
    )
    dte_amount_total = fields.Float(
        "Total sales",
        help="Total amount of sale invoices in Communication",
        digits=dp.get_precision("Account"),
    )
    dte_amount_taxable = fields.Float(
        "Total taxable sales",
        help="Total taxables of sale invoices in Communication",
        digits=dp.get_precision("Account"),
    )
    dte_amount_tax = fields.Float(
        "Total tax sales",
        help="Total taxes of sale invoices in Communication",
        digits=dp.get_precision("Account"),
    )
    dte_amount_discarded = fields.Float(
        "Total discarded sales",
        help="Total amount discarded from sale invoices",
        digits=dp.get_precision("Account"),
    )
    dtr_amount_total = fields.Float(
        "Total purchases",
        help="Total amount of purchase invoices in Communication",
        digits=dp.get_precision("Account"),
    )
    dtr_amount_taxable = fields.Float(
        "Total taxable purchases",
        help="Total taxables of purchase invoices in Communication",
        digits=dp.get_precision("Account"),
    )
    dtr_amount_tax = fields.Float(
        "Total tax purchases",
        help="Total taxes of purchase invoices in Communication",
        digits=dp.get_precision("Account"),
    )
    dtr_amount_discarded = fields.Float(
        "Total discarded purchases",
        help="Total amount discarded from purchase invoices",
        digits=dp.get_precision("Account"),
    )

    @api.model
    def create(self, vals):
        res = super(AccountVatCommunication, self).create(vals)
        if "company_id" in vals:
            sequence_ids = self.search_sequence(vals["company_id"])
            if not sequence_ids:
                self.create_sequence(vals["company_id"])
        return res

    @api.model
    def search_sequence(self, company_id):
        return self.env["ir.sequence"].search(
            [("name", "=", "VAT communication"), ("company_id", "=", company_id)]
        )

    @api.model
    def create_sequence(self, company_id):
        """Create new no_gap entry sequence for progressivo_telematico"""

        # Company sent own communication, so set next number as the nth quarter
        next_number = (
            int((date.today().toordinal() - date(2017, 7, 1).toordinal()) / 90) + 1
        )
        sequence_model = self.env["ir.sequence"]
        vals = {
            "name": "VAT communication",
            "implementation": "no_gap",
            "company_id": company_id,
            "prefix": "",
            "number_increment": 1,
            "number_next": next_number,
            "number_next_actual": next_number,
        }
        return [sequence_model.create(vals)]

    @api.model
    def set_progressivo_telematico(self, communication):
        sequence_model = self.env["ir.sequence"]
        company_id = communication.company_id.id
        sequence_ids = self.search_sequence(company_id)
        if not sequence_ids:
            sequence_ids = self.create_sequence(company_id)
        if len(sequence_ids) != 1:
            raise UserError(_("VAT communication sequence not set!"))
        number = int(
            sequence_model.search([("id", "=", sequence_ids.ids[0])]).next_by_id()
        )
        return number

    @api.multi
    def test_open(self):
        return True

    @api.multi
    def communication_draft(self):
        self.write({"state": "draft"})

    @api.multi
    def communication_open(self):
        self.write({"state": "open"})

    def get_country_code(self, partner):
        if release.major_version == "6.1":
            address_id = self.env["res.partner"].address_get([partner.id])["default"]
            address = self.env["res.partner.address"].browse(address_id)
        else:
            address = partner
        code = partner.vat and partner.vat[0:2].upper()
        return code or address.country_id and address.country_id.code

    def load_invoices(
        self,
        commitment,
        commitment_line_model,
        dte_dtr_id,
        where,
        comm_lines,
        context=None,
    ):
        """Read all in/out invoices and return amount and fiscal parts"""
        context = context or {}
        invoice_model = self.env["account.invoice"]
        account_tax_model = self.env["account.invoice.tax"]
        sum_amounts = {}
        for f in ("total", "taxable", "tax", "discarded"):
            sum_amounts[f] = 0.0
        invoices = invoice_model.search(where)
        for invoice in invoices:
            inv_line = {}
            invoice_id = invoice.id
            for invoice_tax in invoice.tax_line_ids:
                xml_Error2 = ""
                tax_kind = False
                tax_payability = "I"
                tax_rate = 0.0
                tax_nodet_rate = 0.0
                tax_type = ""
                if invoice_tax.tax_id:
                    taxcode_base_id = invoice_tax.tax_id.id
                    taxcode_vat_id = False
                    where = [("tax_id", "=", taxcode_base_id)]
                else:
                    taxcode_base_id = invoice_tax.base_code_id.id
                    taxcode_vat_id = invoice_tax.tax_id.id
                    where = [("base_code_id", "=", taxcode_base_id)]
                # for tax in invoice_tax.tax_code_id.tax_ids:
                r = account_tax_model.search(where)
                for tax in r:
                    if tax:
                        if tax.tax_id.amount > tax_rate:
                            tax_rate = tax.tax_id.amount / 100
                        if tax.tax_id.kind_id:
                            tax_kind = tax.tax_id.kind_id.code
                        if tax_payability:
                            tax_payability = tax.tax_id.payability
                        if tax.tax_id.type_tax_use:
                            tax_type = tax.tax_id.type_tax_use
                    else:
                        if release.major_version == "6.1":
                            tax_rate = 0
                            for child in account_tax_model.browse(
                                tax.parent_id.id
                            ).child_ids:
                                if child.type == "percent":
                                    tax_rate += child.amount
                            tax_nodet_rate = 1 - (tax.amount / tax_rate)
                        else:
                            if tax.type == "percent" and tax.amount > tax_nodet_rate:
                                tax_nodet_rate = tax.amount
                            tax = account_tax_model.browse(tax.parent_id.id)
                            taxcode_base_id = invoice_tax.tax_id.id
                            if tax.amount > tax_rate:
                                tax_rate = tax.amount
                if tax_type in ("sale", "purchase"):
                    if tax_rate == 0.0 and (
                        not tax_kind
                        or (dte_dtr_id == "DTR" and tax_kind.startswith("N6"))
                    ):
                        xml_Error2 += self._get_error(
                            _("00400 - Missed/wrong tax nature in %s")
                            % (invoice_tax.name),
                            context,
                        )
                    elif (
                        tax_rate
                        and tax_kind
                        and (dte_dtr_id == "DTE" or not tax_kind.startswith("N6"))
                    ):
                        xml_Error2 += self._get_error(
                            _("00401 - Invalid/wrong tax nature in %s")
                            % invoice_tax.name,
                            context,
                        )
                    if tax_payability == "S" and tax_kind.startswith("N6"):
                        xml_Error2 += self._get_error(
                            _("00420 - Wrong tax payability in %s") % invoice_tax.name,
                            context,
                        )
                if tax_rate and (tax_rate < 0.01 or tax_rate > 1):
                    xml_Error2 += self._get_error(
                        _("00424 - Invalid tax rate in %s") % invoice_tax.name, context
                    )
                if tax_kind:
                    if (tax_kind == "FC") or (
                        tax_kind == "N2" and not invoice.partner_id.vat
                    ):
                        if invoice.type[-7:] == "_refund":
                            sum_amounts["discarded"] -= round(
                                invoice_tax.base + invoice_tax.amount, 2
                            )
                        else:
                            sum_amounts["discarded"] += round(
                                invoice_tax.base + invoice_tax.amount, 2
                            )
                        _logger.info(
                            _(
                                "Invoice %s (%d), discarded tax line %s"
                                % (invoice.number, invoice.id, invoice_tax.name)
                            )
                        )
                        continue
                if taxcode_base_id not in inv_line:
                    inv_line[taxcode_base_id] = {}
                    inv_line[taxcode_base_id]["amount_taxable"] = 0.0
                    inv_line[taxcode_base_id]["amount_tax"] = 0.0
                    inv_line[taxcode_base_id]["amount_total"] = 0.0
                    inv_line[taxcode_base_id]["tax_vat_id"] = taxcode_vat_id
                    inv_line[taxcode_base_id]["tax_rate"] = tax_rate
                    inv_line[taxcode_base_id]["tax_nodet_rate"] = tax_nodet_rate
                    inv_line[taxcode_base_id]["tax_kind"] = tax_kind
                    inv_line[taxcode_base_id]["tax_payability"] = tax_payability
                    inv_line[taxcode_base_id]["xml_Error2"] = xml_Error2
                if tax_rate and not inv_line[taxcode_base_id]["tax_rate"]:
                    inv_line[taxcode_base_id]["tax_rate"] = tax_rate
                if tax_nodet_rate and not inv_line[taxcode_base_id]["tax_nodet_rate"]:
                    inv_line[taxcode_base_id]["tax_nodet_rate"] = tax_nodet_rate
                if tax_payability and not inv_line[taxcode_base_id]["tax_payability"]:
                    inv_line[taxcode_base_id]["tax_payability"] = tax_payability
                inv_line[taxcode_base_id]["amount_taxable"] += invoice_tax.base
                inv_line[taxcode_base_id]["amount_tax"] += invoice_tax.amount
                inv_line[taxcode_base_id]["amount_total"] += round(
                    invoice_tax.base + invoice_tax.amount, 2
                )
                if invoice.type[-7:] == "_refund":
                    sum_amounts["taxable"] -= invoice_tax.base
                    sum_amounts["tax"] -= invoice_tax.amount
                    sum_amounts["total"] -= round(
                        invoice_tax.base + invoice_tax.amount, 2
                    )
                else:
                    sum_amounts["taxable"] += invoice_tax.base
                    sum_amounts["tax"] += invoice_tax.amount
                    sum_amounts["total"] += round(
                        invoice_tax.base + invoice_tax.amount, 2
                    )
            if inv_line:
                comm_lines[invoice_id] = {}
                comm_lines[invoice_id]["partner_id"] = invoice.partner_id.id
                comm_lines[invoice_id]["taxes"] = inv_line
        return comm_lines, sum_amounts

    def load_DTE_DTR(self, commitment, commitment_line_model, dte_dtr_id):
        company_id = commitment.company_id.id
        # return 0        #debug
        p_start = 0
        p_stop = 0
        if commitment.period_ids:
            p_start = commitment.period_ids[0].date_start
            p_stop = commitment.period_ids[0].date_end
            for period in commitment.period_ids:
                if period.date_start < p_start:
                    p_start = period.date_start
                if period.date_end > p_stop:
                    p_stop = period.date_end
        where = [
            ("company_id", "=", company_id),
            ("date", ">=", p_start),
            ("date", "<=", p_stop),
            ("communication_type", "=", commitment.type),
            ("state", "in", ("open", "paid")),
        ]
        if dte_dtr_id == "DTE":
            where.append(("type", "in", ["out_invoice", "out_refund"]))
        elif dte_dtr_id == "DTR":
            where.append(("type", "in", ["in_invoice", "in_refund"]))
        else:
            return
        if not commitment.period_ids:
            resl = commitment_line_model.search([("commitment_id", "=", commitment.id)])
            for com_line in resl:
                com_line.unlink()
        context = {"no_except": True}
        comm_lines, sum_amounts = self.load_invoices(
            commitment, commitment_line_model, dte_dtr_id, where, {}, context=context
        )
        if comm_lines:
            for line_id in commitment_line_model.search(
                [
                    ("commitment_id", "=", commitment.id),
                    ("invoice_id", "not in", list(comm_lines.keys())),
                ]
            ):
                line_id.unlink()
        for invoice_id in comm_lines:
            for line_id in commitment_line_model.search(
                [
                    ("commitment_id", "=", commitment.id),
                    ("invoice_id", "=", invoice_id),
                    ("tax_id", "not in", list(comm_lines[invoice_id]["taxes"].keys())),
                ]
            ):
                line_id.unlink()
            for tax_id in comm_lines[invoice_id]["taxes"]:
                # aa = self.env['account.tax'].search([('id', '=', tax_id)]).id
                line = {
                    "commitment_id": commitment.id,
                    "invoice_id": invoice_id,
                    "tax_id": int(
                        self.env["account.tax"].search([("id", "=", tax_id)]).id
                    ),
                    "partner_id": comm_lines[invoice_id]["partner_id"],
                }
                for f in (
                    "amount_total",
                    "amount_taxable",
                    "amount_tax",
                    "tax_vat_id",
                    "tax_rate",
                    "tax_nodet_rate",
                    "tax_kind",
                    "tax_payability",
                    "xml_Error2",
                ):
                    line[f] = comm_lines[invoice_id]["taxes"][tax_id][f]

                commitment_line = commitment_line_model.search(
                    [
                        ("commitment_id", "=", commitment.id),
                        ("invoice_id", "=", invoice_id),
                        ("tax_id", "=", tax_id),
                    ]
                )
                if commitment_line:
                    commitment_line.write(line)
                else:
                    commitment_line_model.create(line)
        return sum_amounts

    @api.model
    def load_DTE(self, commitment):
        """Read all sale invoices in periods"""
        commitment_DTE_line_model = self.env["account.vat.communication.dte.line"]
        sum_amounts = self.load_DTE_DTR(commitment, commitment_DTE_line_model, "DTE")
        return sum_amounts

    @api.model
    def load_DTR(self, commitment):
        """Read all purchase invoices in periods"""
        commitment_DTR_line_model = self.env["account.vat.communication.dtr.line"]
        sum_amounts = self.load_DTE_DTR(commitment, commitment_DTR_line_model, "DTR")
        return sum_amounts

    @api.multi
    def compute_amounts(self, ids):
        if type(ids) == dict:
            ids = self.ids
            self = self.env["account.vat.communication"]
        for commitment in self.browse(ids):
            dte_sum_amounts = self.load_DTE(commitment)
            dtr_sum_amounts = self.load_DTR(commitment)
            vals = {}
            for t in ("total", "taxable", "tax", "discarded"):
                f = "dte_amount_" + t
                vals[f] = dte_sum_amounts[t]
                f = "dtr_amount_" + t
                vals[f] = dtr_sum_amounts[t]
            self.write([commitment.id])
        return True

    @api.model
    def onchange_fiscalcode(self, fiscalcode, name, country=None):
        name = name or "fiscalcode"
        if fiscalcode:
            country_model = self.env["res.country"]
            if country and country_model.browse(country.id).code != "IT":
                return {"value": {name: fiscalcode, "individual": True}}
            elif len(fiscalcode) == 11:
                res_partner_model = self.env["res.partner"]
                chk = res_partner_model.simple_vat_check("it", fiscalcode)
                if not chk:
                    return {
                        "value": {name: False},
                        "warning": {
                            "title": "Invalid fiscalcode!",
                            "message": "Invalid vat number",
                        },
                    }
                individual = False
            elif len(fiscalcode) != 16:
                return {
                    "value": {name: False},
                    "warning": {
                        "title": "Invalid len!",
                        "message": "Fiscal code len must be 11 or 16",
                    },
                }
            else:
                fiscalcode = fiscalcode.upper()
                chk = codicefiscale.control_code(fiscalcode[0:15])
                if chk != fiscalcode[15]:
                    value = fiscalcode[0:15] + chk
                    return {
                        "value": {name: value},
                        "warning": {
                            "title": "Invalid fiscalcode!",
                            "message": "Fiscal code could be %s" % (value),
                        },
                    }
                individual = True
            return {"value": {name: fiscalcode, "individual": individual}}
        return {"value": {"individual": False}}

    #
    # INTERNAL INTERFACE TO XML EXPORT CODE
    #
    @api.model
    def get_xml_fattura_header(self, commitment, dte_dtr_id):
        """Return DatiFatturaHeader: may be empty"""
        res = {}
        if commitment.codice_carica and commitment.soggetto_codice_fiscale:
            res["xml_CodiceFiscale"] = commitment.soggetto_codice_fiscale
            res["xml_Carica"] = commitment.codice_carica
        return res

    @api.model
    def get_xml_company(self, commitment, dte_dtr_id):
        """Return data of CessionarioCommittente or CedentePrestatore
        which referers to current company.
        This function is pair to get_xml_cessionario_cedente which returns
        customer or supplier data"""
        line_model = self.env["account.vat.communication.line"]
        res = line_model._dati_partner(commitment.company_id.partner_id, None)
        if res.get("xml_IdPaese", None) != "IT":
            raise UserError(_("Missed company VAT number"))
        return res

    @api.model
    def get_partner_list(self, commitment, dte_dtr_id):
        """Return list of partner_id in communication by commitment_id
        This function has to be used for CessionarioCommittente or
        CedentePrestatore iteration"""
        if dte_dtr_id != "DTE" and dte_dtr_id != "DTR":
            raise UserError(_("Internal error: no DTE neither DTR indexed"))
        model_name = "account.vat.communication.%s.line" % dte_dtr_id.lower()
        table_name = model_name.replace(".", "_")
        self.env.cr.execute(
            "SELECT DISTINCT partner_id FROM %s WHERE commitment_id = %%s" % table_name,
            (commitment.id,),
        )
        ids = []
        for rec in self.env.cr.fetchall():
            ids.append(rec[0])
        return ids

    @api.model
    def get_xml_cessionario_cedente(self, commitment, partner_id, dte_dtr_id):
        """Return data of CessionarioCommittente or CedentePrestatore
        This function has to be used as result of every iteration of
        get_partner_list"""
        commitment_line_model = self.env["account.vat.communication.line"]
        res_partner_model = self.env["res.partner"]
        partner = res_partner_model.browse(partner_id)
        return commitment_line_model._dati_partner(partner, None)

    @api.model
    def get_invoice_list(self, commitment, partner_id, dte_dtr_id):
        """Return list of invoices in communication
        by partner_id and commitment_id.
        This function has to be used for CessionarioCommittente or
        CedentePrestatore sub-iteration"""
        if dte_dtr_id != "DTE" and dte_dtr_id != "DTR":
            raise UserError(_("Internal error: no DTE neither DTR selected"))
        model_name = "account.vat.communication.%s.line" % dte_dtr_id.lower()
        table_name = model_name.replace(".", "_")
        self.env.cr.execute(
            """SELECT DISTINCT invoice_id FROM %s
               WHERE commitment_id = %%s and partner_id = %%s""" % table_name,
            (commitment.id, partner_id),
        )
        ids = []
        for rec in self.env.cr.fetchall():
            ids.append(rec[0])
        return ids

    @api.model
    def get_xml_invoice(self, commitment, invoice_id, dte_dtr_id):
        """Return data of Invoice.
        This function has to be used as result of every iteration of
        get_invoice_list"""
        account_invoice_model = self.env["account.invoice"]
        invoice = account_invoice_model.browse(invoice_id)
        res = {}
        res["xml_TipoDocumento"] = self.env[
            "account.vat.communication.line"
        ]._tipodocumento(invoice)
        res["xml_Data"] = invoice.date_invoice
        if invoice.type in ("in_invoice", "in_refund"):
            if not invoice.reference:
                raise UserError(
                    _("Missed supplier invoice number %s, id=%d")
                    % (invoice.number, invoice.id)
                )
            res["xml_Numero"] = invoice.reference[-20:]
            res["xml_DataRegistrazione"] = invoice.date
            res["xml_DataContabile"] = invoice.date
        else:
            res["xml_Numero"] = invoice.number[:20]
        return res

    @api.model
    def get_riepilogo_list(self, commitment, invoice_id, dte_dtr_id):
        """Return list of tax lines of invoice in communication
        by invoice_id and commitment.id.
        This function has to be used for CessionarioCommittente or
        CedentePrestatore sub-sub-iteration"""
        if dte_dtr_id != "DTE" and dte_dtr_id != "DTR":
            raise UserError(_("Internal error: no DTE neither DTR selected"))
        model_name = "account.vat.communication.%s.line" % dte_dtr_id.lower()
        line_model = self.env[model_name]
        ids = line_model.search(
            [("commitment_id", "=", commitment.id), ("invoice_id", "=", invoice_id)]
        )
        return ids

    @api.model
    def get_xml_riepilogo(self, commitment, line_id, dte_dtr_id):
        """Return data of tax invoice line.
        This function has to be used as result of every iteration of
        get_riepilogo_list"""
        commitment_line_model = self.env["account.vat.communication.line"]
        # model_name = 'account.vat.communication.%s.line' % dte_dtr_id.lower()
        # line_model = self.env[model_name]
        CommitmentLine = line_id
        return commitment_line_model._dati_line(CommitmentLine, {"xml": True})


class CommitmentLine(models.AbstractModel):
    _name = "account.vat.communication.line"

    def _get_error(self, error, context):
        if context.get("no_except", True):
            return error
        else:
            raise UserError(error)
        return False

    @api.model
    def _dati_partner(self, partner, args, context=None):
        if not context:
            context = self.env.context

        if release.major_version == "6.1":
            address_id = self.env["res.partner"].address_get([partner.id])["default"]
            address = self.env["res.partner.address"].browse(address_id)
        else:
            address = partner

        res = {"xml_Error1": ""}
        if partner.vat:
            res["xml_IdPaese"], res["xml_IdCodice"] = partner.split_vat_n_country(
                partner.vat
            )
        res["xml_Nazione"] = address.country_id.code or res.get("xml_IdPaese")
        if not res.get("xml_Nazione"):
            self._get_error(_("Unknow country of %s") % partner.name, context)

        if (partner.individual or not partner.is_company) and partner.fiscalcode:
            r = self.env["account.vat.communication"].onchange_fiscalcode(
                partner.fiscalcode, None, country=partner.country_id
            )
            if "warning" in r:
                res["xml_Error1"] += self._get_error(
                    _("00302 - " "Invalid fiscalcode of %s") % partner.name, context
                )
            if res.get("xml_Nazione", "") == "IT" and partner.fiscalcode != res.get(
                "xml_IdCodice"
            ):
                res["xml_CodiceFiscale"] = partner.wep_fiscalcode(partner.fiscalcode)
        elif res.get("xml_IdPaese", "") == "IT":
            pass
        elif not partner.vat:
            res["xml_CodiceFiscale"] = "99999999999"

        if partner.individual or not partner.is_company:
            if release.major_version == "6.1":
                if partner.fiscalcode_firstname and partner.fiscalcode_surname:
                    res["xml_Nome"] = partner.fiscalcode_firstname
                    res["xml_Cognome"] = partner.fiscalcode_surname
                else:
                    res["xml_Denominazione"] = partner.name
            else:
                res["xml_Nome"] = partner.firstname
                res["xml_Cognome"] = partner.lastname
            if not res.get("xml_Cognome") or not res.get("xml_Nome"):
                res["xml_Error1"] += self._get_error(
                    _("Invalid First or Last name %s") % partner.name, context
                )
        else:
            res["xml_Denominazione"] = partner.name
        if (
            not res.get("xml_CodiceFiscale")
            and not res.get("xml_IdPaese")
            and not res.get("xml_IdCodice")
        ):
            res["xml_Error1"] += self._get_error(
                _("00464 - " "Partner %s without fiscal data") % partner.name, context
            )
        if (
            res.get("xml_IdPaese")
            and res.get("xml_IdPaese") != "EU"
            and res.get("xml_IdPaese") != res["xml_Nazione"]
        ):
            res["xml_Error1"] += self._get_error(
                _("003XC - " "Partner %s vat country differs from country")
                % partner.name,
                context,
            )

        if address.street:
            res["xml_Indirizzo"] = address.street.replace(u"'", "").replace(u"’", "")
        else:
            res["xml_Error1"] += self._get_error(
                _("003XA - " "Partner %s without street on address") % partner.name,
                context,
            )

        if res.get("xml_IdPaese", "") == "IT":
            if address.zip:
                res["xml_CAP"] = address.zip.replace("x", "0").replace("%", "0")
            if len(res["xml_CAP"]) != 5 or not res["xml_CAP"].isdigit():
                res["xml_Error1"] += self._get_error(
                    _("003XZ - " "Partner %s has wrong zip code") % partner.name,
                    context,
                )

        res["xml_Comune"] = address.city or " "
        if not address.city:
            res["xml_Error1"] += self._get_error(
                _("003XY - " "Partner %s without city on address") % partner.name,
                context,
            )

        if res["xml_Nazione"] == "IT":
            if release.major_version == "6.1":
                res["xml_Provincia"] = address.province.code
            else:
                res["xml_Provincia"] = partner.state_id.code
            if not res["xml_Provincia"]:
                del res["xml_Provincia"]
                res["xml_Error1"] += self._get_error(
                    _("003XP - " "Partner %s without province on address")
                    % partner.name,
                    context,
                )
        return res

    @api.model
    def _dati_line(self, line, args):

        res = {}
        res["xml_ImponibileImporto"] = abs(line.amount_taxable)
        res["xml_Imposta"] = abs(line.amount_tax)
        res["xml_Aliquota"] = line.tax_rate * 100
        res["xml_Detraibile"] = 100.0 - line.tax_nodet_rate * 100
        if line.tax_kind:
            res["xml_Natura"] = line.tax_id.kind_id.code
        else:
            res["xml_Natura"] = line.tax_kind
        # res['xml_Natura'] = line.tax_id.kind_id.code
        res["xml_EsigibilitaIVA"] = line.tax_payability
        res["xml_Error2"] = line.xml_Error2
        return res

    @api.model
    def _tipodocumento(self, invoice):
        # cr = self.env.cr
        # uid = self.env.user.id
        # context = self.env.context

        doctype = invoice.type
        country_code = self.env["account.vat.communication"].get_country_code(
            invoice.partner_id
        )
        if invoice.fiscal_document_type_id:
            return invoice.fiscal_document_type_id.code
        elif (
            doctype == "out_invoice"
            and not invoice.partner_id.vat
            and not invoice.partner_id.fiscalcode
        ):
            if invoice.amount_total >= 0:
                return "TD07"
            else:
                return "TD08"
        elif (
            doctype == "out_refund"
            and not invoice.partner_id.vat
            and not invoice.partner_id.fiscalcode
        ):
            return "TD08"
        elif (
            country_code != "IT"
            and country_code in EU_COUNTRIES + ["EU"]
            and doctype == "in_invoice"
        ):
            return "TD11"
        elif doctype in ("out_invoice", "in_invoice"):
            if invoice.amount_total >= 0:
                return "TD01"
            else:
                return "TD04"
        elif doctype in ("out_refund", "in_refund"):
            return "TD04"
        else:
            raise UserError(
                _("Invalid type %s (%s) for invoice %s")
                % (doctype, country_code, invoice.number)
            )


class CommitmentDTELine(models.Model):
    _name = "account.vat.communication.dte.line"
    _inherit = "account.vat.communication.line"

    @api.multi
    def _xml_dati_partner(self, fname=None, args=None):
        # cr = self.env.cr
        # uid = self.env.user.id
        ids = self.ids
        context = self.env.context

        res = {}
        for line in self.browse(ids):
            ctx = context.copy()
            ctx["no_except"] = True
            fields = self._dati_partner(line.partner_id, args, context=ctx)
            result = {}
            for f in ("xml_IdPaese", "xml_IdCodice", "xml_CodiceFiscale"):
                if fields.get(f, ""):
                    result[f] = fields[f]
                else:
                    result[f] = False
            line.xml_IdPaese = result["xml_IdPaese"]
            line.xml_IdCodice = result["xml_IdCodice"]
            line.xml_CodiceFiscale = result["xml_CodiceFiscale"]
            line.xml_Error1 = fields["xml_Error1"]
        return res

    @api.multi
    def _xml_dati_line(self, fname=None, args=None):
        # cr = self.env.cr
        # uid = self.env.user.id
        ids = self.ids
        # context = self.env.context
        res = {}
        for line in self.browse(ids):
            data = self._dati_line(line, args)
            line.xml_Aliquota = data["xml_Aliquota"]
            line.xml_Detraibile = data["xml_Detraibile"]
            line.xml_ImponibileImporto = data["xml_ImponibileImporto"]
            line.xml_Imposta = data["xml_Imposta"]
            line.xml_Natura = data["xml_Natura"]
            line.xml_Error2 = data["xml_Error2"]
        return res

    @api.multi
    def _xml_tipodocumento(self, fname=None, args=None):
        ids = self.ids
        res = {}
        for line in self.browse(ids):
            td = self._tipodocumento(line.invoice_id)
            line.xml_TipoDocumento = td
        return res

    commitment_id = fields.Many2one("account.vat.communication", "VAT commitment")
    invoice_id = fields.Many2one("account.invoice", "Invoice")
    tax_id = fields.Many2one("account.tax", "VAT code")
    partner_id = fields.Many2one("res.partner", "Partner", readonly=True)
    tax_vat_id = fields.Many2one("account.tax", "VAT code", readonly=True)
    tax_rate = fields.Float("VAT rate", readonly=True)
    tax_nodet_rate = fields.Float("VAT non deductible rate", readonly=True)
    tax_kind = fields.Char("Non taxable nature", readonly=True, oldname="tax_nature")
    tax_payability = fields.Char("VAT payability", readonly=True)
    amount_total = fields.Float("Amount", digits=dp.get_precision("Account"))
    amount_taxable = fields.Float("Taxable amount", digits=dp.get_precision("Account"))
    amount_tax = fields.Float("Tax amount", digits=dp.get_precision("Account"))
    xml_Error1 = fields.Char(
        compute="_xml_dati_partner",
        string="Error",
        store=False,
        index=True,
        readonly=True,
    )
    xml_Error2 = fields.Char(string="Error", readonly=True)
    xml_IdPaese = fields.Char(
        compute="_xml_dati_partner",
        string="Country",
        store=False,
        index=True,
        readonly=True,
    )
    xml_IdCodice = fields.Char(
        compute="_xml_dati_partner",
        string="VAT number",
        store=False,
        index=True,
        readonly=True,
    )
    xml_CodiceFiscale = fields.Char(
        compute="_xml_dati_partner",
        string="Fiscalcode",
        store=False,
        index=True,
        readonly=True,
    )
    xml_TipoDocumento = fields.Char(
        compute="_xml_tipodocumento",
        string="Document type",
        help="Values: TD01=invoice, TD04=refund",
        store=False,
        index=True,
        readonly=True,
    )
    xml_ImponibileImporto = fields.Float(
        compute="_xml_dati_line",
        string="Taxable",
        store=False,
        index=True,
        readonly=True,
    )
    xml_Imposta = fields.Float(
        compute="_xml_dati_line", string="Tax", store=False, index=True, readonly=True
    )
    xml_Aliquota = fields.Float(
        compute="_xml_dati_line",
        string="Tax rate",
        store=False,
        index=True,
        readonly=True,
    )
    xml_Detraibile = fields.Float(
        compute="_xml_dati_line",
        string="Tax deductible",
        store=False,
        index=True,
        readonly=True,
    )
    xml_Natura = fields.Char(
        compute="_xml_dati_line",
        string="Tax type",
        store=False,
        index=True,
        readonly=True,
    )


class CommitmentDTRLine(models.Model):
    _name = "account.vat.communication.dtr.line"
    _inherit = "account.vat.communication.line"

    @api.multi
    def _xml_dati_partner(self, fname=None, args=None):
        # cr = self.env.cr
        # uid = self.env.user.id
        ids = self.ids
        context = self.env.context

        res = {}
        for line in self.browse(ids):
            ctx = context.copy()
            ctx["no_except"] = True
            fields = self._dati_partner(line.partner_id, args, context=ctx)
            result = {}
            for f in ("xml_IdPaese", "xml_IdCodice", "xml_CodiceFiscale"):
                if fields.get(f, ""):
                    result[f] = fields[f]
                else:
                    result[f] = False
            line.xml_IdPaese = result["xml_IdPaese"]
            line.xml_IdCodice = result["xml_IdCodice"]
            line.xml_CodiceFiscale = result["xml_CodiceFiscale"]
            line.xml_Error1 = fields["xml_Error1"]
        return res

    @api.multi
    def _xml_dati_line(self, fname=None, args=None):
        # cr = self.env.cr
        # uid = self.env.user.id
        ids = self.ids
        # context = self.env.context
        res = {}
        for line in self.browse(ids):
            data = self._dati_line(line, args)
            line.xml_Aliquota = data["xml_Aliquota"]
            line.xml_Detraibile = data["xml_Detraibile"]
            line.xml_ImponibileImporto = data["xml_ImponibileImporto"]
            line.xml_Imposta = data["xml_Imposta"]
            line.xml_Natura = data["xml_Natura"]
        return res

    @api.multi
    def _xml_tipodocumento(self, fname=None, args=None):
        # cr=self.env.cr
        # uid=self.env.user.id
        ids = self.ids
        # context=self.env.context
        res = {}
        for line in self.browse(ids):
            td = self._tipodocumento(line.invoice_id)
            line.xml_TipoDocumento = td
        return res

    commitment_id = fields.Many2one("account.vat.communication", "VAT commitment")
    invoice_id = fields.Many2one("account.invoice", "Invoice")
    tax_id = fields.Many2one("account.tax", "VAT code")
    partner_id = fields.Many2one("res.partner", "Partner", readonly=True)
    tax_vat_id = fields.Many2one("account.tax", "VAT code", readonly=True)
    tax_rate = fields.Float("VAT rate", readonly=True)
    tax_nodet_rate = fields.Float("VAT non deductible rate", readonly=True)
    tax_kind = fields.Char("Non taxable nature", readonly=True, oldname="tax_nature")
    tax_payability = fields.Char("VAT payability", readonly=True)
    amount_total = fields.Float("Amount", digits=dp.get_precision("Account"))
    amount_taxable = fields.Float("Taxable amount", digits=dp.get_precision("Account"))
    amount_tax = fields.Float("Tax amount", digits=dp.get_precision("Account"))
    xml_Error1 = fields.Char(
        compute="_xml_dati_partner",
        string="Error",
        store=False,
        index=True,
        readonly=True,
    )
    xml_Error2 = fields.Char(string="Error", readonly=True)
    xml_IdPaese = fields.Char(
        compute="_xml_dati_partner",
        string="Country",
        store=False,
        index=True,
        readonly=True,
    )
    xml_IdCodice = fields.Char(
        compute="_xml_dati_partner",
        string="VAT number",
        store=False,
        index=True,
        readonly=True,
    )
    xml_CodiceFiscale = fields.Char(
        compute="_xml_dati_partner",
        string="Fiscalcode",
        store=False,
        index=True,
        readonly=True,
    )
    xml_TipoDocumento = fields.Char(
        compute="_xml_tipodocumento",
        string="Document type",
        help="Values: TD01=invoice, TD04=refund",
        store=False,
        index=True,
        readonly=True,
    )
    xml_ImponibileImporto = fields.Float(
        compute="_xml_dati_line",
        string="Taxable",
        store=False,
        index=True,
        readonly=True,
    )
    xml_Imposta = fields.Float(
        compute="_xml_dati_line", string="Tax", store=False, index=True, readonly=True
    )
    xml_Aliquota = fields.Float(
        compute="_xml_dati_line",
        string="Tax rate",
        store=False,
        index=True,
        readonly=True,
    )
    xml_Detraibile = fields.Float(
        compute="_xml_dati_line",
        string="Tax deductible",
        store=False,
        index=True,
        readonly=True,
    )
    xml_Natura = fields.Char(
        compute="_xml_dati_line",
        string="Tax type",
        store=False,
        index=True,
        readonly=True,
    )


class DateTange(models.Model):
    _inherit = "date.range"

    vat_commitment_id = fields.Many2one("account.vat.communication", "VAT commitment")
