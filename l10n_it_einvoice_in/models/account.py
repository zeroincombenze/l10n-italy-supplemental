# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare
# from odoo.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_attachment_in_id = fields.Many2one(
        "fatturapa.attachment.in", "E-bill Import File", ondelete="restrict", copy=False
    )
    inconsistencies = fields.Text("Import Inconsistencies", copy=False)
    e_invoice_line_ids = fields.One2many(
        "einvoice.line", "invoice_id",
        string="e-Lines Detail", readonly=True, copy=False
    )

    e_invoice_amount_untaxed = fields.Monetary(
        string="E-Invoice Untaxed Amount", readonly=True
    )
    e_invoice_amount_tax = fields.Monetary(string="E-Invoice Tax Amount", readonly=True)
    e_invoice_amount_total = fields.Monetary(
        string="E-Invoice Total Amount", readonly=True
    )

    e_invoice_reference = fields.Char(
        string="E-invoice vendor reference", readonly=True
    )

    e_invoice_date_invoice = fields.Date(string="E-invoice date", readonly=True)

    e_invoice_validation_error = fields.Boolean(
        compute="_compute_e_invoice_validation_error"
    )

    e_invoice_validation_message = fields.Text(
        compute="_compute_e_invoice_validation_error"
    )

    e_invoice_force_validation = fields.Boolean(string="Force E-Invoice Validation")

    e_invoice_received_date = fields.Date(string="E-Bill Received Date")

    @api.multi
    def _compute_einvoice_amounts(self):
        for invoice in self:
            # Evaluate e_invoice_amount(s) just for invoice created before this upgraded
            # module
            if (
                invoice.e_invoice_amount_total
                and invoice.e_invoice_amount_untaxed
            ):
                continue
            round_curr = invoice.currency_id.round  # pragma: no cover
            # rounding = invoice.currency_id.rounding
            e_invoice_amount_tax = e_invoice_amount_untaxed = line_amount = 0.0
            for ln in invoice.fatturapa_summary_ids:
                e_invoice_amount_untaxed += ln.amount_untaxed
                e_invoice_amount_tax += ln.amount_tax
            for ln in invoice.e_invoice_line_ids:
                line_amount += ln.total_price
            invoice.e_invoice_amount_untaxed = round_curr(e_invoice_amount_untaxed)
            invoice.e_invoice_amount_tax = round_curr(e_invoice_amount_tax)
            invoice.efatt_xml_rounding = round_curr(line_amount
                                                    - e_invoice_amount_untaxed)
            invoice.e_invoice_amount_total = round_curr(
                self.e_invoice_amount_untaxed
                + self.e_invoice_amount_tax
                + self.efatt_xml_rounding)

    @api.model
    def float_diff_in_range(self, left, right):
        rounding = self.currency_id.rounding
        return (
            float_compare(left,
                          right,
                          precision_rounding=rounding) != 0
            and float_compare(left,
                              right,
                              precision_rounding=rounding * 10.0) == 0
        )

    # @api.multi
    # def compute_taxes(self):
    #     res = super(AccountInvoice, self).compute_taxes()
    #     for invoice in self:
    #         if invoice.type not in ("in_invoice", "in_refund"):
    #             continue
    #         if not invoice.e_invoice_amount_total:
    #             continue
    #
    #         # rounding = invoice.currency_id.rounding
    #         for inv_tax_line in invoice.tax_line_ids:
    #             for ln in invoice.fatturapa_summary_ids:
    #                 if (
    #                     ln.tax_rate != inv_tax_line.tax_id.amount
    #                     or ln.non_taxable_nature != inv_tax_line.tax_id.kind_id
    #                 ):
    #                     continue
    #                 if self.float_diff_in_range(inv_tax_line.amount, ln.amount_tax):
    #                     inv_tax_line.amount = ln.amount_tax
    #                 if self.float_diff_in_range(inv_tax_line.base, ln.amount_untaxed):
    #                     inv_tax_line.base = ln.amount_untaxed
    #     return res

    @api.multi
    def get_taxes_values(self):
        tax_grouped = super(AccountInvoice, self).get_taxes_values()
        if self.type in ("in_invoice", "in_refund") and self.e_invoice_amount_total:
            Tax = self.env["account.tax"]
            for ln in self.fatturapa_summary_ids:
                tax_id, errmsg = Tax.search_tax_by_code_kind(
                    self.company_id.id, ln.tax_rate, ln.non_taxable_nature.code)
                for vals in tax_grouped.items():
                    if tax_id == vals[1]["tax_id"]:
                        if self.float_diff_in_range(vals[1]["base"], ln.amount_untaxed):
                            vals[1]["base"] = ln.amount_untaxed
                        if self.float_diff_in_range(vals[1]["amount"], ln.amount_tax):
                            vals[1]["amount"] = ln.amount_tax
        return tax_grouped

    def load_rounding_values(self, round_amount, tax_rate=None, tax_kind=None):
        if round_amount > 0:
            arrotondamenti_account_id = (
                self.env.user.company_id.arrotondamenti_passivi_account_id
            )
            if not arrotondamenti_account_id:
                raise UserError(
                    _("Round down account is not set in Accounting Settings")
                )
            name = _("Rounding down")
        else:
            arrotondamenti_account_id = (
                self.env.user.company_id.arrotondamenti_attivi_account_id
            )
            if not arrotondamenti_account_id:
                raise UserError(
                    _("Round up account is not set in Accounting Settings")
                )
            name = _("Rounding up")
        if tax_rate or tax_kind:
            tax_id, errmsg = self.env["account.tax"].search_tax_by_code_kind(
                self.company_id.id, tax_rate, tax_kind)
        else:
            tax_id = self.env.user.company_id.arrotondamenti_tax_id.id
            if not tax_id:
                raise UserError(
                    _("Round down tax code is not set in Accounting Settings")
                )
        return {
            "name": name,
            "price_unit": round_amount,
            "account_id": arrotondamenti_account_id.id,
            "invoice_line_tax_ids": [(6, 0, [tax_id])],
            "quantity": 1,
        }

    @api.one
    def create_round_lines(self):
        self.ensure_one()
        rounding = self.currency_id.rounding
        round_curr = self.currency_id.round
        force_round_total = False
        summary_amounts = {}
        for ln in self.fatturapa_summary_ids:
            kk = (ln.tax_rate, ln.non_taxable_nature)
            if kk not in summary_amounts:
                summary_amounts[kk] = {"amt": 0.0, "tax": 0.0}
            summary_amounts[kk]["amt"] += ln.amount_untaxed
            summary_amounts[kk]["tax"] += ln.amount_tax
            if ln.rounding:
                kk = (0.0, None)
                if kk not in summary_amounts:
                    summary_amounts[kk] = {"amt": 0.0, "tax": 0.0}
                summary_amounts[kk]["amt"] -= ln.amount_untaxed
        round_lines = []
        for item in summary_amounts.items():
            found_tax_line = False
            for inv_tax_line in self.tax_line_ids:
                if (
                    item[0][0] == inv_tax_line.tax_id.amount
                    and item[0][1] == inv_tax_line.tax_id.kind_id
                ):
                    found_tax_line = True
                    break
            if (
                not found_tax_line
                or round_curr(item[1]["amt"] - inv_tax_line.base)
            ):
                vals = self.load_rounding_values(
                    round_curr(item[1]["amt"] - inv_tax_line.base),
                    tax_rate=item[0][0],
                    tax_kind=item[0][1].code if item[0][1] else None)
                round_lines.append(vals)
        if round_lines:
            for inv_line in self.invoice_line_ids:
                for round_line in round_lines:
                    if (
                        not round_line.get("found")
                        and inv_line.account_id.id == round_line["account_id"]
                        and inv_line.invoice_line_tax_ids.id
                        == round_line["invoice_line_tax_ids"][0][2][0]
                        and inv_line.quantity == round_line["quantity"]
                    ):
                        inv_line.write(round_line)
                        round_line["found"] = True
                        break
            for round_line in round_lines:
                if not round_line.get("found"):
                    round_line["sequence"] = 997
                    round_line["invoice_id"] = self.id
                    inv_line.create(round_line)
                    round_line["found"] = True
            self.compute_taxes()
            force_round_total = True
        if (
            (force_round_total and not float_is_zero(
                (self.e_invoice_amount_total - self.amount_total),
                precision_rounding=rounding))
            or self.float_diff_in_range(self.e_invoice_amount_total, self.amount_total)
        ):
            vals = self.load_rounding_values(
                round_curr(self.e_invoice_amount_total - self.amount_total))
            for inv_line in self.invoice_line_ids:
                if (
                        inv_line.account_id.id == vals["account_id"]
                        and inv_line.invoice_line_tax_ids.id
                        == vals["invoice_line_tax_ids"][0][2][0]
                        and inv_line.quantity == vals["quantity"]
                ):
                    inv_line.write(vals)
                    vals["found"] = True
                    break
            if not vals.get("found"):
                vals["sequence"] = 998
                vals["invoice_id"] = self.id
                inv_line.create(vals)
                vals["found"] = True
            self.compute_taxes()

    @api.model
    def invoice_line_move_line_get(self):
        """Append global rounding move lines"""
        res = super(AccountInvoice, self).invoice_line_move_line_get()

        if not float_is_zero(self.efatt_rounding,
                             precision_rounding=self.currency_id.rounding):
            if self.efatt_rounding > 0:
                arrotondamenti_account_id = (
                    self.env.user.company_id.arrotondamenti_passivi_account_id
                )
                if not arrotondamenti_account_id:  # pragma: no cover
                    raise UserError(
                        _("Round down account is not set " "in Accounting Settings")
                    )
                name = _("Rounding down")
            else:
                arrotondamenti_account_id = (
                    self.env.user.company_id.arrotondamenti_attivi_account_id
                )
                if not arrotondamenti_account_id:  # pragma: no cover
                    raise UserError(
                        _("Round up account is not set " "in Accounting Settings")
                    )
                name = _("Rounding up")

            res.append(
                {
                    "type": "global_rounding",
                    "name": name,
                    "price_unit": self.efatt_rounding,
                    "quantity": 1,
                    "price": self.efatt_rounding,
                    "account_id": arrotondamenti_account_id.id,
                    "invoice_id": self.id,
                }
            )
        return res

    def _fatturapa_set_invoice_date(self):
        pass

    @api.multi
    def action_invoice_draft(self):
        res = super(AccountInvoice, self).action_invoice_draft()
        self._fatturapa_set_invoice_date()
        return res

    @api.multi
    def invoice_validate(self):
        for invoice in self:
            invoice._compute_einvoice_amounts()
            invoice._compute_e_invoice_validation_error()
            if (
                invoice.e_invoice_validation_error
                and not invoice.e_invoice_force_validation
            ):
                raise ValidationError(
                    _("The invoice '%s' doesn't match the related e-invoice")
                    % invoice.display_name
                )
        return super(AccountInvoice, self).invoice_validate()

    def e_inv_check_amount_untaxed(self):
        error_message = ""
        rounding = self.currency_id.rounding
        round_curr = self.currency_id.round
        if (
            not float_is_zero(
                round_curr(self.e_invoice_amount_untaxed - self.amount_untaxed),
                precision_rounding=rounding)
            and not float_is_zero(
                round_curr(self.e_invoice_amount_untaxed
                           - self.amount_untaxed
                           - self.efatt_xml_rounding),
                precision_rounding=rounding)
        ):
            error_message = _(
                "Untaxed amount ({bill_amount_untaxed}) "
                "does not match with "
                "e-bill untaxed amount ({e_bill_amount_untaxed})"
            ).format(
                bill_amount_untaxed=self.amount_untaxed,
                e_bill_amount_untaxed=self.e_invoice_amount_untaxed,
            )
        return error_message

    def e_inv_check_amount_tax(self):
        error_message = ""
        rounding = self.currency_id.rounding
        round_curr = self.currency_id.round
        if not float_is_zero(
                round_curr(self.e_invoice_amount_tax - self.amount_tax),
                precision_rounding=rounding):
            error_message = _(
                "Taxed amount ({bill_amount_tax}) "
                "does not match with "
                "e-bill taxed amount ({e_bill_amount_tax})"
            ).format(
                bill_amount_tax=self.amount_tax,
                e_bill_amount_tax=self.e_invoice_amount_tax,
            )
        return error_message

    def e_inv_check_amount_total(self):
        error_message = ""
        rounding = self.currency_id.rounding
        round_curr = self.currency_id.round
        if not float_is_zero(
                round_curr(self.e_invoice_amount_total - self.amount_total),
                precision_rounding=rounding):
            error_message = _(
                "Total amount ({bill_amount_total}) "
                "does not match with "
                "e-bill total amount ({e_bill_amount_total})"
            ).format(
                bill_amount_total=self.amount_total,
                e_bill_amount_total=self.e_invoice_amount_total,
            )
        return error_message

    def e_inv_dati_ritenuta(self):
        error_message = ""
        # ftpa_withholding_type is set when DatiRitenuta is set,
        # withholding_tax is not set if no lines with Ritenuta = SI are found
        # TODO> is it to reactivate?
        # if self.ftpa_withholding_ids and not self.withholding_tax:
        #     error_message += _(
        #         "E-bill contains DatiRitenuta but no lines subjected to Ritenuta was "
        #         "found. Please manually check Withholding tax Amount\n"
        #     )
        # if (
        #     sum(self.ftpa_withholding_ids.mapped("amount"))
        #     != self.withholding_tax_amount
        # ):
        #     error_message += _(
        #         "E-bill contains ImportoRitenuta %s but created invoice has got"
        #         " %s\n"
        #         % (
        #             sum(self.ftpa_withholding_ids.mapped("amount")),
        #             self.withholding_tax_amount,
        #         )
        #     )
        return error_message

    @api.depends(
        "type",
        "state",
        "fatturapa_attachment_in_id",
        "amount_untaxed",
        "amount_tax",
        "amount_total",
        "reference",
        "date_invoice",
    )
    def _compute_e_invoice_validation_error(self):
        bills_to_check = self.filtered(
            lambda inv: inv.type in ["in_invoice", "in_refund"]
            and inv.state in ["draft", "open", "paid"]
            and inv.fatturapa_attachment_in_id
        )
        for bill in bills_to_check:
            error_messages = list()

            error_message = bill.e_inv_check_amount_untaxed()
            if error_message:
                error_messages.append(error_message)

            error_message = bill.e_inv_check_amount_tax()
            if error_message:
                error_messages.append(error_message)

            error_message = bill.e_inv_check_amount_total()
            if error_message:
                error_messages.append(error_message)

            error_message = bill.e_inv_dati_ritenuta()
            if error_message:
                error_messages.append(error_message)

            if bill.e_invoice_reference and bill.reference != bill.e_invoice_reference:
                error_messages.append(
                    _(
                        "Vendor reference ({bill_vendor_ref}) "
                        "does not match with "
                        "e-bill vendor reference ({e_bill_vendor_ref})"
                    ).format(
                        bill_vendor_ref=bill.reference or "",
                        e_bill_vendor_ref=bill.e_invoice_reference,
                    )
                )

            if (
                bill.e_invoice_date_invoice
                and bill.e_invoice_date_invoice != bill.date_invoice
            ):
                error_messages.append(
                    _(
                        "Invoice date ({bill_date_invoice}) "
                        "does not match with "
                        "e-bill invoice date ({e_bill_date_invoice})"
                    ).format(
                        bill_date_invoice=bill.date_invoice or "",
                        e_bill_date_invoice=bill.e_invoice_date_invoice,
                    )
                )

            if not error_messages:
                continue
            bill.e_invoice_validation_error = True  # pragma: no cover
            bill.e_invoice_validation_message = ",\n".join(
                error_messages) + "."  # pragma: no cover

    @api.multi
    def name_get(self):
        result = super(AccountInvoice, self).name_get()
        res = []
        for tup in result:
            invoice = self.browse(tup[0])
            if invoice.type in ("in_invoice", "in_refund"):
                name = "%s, %s" % (tup[1], invoice.partner_id.name)
                if invoice.amount_total_signed:
                    name += ", %s %s" % (
                        invoice.amount_total_signed,
                        invoice.currency_id.symbol,
                    )
                if invoice.origin:
                    name += ", %s" % invoice.origin
                res.append((invoice.id, name))
            else:
                res.append(tup)
        return res

    @api.multi
    def remove_attachment_link(self):
        self.ensure_one()
        self.fatturapa_attachment_in_id = False
        return {"type": "ir.actions.client", "tag": "reload"}

    @api.model
    def float_from_tag(self, tag):
        return float(tag) if tag else 0.0

    @api.model
    def compute_xml_amount_untaxed(self, FatturaBody):
        amount_untaxed = 0.0
        for Riepilogo in FatturaBody.DatiBeniServizi.DatiRiepilogo:
            amount_untaxed += self.float_from_tag(Riepilogo.ImponibileImporto)
        return self.currency_id.round(amount_untaxed)

    @api.model
    def compute_xml_amount_total(self, FatturaBody, amount_untaxed, amount_tax):
        amount_total = self.float_from_tag(
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.ImportoTotaleDocumento)
        rounding = self.float_from_tag(
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento)
        return amount_total or self.currency_id.round(
            amount_untaxed + amount_tax + rounding)

    @api.model
    def compute_xml_amount_tax(self, DatiRiepilogo):
        amount_tax = 0.0
        for Riepilogo in DatiRiepilogo:
            amount_tax += self.float_from_tag(Riepilogo.Imposta)
        return self.currency_id.round(amount_tax)

    def set_einvoice_data(self, fattura):
        self.ensure_one()
        amount_untaxed = self.compute_xml_amount_untaxed(fattura)
        amount_tax = self.compute_xml_amount_tax(fattura.DatiBeniServizi.DatiRiepilogo)
        amount_total = self.compute_xml_amount_total(
            fattura, amount_untaxed, amount_tax)
        efatt_rounding = 0.0
        efatt_xml_rounding = (
            (amount_untaxed + amount_tax - amount_total)
            or self.float_from_tag(
                fattura.DatiGenerali.DatiGeneraliDocumento.Arrotondamento)
        )
        reference = fattura.DatiGenerali.DatiGeneraliDocumento.Numero
        date_invoice = fattura.DatiGenerali.DatiGeneraliDocumento.Data
        self.update({
            "e_invoice_amount_untaxed": amount_untaxed,
            "e_invoice_amount_tax": amount_tax,
            "e_invoice_amount_total": amount_total,
            "efatt_rounding": efatt_rounding,
            "efatt_xml_rounding": efatt_xml_rounding,
            "e_invoice_reference": reference,
            "e_invoice_date_invoice": date_invoice,
        })

    def set_vendor_bill_date(self, FatturaBody):
        if not self.date_invoice:
            self.update({
                'date_invoice':
                    FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data.strftime(
                        "%Y-%m-%d"),
            })
        if not self.reference:
            self.update({
                'reference':
                    FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero,
            })

    def xml_get_header_data(
        self,
        wizard,
        fatt,
        fatturapa_attachment,
        FatturaBody,
        partner_id,
    ):
        inconsistencies = ""
        company = self.env["res.company"].xml_get_company(
            fatt.FatturaElettronicaHeader.CessionarioCommittente.DatiAnagrafici,
            wizard=wizard,
        )
        partner = self.env["res.partner"].browse(partner_id)
        # currency 2.1.1.2
        currency = self.env["res.currency"].search(
            [("name", "=", FatturaBody.DatiGenerali.DatiGeneraliDocumento.Divisa)]
        )
        if not currency:
            inconsistencies = (
                "Divisa %s in fattura non valida!"
                % FatturaBody.DatiGenerali.DatiGeneraliDocumento.Divisa
            )
        # 2.1.1
        docType_id = False
        invtype = "in_invoice"
        docType = FatturaBody.DatiGenerali.DatiGeneraliDocumento.TipoDocumento
        if docType:
            docType_record = self.env["italy.ade.invoice.type"].search(
                [("code", "=", docType)]
            )
            if docType_record:
                docType_id = docType_record[0].id
            else:
                raise UserError(_("Document type %s not handled.") % docType)
            if docType == "TD04":
                invtype = "in_refund"
        # 2.1.1.11
        comment = ""
        causLst = FatturaBody.DatiGenerali.DatiGeneraliDocumento.Causale
        if causLst:
            for item in causLst:
                comment += item + "\n"
        #
        invoice_data = {
            "fiscal_document_type_id": docType_id,
            "date_invoice":
                FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data.strftime(
                    "%Y-%m-%d"),
            "reference": FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero,
            "sender": fatt.FatturaElettronicaHeader.SoggettoEmittente or False,
            "type": invtype,
            "currency_id": currency[0].id,
            # 'origin': xmlData.datiOrdineAcquisto,
            "payment_term_id": partner.property_supplier_payment_term_id.id,
            "company_id": company.id,
            "comment": comment,
            "check_total":
                FatturaBody.DatiGenerali.DatiGeneraliDocumento.ImportoTotaleDocumento,
        }
        # 2.1.1.10
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento:
            invoice_data["efatt_xml_rounding"] = self.float_from_tag(
                FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento
            )
        # 2.1.1.12
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento.Art73:
            invoice_data["art73"] = True
        # 2.1.1.5
        wt_found = None
        for Withholding in FatturaBody.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta:
            wts = self.env["withholding.tax"].search(
                [("causale_pagamento_id.code", "=", Withholding.CausalePagamento)]
            )
            if not wts:
                raise UserError(
                    _(
                        "The bill contains withholding tax with "
                        "payment reason %s, "
                        "but such a tax is not found in your system. Please "
                        "set it."
                    )
                    % Withholding.CausalePagamento
                )
            wt_found = False
            for wt in wts:
                wt_aliquota = wt.tax * wt.base
                if wt_aliquota == self.float_from_tag(
                    Withholding.AliquotaRitenuta
                ) or wt.tax == self.float_from_tag(Withholding.AliquotaRitenuta):
                    wt_found = wt
                    break
            if not wt_found:
                raise UserError(
                    _(
                        "No withholding tax found with "
                        "document payment reason %s and rate %s."
                    )
                    % (Withholding.CausalePagamento, Withholding.AliquotaRitenuta)
                )
            invoice_data["ftpa_withholding_type"] = Withholding.TipoRitenuta
        return invoice_data, company, partner, wt_found, inconsistencies

    # def xml_get_body_data(
    #     self,
    #     wizard,
    #     fatt,
    #     fatturapa_attachment,
    #     FatturaBody,
    #     partner_id,
    #     detail_level,
    #     company,
    #     wt_found,
    # ):
    #     # TODO: to complete
    #     invoice_line_model = self.env["account.invoice.line"]
    #     partner = self.env["res.partner"].browse(partner_id)
    #     invoice_lines = []
    #     e_invoice_line_ids = []
    #     e_invoice_line_ids_2 = {}
    #     credit_account = False
    #     if detail_level > "0" and partner.e_invoice_default_account_id:
    #         credit_account = partner.e_invoice_default_account_id
    #     for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
    #         if detail_level == "2":
    #             if credit_account:
    #                 credit_account_id = credit_account.id
    #             invoice_line_data = wizard._prepareInvoiceLine(
    #                 credit_account_id, line, wt_found
    #             )
    #             product = wizard.get_line_product(line, partner)
    #             if product:
    #                 invoice_line_data["product_id"] = product.id
    #                 wizard.adjust_accounting_data(product, invoice_line_data)
    #             invoice_line_id = invoice_line_model.create(invoice_line_data).id
    #             invoice_lines.append(invoice_line_id)
    #
    #         elif detail_level == "1":
    #             company_id = company.id
    #             account_tax = wizard.get_tax(company_id,
    #                                          line.AliquotaIVA, line.Natura)
    #             if account_tax not in e_invoice_line_ids_2:
    #                 e_invoice_line_ids_2[account_tax] = 0.0
    #             e_invoice_line_ids_2[account_tax] += self.float_from_tag(
    #                 line.PrezzoTotale)
    #
    #         einvoiceline = self.create_e_invoice_line(line)
    #         e_invoice_line_ids.append(einvoiceline.id)

    def process_negative_lines(self):
        self.ensure_one()
        if not self.invoice_line_ids:
            return
        # if total is negative, change lines sign, and change move type
        if self.amount_total < 0:
            if self.fiscal_document_type_id.code == "TD01":
                self.type = "in_refund"
            for line in self.invoice_line_ids:
                line.price_unit = -line.price_unit
        self.compute_taxes()


class FatturapaArticleCode(models.Model):
    # _position = ['2.2.1.3']
    _name = "fatturapa.article.code"
    _description = "E-bill Article Code"

    name = fields.Char("Code Type")
    code_val = fields.Char("Code Value")
    e_invoice_line_id = fields.Many2one(
        "einvoice.line", "Related E-bill Line", readonly=True
    )


class AccountInvoiceLine(models.Model):
    # _position = [
    #     '2.2.1.3', '2.2.1.6', '2.2.1.7',
    #     '2.2.1.8', '2.1.1.10'
    # ]
    _inherit = "account.invoice.line"

    fatturapa_attachment_in_id = fields.Many2one(
        "fatturapa.attachment.in",
        "E-bill Import File",
        readonly=True,
        related="invoice_id.fatturapa_attachment_in_id",
        copy=False,
    )


class DiscountRisePrice(models.Model):
    _inherit = "discount.rise.price"
    e_invoice_line_id = fields.Many2one(
        "einvoice.line", "Related E-bill Line", readonly=True
    )


class EInvoiceLine(models.Model):
    _name = "einvoice.line"
    _description = "E-invoice line"

    invoice_id = fields.Many2one(
        "account.invoice", "Bill", readonly=True, ondelete="cascade"
    )
    line_number = fields.Integer("Line Number", readonly=True)
    service_type = fields.Char("Sale Provision Type", readonly=True)
    cod_article_ids = fields.One2many(
        "fatturapa.article.code", "e_invoice_line_id", "Articles Code", readonly=True
    )
    name = fields.Char("Description", readonly=True)
    qty = fields.Float(
        "Quantity",
        readonly=True,
        digits=(12, 6),
    )
    uom = fields.Char("Unit of measure", readonly=True)
    period_start_date = fields.Date("Period Start Date", readonly=True)
    period_end_date = fields.Date("Period End Date", readonly=True)
    unit_price = fields.Float(
        "Unit Price",
        readonly=True,
        digits=(12, 6),
    )
    discount_rise_price_ids = fields.One2many(
        "discount.rise.price",
        "e_invoice_line_id",
        "Discount and Supplement Details",
        readonly=True,
    )
    total_price = fields.Float("Total Price", readonly=True)
    tax_amount = fields.Float("VAT Rate", readonly=True)
    wt_amount = fields.Char("Tax Withholding", readonly=True)
    tax_kind = fields.Char("Nature", readonly=True, oldname="tax_nature")
    admin_ref = fields.Char("Administration Reference", readonly=True)
    other_data_ids = fields.One2many(
        "einvoice.line.other.data",
        "e_invoice_line_id",
        string="Other Administrative Data",
        readonly=True,
    )


class EInvoiceLineOtherData(models.Model):
    _name = "einvoice.line.other.data"
    _description = "E-invoice line other data"

    e_invoice_line_id = fields.Many2one(
        "einvoice.line", "Related E-bill Line", readonly=True
    )
    name = fields.Char("Data Type", readonly=True)
    text_ref = fields.Char("Text Reference", readonly=True)
    num_ref = fields.Float("Number Reference", readonly=True)
    date_ref = fields.Char("Date Reference", readonly=True)
