# -*- coding: utf-8 -*-
#
# Copyright 2017-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# import datetime
from odoo import api, fields, models

# from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    date_apply_vat = fields.Date(
        "Apply for VAT date",
        states={
            "paid": [("readonly", True)],
            "open": [("readonly", True)],
            "close": [("readonly", True)],
        },
        help="Date to apply for VAT",
    )

    date_apply_balance = fields.Date(
        "Apply for balance date",
        states={
            "paid": [("readonly", True)],
            "open": [("readonly", True)],
            "close": [("readonly", True)],
        },
        help="Date to apply for balance sheet",
    )

    @api.multi
    def _check_4_inv_date(self):

        for invoice in self:
            # res = False
            if (
                invoice.type in ("out_invoice", "out_refund")
                and not invoice.journal_id.enable_date
            ):
                invoice.date_apply_vat = (
                    invoice.date_apply_balance
                ) = invoice.date_invoice
        return True

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        self._check_4_inv_date()
        return res
