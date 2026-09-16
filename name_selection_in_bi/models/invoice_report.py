# -*- coding: utf-8 -*-
#
# Copyright 2026 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    line_name = fields.Char(string="Line Description", readonly=True)

    def _select(self):
        return (
            super(AccountInvoiceReport, self)._select()
            + ",sub.line_name as line_name"
        )

    def _sub_select(self):
        return (
            super(AccountInvoiceReport, self)._sub_select()
            + ",ail.name as line_name"
        )

    def _group_by(self):
        return (
            super(AccountInvoiceReport, self)._group_by()
            + ",ail.name"
        )
