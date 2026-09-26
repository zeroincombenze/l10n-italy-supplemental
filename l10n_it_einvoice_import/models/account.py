# -*- coding: utf-8 -*-
#
# Copyright 2018-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import api, models, _
from odoo.exceptions import UserError

# TipoDocumento codes of a document issued by the seller which is a credit note
SALE_REFUND_DOCTYPES = ("TD04", "TD08")
# TipoDocumento codes of self billing: the company is the buyer but issues the
# document. Header roles are swapped: see xml_get_header_data_sale()
SELF_BILLING_DOCTYPES = ("TD16", "TD17", "TD18", "TD19", "TD20", "TD21", "TD22", "TD23")


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def remove_attachment_out_link(self):
        self.ensure_one()
        self.fatturapa_attachment_out_id = False
        return {"type": "ir.actions.client", "tag": "reload"}

    def get_rounding_tax(self):
        """Rounding tax of a sale invoice, falling back to the purchase one."""
        if self.type in ("out_invoice", "out_refund"):
            company = self.env.user.company_id
            if company.arrotondamenti_tax_sale_id:
                return company.arrotondamenti_tax_sale_id
        return super(AccountInvoice, self).get_rounding_tax()

    @api.model
    def is_self_billing(self, FatturaBody):
        docType = FatturaBody.DatiGenerali.DatiGeneraliDocumento.TipoDocumento
        return docType in SELF_BILLING_DOCTYPES

    def xml_get_header_data_sale(
        self,
        wizard,
        fatt,
        fatturapa_attachment,
        FatturaBody,
        partner_id,
    ):
        """Header data of a customer invoice read from the xml file.

        Mirrors account.invoice.xml_get_header_data() of l10n_it_einvoice_in:
        there the company is the CessionarioCommittente (we receive the bill),
        here it is the CedentePrestatore (we issue the invoice).
        """
        inconsistencies = ""
        header = fatt.FatturaElettronicaHeader
        company = self.env["res.company"].xml_get_company(
            header.CedentePrestatore.DatiAnagrafici, wizard=wizard
        )
        partner = self.env["res.partner"].browse(partner_id)
        # 2.1.1.2
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
            if docType in SALE_REFUND_DOCTYPES:
                invtype = "out_refund"
        # 2.1.1.11
        comment = ""
        causLst = FatturaBody.DatiGenerali.DatiGeneraliDocumento.Causale
        if causLst:
            for item in causLst:
                comment += item + "\n"
        invoice_data = {
            "fiscal_document_type_id": docType_id,
            "date_invoice":
                FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data.strftime(
                    "%Y-%m-%d"),
            "reference": FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero,
            # The invoice already exists at SdI under this very number, so it
            # must not be renumbered by the sale journal sequence:
            # account_invoice_force_number exposes move_name as "Force Number"
            # and account.move.post() uses it instead of the sequence.
            "move_name": FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero,
            "sender": header.SoggettoEmittente or False,
            "type": invtype,
            "currency_id": currency[0].id,
            "payment_term_id": partner.property_payment_term_id.id,
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
        wt_found = self.xml_get_withholding(FatturaBody, invoice_data)
        return invoice_data, company, partner, wt_found, inconsistencies

    def xml_get_withholding(self, FatturaBody, invoice_data):
        """Withholding tax of the document, if any. Same rules of purchase."""
        wt_found = None
        for Withholding in FatturaBody.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta:
            wts = self.env["withholding.tax"].search(
                [("causale_pagamento_id.code", "=", Withholding.CausalePagamento)]
            )
            if not wts:
                raise UserError(
                    _(
                        "The invoice contains withholding tax with "
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
        return wt_found
