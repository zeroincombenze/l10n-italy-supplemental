# -*- coding: utf-8 -*-
from odoo import api, models
# from odoo.exceptions import UserError


class Invoice(models.Model):
    _inherit = "account.invoice"

    def generate_self_invoice(self):
        res = super(Invoice, self).generate_self_invoice()
        is_rc = False
        if self.rc_self_invoice_id:
            if self.fiscal_position_id.rc_type == "self":
                self.rc_self_invoice_id.fiscal_document_type_id = (
                    self.fiscal_position_id.fiscal_document_type_id.id
                )
                is_rc = True
            else:
                # Old deprecated style
                rc_type = self.fiscal_position_id.rc_type_id
                if rc_type.fiscal_document_type_id:
                    self.rc_self_invoice_id.fiscal_document_type_id = (
                        rc_type.fiscal_document_type_id.id
                    )
                    is_rc = True
        if is_rc:
            if self.fatturapa_attachment_in_id:
                doc_id = self.fatturapa_attachment_in_id.name
            else:
                doc_id = self.reference if self.reference else self.number
            self.rc_self_invoice_id.related_documents = [
                (0, 0, {
                    "type": "invoice",
                    "name": doc_id,
                    "date": self.date_invoice,
                })
            ]
        return res

    @api.multi
    def _get_original_suppliers(self):
        rc_purchase_invoices = self.mapped("rc_purchase_invoice_id")
        supplier_invoices = self.env["account.invoice"]
        for rc_purchase_invoice in rc_purchase_invoices:
            current_supplier_invoices = self.search(
                [("rc_self_purchase_invoice_id", "=", rc_purchase_invoice.id)]
            )
            if current_supplier_invoices:
                supplier_invoices |= current_supplier_invoices
            else:
                supplier_invoices |= rc_purchase_invoice
        return supplier_invoices.mapped("partner_id")
