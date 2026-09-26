# -*- coding: utf-8 -*-
#
# Copyright 2018-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
import logging

import pyxb

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

from odoo.addons.l10n_it_ade.bindings import fatturapa_v_1_2

_logger = logging.getLogger(__name__)


class WizardImportFatturapaSale(models.TransientModel):
    """Create customer invoices out of e-invoice xml files.

    Everything but the few points telling a received bill from an issued
    invoice is inherited from wizard.import.fatturapa of l10n_it_einvoice_in:
    the company is read from CedentePrestatore instead of
    CessionarioCommittente, the partner the other way round, the journal is a
    sale one and products are looked up by internal code rather than by
    supplier code.
    """

    _name = "wizard.import.fatturapa.sale"
    _inherit = "wizard.import.fatturapa"
    _description = "Import sale e-invoice"

    customer_product_search = fields.Selection(
        [
            ("c", "By internal code"),
            ("cn", "By code or exact name"),
            ("cndx", "By code or similar name"),
            ("n", "By exact name"),
        ],
        "Customer product search",
        default="c",
        help="How to search for product from sale e-invoice",
    )

    def get_invoice_obj(self, fatturapa_attachment):
        xml_string = fatturapa_attachment.get_normalized_xml_string()
        if xml_string:
            pyxb.RequireValidWhenParsing(False)
            inv_obj = fatturapa_v_1_2.CreateFromDocument(xml_string)
            pyxb.RequireValidWhenParsing(True)
            return inv_obj
        return False

    @api.model
    def default_get(self, fields_list):
        # active_ids are fatturapa.attachment.out here, while the parent walks
        # fatturapa.attachment.in: hide them from it
        res = super(
            WizardImportFatturapaSale, self.with_context(active_ids=False)
        ).default_get(fields_list)
        res["e_invoice_detail_level"] = "2"
        res["customer_product_search"] = (
            self.env.user.company_id.customer_product_search or "c"
        )
        fatturapa_attachment_ids = self.env.context.get("active_ids", False)
        if fatturapa_attachment_ids is False:
            return res
        fatturapa_attachment_model = self.env["fatturapa.attachment.out"]
        partners = self.env["res.partner"]
        for fatturapa_attachment in fatturapa_attachment_model.browse(
            fatturapa_attachment_ids
        ):
            if fatturapa_attachment.out_invoice_ids:
                raise UserError(
                    _("File %s is linked to invoices yet.")
                    % fatturapa_attachment.name
                )
            partners |= fatturapa_attachment.invoice_partner_id
            if len(partners) == 1:
                if partners[0].e_invoice_detail_level:
                    res["e_invoice_detail_level"] = partners[0].e_invoice_detail_level
                if partners[0].e_invoice_customer_product_search:
                    res["customer_product_search"] = (
                        partners[0].e_invoice_customer_product_search
                    )
        return res

    # Hooks of wizard.import.fatturapa, see l10n_it_einvoice_in

    def get_tax_type_use(self):
        return "sale"

    def get_invoice_journal(self, company):
        return self.get_sale_journal(company)

    def get_invoice_default_account(self, journal):
        return journal.default_debit_account_id

    def get_invoice_partner_account(self, partner):
        return partner.property_account_receivable_id

    def get_invoice_attachment_field(self):
        return "fatturapa_attachment_out_id"

    def get_invoice_header_data(
        self, fatt, fatturapa_attachment, FatturaBody, partner_id
    ):
        return self.env["account.invoice"].xml_get_header_data_sale(
            self, fatt, fatturapa_attachment, FatturaBody, partner_id
        )

    def use_xml_payment_term(self, company):
        return company.customer_payment_term == "customer"

    def get_line_product(self, line, partner, company):
        """Look the product up by internal code or name.

        A sale e-invoice carries our own codes, so product.supplierinfo, which
        the purchase import searches, is of no use here.
        """
        product = None
        product_model = self.env["product.product"]
        hashname = ""
        if "x" in self.customer_product_search:
            hashname = self.get_hashname(line.Descrizione, like=True)
        if "c" in self.customer_product_search and line.CodiceArticolo:
            for CodiceArticolo in line.CodiceArticolo:
                products = product_model.search(
                    [("default_code", "=", CodiceArticolo.CodiceValore)]
                )
                if len(products) == 1:
                    product = fields.first(products)
                    break
        if not product and "n" in self.customer_product_search:
            products = product_model.search([("name", "=", line.Descrizione)])
            if len(products) == 1:
                product = fields.first(products)
        if not product and "x" in self.customer_product_search:
            products = product_model.search([("name", "ilike", hashname)])
            if len(products) == 1:
                product = fields.first(products)
        if (
            not product
            and line.PrezzoTotale
            and float(line.PrezzoTotale)
            and partner.e_invoice_default_product_id
        ):
            product = partner.e_invoice_default_product_id
        return product

    def adjust_accounting_data(self, product, line_vals):
        """Income account and customer taxes, the sale counterpart."""
        if product.product_tmpl_id.property_account_income_id:
            line_vals[
                "account_id"
            ] = product.product_tmpl_id.property_account_income_id.id
        elif product.product_tmpl_id.categ_id.property_account_income_categ_id:
            line_vals[
                "account_id"
            ] = product.product_tmpl_id.categ_id.property_account_income_categ_id.id
        account = self.env["account.account"].browse(line_vals["account_id"])
        new_tax = None
        if len(product.product_tmpl_id.taxes_id) == 1:
            new_tax = product.product_tmpl_id.taxes_id[0]
        elif len(account.tax_ids) == 1:
            new_tax = account.tax_ids[0]
        if new_tax:
            line_tax_id = (
                line_vals.get("invoice_line_tax_ids")
                and line_vals["invoice_line_tax_ids"][0][2][0]
            )
            line_tax = self.env["account.tax"].browse(line_tax_id)
            if new_tax.id != line_tax_id:
                if new_tax._get_tax_amount() != line_tax._get_tax_amount():
                    self.log_inconsistency(
                        _(
                            "Il file XML ha codice IVA %s. "
                            "Il prodotto %s ha codice IVA %s. "
                            "Selezionare il codice IVA corretto,"
                        )
                        % (line_tax.name, product.name, new_tax.name)
                    )
                else:
                    line_vals["invoice_line_tax_ids"] = [(6, 0, [new_tax.id])]

    @api.multi
    def importFatturaPA(self):
        fatturapa_attachment_model = self.env["fatturapa.attachment.out"]
        fatturapa_attachment_ids = self.env.context.get("active_ids", False)
        linked_invoice = self.env.context.get("linked_invoice", False)
        invoice_model = self.env["account.invoice"]
        partner_model = self.env["res.partner"]
        new_invoices = []
        for fatturapa_attachment_id in fatturapa_attachment_ids:
            self.__dict__.update(self.with_context(inconsistencies="").__dict__)
            fatturapa_attachment = fatturapa_attachment_model.browse(
                fatturapa_attachment_id
            )
            if fatturapa_attachment.out_invoice_ids:
                raise UserError(_("File is linked to invoices yet."))
            fatt = self.get_invoice_obj(fatturapa_attachment)
            if not fatt:
                raise UserError(
                    _("File %s is not a valid e-invoice.")
                    % fatturapa_attachment.name
                )
            header = fatt.FatturaElettronicaHeader
            # 1.2 the seller is this company: xml_get_company() raises when not
            self.env["res.company"].xml_get_company(
                header.CedentePrestatore.DatiAnagrafici, wizard=self
            )
            # 1.4 the buyer is the customer of the invoice
            partner_id = partner_model.getCustomerBase(
                header.CessionarioCommittente, fatturapa=self
            )
            if partner_id < 1:
                _logger.error("Unrecognized customer")
                continue
            # 1.3
            TaxRappresentative = header.RappresentanteFiscale
            # 1.5
            Intermediary = header.TerzoIntermediarioOSoggettoEmittente

            generic_inconsistencies = ""
            if self.env.context.get("inconsistencies"):
                generic_inconsistencies = self.env.context["inconsistencies"] + "\n\n"
            # 2
            for FatturaBody in fatt.FatturaElettronicaBody:
                # reset inconsistencies
                self.__dict__.update(self.with_context(inconsistencies="").__dict__)
                if invoice_model.is_self_billing(FatturaBody):
                    self.log_inconsistency(
                        _(
                            "Documento di tipo %s (autofattura): verificare "
                            "cedente e cessionario del documento creato."
                        )
                        % FatturaBody.DatiGenerali.DatiGeneraliDocumento.TipoDocumento
                    )
                if linked_invoice:
                    invoice = linked_invoice
                    invoice_id = invoice.id
                else:
                    invoice_id = self.invoiceCreate(
                        fatt, fatturapa_attachment, FatturaBody, partner_id
                    )
                    invoice = invoice_model.browse(invoice_id)
                self.set_StabileOrganizzazione(header.CedentePrestatore, invoice)
                vals = {}
                if TaxRappresentative:
                    tax_partner_id = partner_model.getPartnerBase(
                        TaxRappresentative.DatiAnagrafici, fatturapa=self
                    )
                    if tax_partner_id > 0:
                        vals["tax_representative_id"] = tax_partner_id
                if Intermediary:
                    intermediary_id = partner_model.getPartnerBase(
                        Intermediary.DatiAnagrafici, fatturapa=self
                    )
                    if intermediary_id > 0:
                        vals["intermediary"] = intermediary_id
                if vals:
                    invoice.write(vals)
                new_invoices.append(invoice_id)
                self.check_invoice_amount(invoice, FatturaBody)

                if self.env.context.get("inconsistencies"):
                    invoice_inconsistencies = self.env.context["inconsistencies"]
                else:
                    invoice_inconsistencies = ""
                invoice.inconsistencies = (
                    generic_inconsistencies + invoice_inconsistencies
                )
            # Also covers a file uploaded before this module was installed,
            # which may still sit in the "ready" state
            att_vals = {"imported": True}
            if "state" in fatturapa_attachment._fields:
                att_vals["state"] = "sent"
            fatturapa_attachment.write(att_vals)

        return {
            "view_type": "form",
            "name": "Electronic Invoices",
            "view_mode": "tree,form",
            "res_model": "account.invoice",
            "type": "ir.actions.act_window",
            "domain": [("id", "in", new_invoices)],
        }
