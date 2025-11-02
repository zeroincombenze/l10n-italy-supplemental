# -*- coding: utf-8 -*-
#
# Copyright 2018-19 - Odoo Italia Associazione <https://www.odoo-italia.org>
# Copyright 2018-19 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
# import odoo.addons.decimal_precision as dp
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_attachment_out_id = fields.Many2one(
        "fatturapa.attachment.in",
        "E-invoice Import File",
        ondelete="restrict",
        copy=False,
    )
    inconsistencies = fields.Text("Import Inconsistencies", copy=False)
    e_invoice_line_ids = fields.One2many(
        "einvoice.line", "invoice_id", string="Lines Detail", readonly=True, copy=False
    )

    @api.multi
    def name_get(self):
        result = super(AccountInvoice, self).name_get()
        res = []
        for tup in result:
            invoice = self.browse(tup[0])
            if invoice.type in ("out_invoice", "out_refund"):
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
        self.fatturapa_attachment_out_id = False
        return {"type": "ir.actions.client", "tag": "reload"}

    def xml_get_header_data(
        self,
        wizard,
        fatt,
        fatturapa_attachment,
        FatturaBody,
        partner_id,
    ):
        inconsistencies = ""
        company = False
        partner = self.env["res.company"].xml_get_company(
            fatt.FatturaElettronicaHeader.CessionarioCommittente.DatiAnagrafici,
            wizard=wizard,
        )
        partner_id = self.env["res.partner"].browse(partner_id)
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
        invtype = "out_invoice"
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
                invtype = "out_refund"
        # 2.1.1.11
        comment = ""
        causLst = FatturaBody.DatiGenerali.DatiGeneraliDocumento.Causale
        if causLst:
            for item in causLst:
                comment += item + "\n"
        #
        invoice_data = {
            "fiscal_document_type_id": docType_id,
            "date_invoice": FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data.strftime(
                "%Y-%m-%d"
            ),
            "reference": FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero,
            "sender": fatt.FatturaElettronicaHeader.SoggettoEmittente or False,
            "type": invtype,
            "currency_id": currency[0].id,
            # 'origin': xmlData.datiOrdineAcquisto,
            "payment_term_id": partner.property_supplier_payment_term_id.id,
            "company_id": self.user.company_id.id,
            "comment": comment,
            "check_total": FatturaBody.DatiGenerali.DatiGeneraliDocumento.ImportoTotaleDocumento,
        }
        # 2.1.1.10
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento:
            invoice_data["efatt_rounding"] = float(
                FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento
            )
        # 2.1.1.12
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento.Art73:
            invoice_data["art73"] = True
        # 2.1.1.5
        Withholding = FatturaBody.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta
        wt_found = None
        if Withholding:
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
                if wt_aliquota == float(
                    Withholding.AliquotaRitenuta
                ) or wt.tax == float(Withholding.AliquotaRitenuta):
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

    def xml_get_body_data(
        self,
        wizard,
        fatt,
        fatturapa_attachment,
        FatturaBody,
        partner_id,
        detail_level,
        company,
        wt_found,
    ):
        # TODO: to complete
        invoice_line_model = self.env["account.invoice.line"]
        partner = self.env["res.partner"].browse(partner_id)
        invoice_lines = []
        e_invoice_line_ids = []
        e_invoice_line_ids_2 = {}
        credit_account = False
        if detail_level > "0" and partner.e_invoice_default_account_id:
            credit_account = partner.e_invoice_default_account_id
        for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
            if detail_level == "2":
                if credit_account:
                    credit_account_id = credit_account.id
                invoice_line_data = wizard._prepareInvoiceLine(
                    credit_account_id, line, wt_found
                )
                product = wizard.get_line_product(line, partner)
                if product:
                    invoice_line_data["product_id"] = product.id
                    wizard.adjust_accounting_data(product, invoice_line_data)
                invoice_line_id = invoice_line_model.create(invoice_line_data).id
                invoice_lines.append(invoice_line_id)

            elif detail_level == "1":
                company_id = company.id
                account_tax = wizard.get_tax(company_id, line.AliquotaIVA, line.Natura)
                if account_tax not in e_invoice_line_ids_2:
                    e_invoice_line_ids_2[account_tax] = float(0)
                e_invoice_line_ids_2[account_tax] += float(line.PrezzoTotale)

            einvoiceline = self.create_e_invoice_line(line)
            e_invoice_line_ids.append(einvoiceline.id)


class fatturapa_article_code(models.Model):
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

    fatturapa_attachment_out_id = fields.Many2one(
        "fatturapa.attachment.in",
        "E-bill Import File",
        readonly=True,
        related="invoice_id.fatturapa_attachment_out_id",
        copy=False,
    )


class DiscountRisePrice(models.Model):
    _inherit = "discount.rise.price"
    e_invoice_line_id = fields.Many2one(
        "einvoice.line", "Related E-bill Line", readonly=True
    )


class EInvoiceLine(models.Model):
    _name = "einvoice.line"
    invoice_id = fields.Many2one("account.invoice", "Bill", readonly=True)
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

    e_invoice_line_id = fields.Many2one(
        "einvoice.line", "Related E-bill Line", readonly=True
    )
    name = fields.Char("Data Type", readonly=True)
    text_ref = fields.Char("Text Reference", readonly=True)
    num_ref = fields.Float("Number Reference", readonly=True)
    date_ref = fields.Char("Date Reference", readonly=True)
