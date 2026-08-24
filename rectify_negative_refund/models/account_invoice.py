# -*- coding: utf-8 -*-

from odoo import models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def rectify_invoice(self):
        ctr = 0
        for invoice in self:
            if invoice.type.startswith("in_") and invoice.check_total < 0.0:
                self.env.cr.execute(
                    "UPDATE account_invoice"
                    " SET type='in_refund'"
                    ",check_total=%f"
                    " WHERE id=%d" % (-invoice.check_total,
                                      invoice.id)
                )
                ctr = 1
                continue

            saved_state = invoice.state
            new_invoice_type = invoice.type
            if "_invoice" in invoice.type:
                new_invoice_type = invoice.type.replace("_invoice", "_refund")
            if invoice.state == "open":
                if invoice.type.startswith("in_"):
                    saved_attachment_id = invoice.fatturapa_attachment_in_id
                    saved_fatturapa_state = invoice.fatturapa_state
                else:
                    saved_attachment_id = invoice.fatturapa_attachment_out_id
                if saved_attachment_id:
                    # We use SQL because invoice is locked
                    if invoice.type.startswith("in_"):
                        self.env.cr.execute(
                            "UPDATE account_invoice"
                            " SET fatturapa_attachment_in_id=null"
                            ",fatturapa_state=null"
                            " WHERE id=%d" % invoice.id
                        )
                    else:
                        self.env.cr.execute(
                            "UPDATE account_invoice"
                            " SET fatturapa_attachment_out_id=null"
                            " WHERE id=%d" % invoice.id
                        )
                    # Invalidate cache and reload invoice updated by SQL
                    self.invalidate_cache()
                    invoice = self.env["account.invoice"].browse(invoice.id)
                invoice.action_invoice_cancel()
                invoice.action_invoice_draft()
            if invoice.state != "draft":
                continue
            if invoice.type != new_invoice_type:
                invoice.type = new_invoice_type
            for line in invoice.invoice_line_ids:
                line.price_unit = -line.price_unit
            invoice.compute_taxes()
            ctr = 1
            if saved_state == "open":
                invoice.action_invoice_open()
                if saved_attachment_id:
                    # Avoid account check, so we force restoring via SQL
                    if invoice.type.startswith("in_"):
                        self.env.cr.execute(
                            "UPDATE account_invoice"
                            " SET fatturapa_attachment_in_id=%d"
                            ",fatturapa_state='%s'"
                            " WHERE id=%d" % (saved_attachment_id,
                                              saved_fatturapa_state,
                                              invoice.id)
                        )
                    else:
                        self.env.cr.execute(
                            "UPDATE account_invoice"
                            " SET fatturapa_attachment_out_id=%d"
                            " WHERE id=%d" % (saved_attachment_id,
                                              invoice.id)
                        )
        if ctr == 0:
            return False
