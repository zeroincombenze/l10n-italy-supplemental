# -*- coding: utf-8 -*-

from odoo import models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def action_cancel_zero(self):
        for invoice in self:
            invoice.write({"state": "open"})
        return self.action_cancel()
