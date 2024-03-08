# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    espresso = fields.Boolean(string="Documento con prodotti espresso")

    def _select(self):
        return super(AccountInvoiceReport, self)._select(
        ) + ", sub.espresso"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select(
        ) + ",pt.espresso"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ", pt.espresso"
