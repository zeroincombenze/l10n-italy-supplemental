# -*- coding: utf-8 -*-
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from decorator import decorator, getfullargspec
from odoo import api, fields, models


@getfullargspec
def no_raise(method):
    def wrap(method, self):
        result = [method(self)]
        return result
    return decorator(wrap, method)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def check_4_last(self):
        for invoice in self:
            if invoice.state in ('cancel', 'draft'):
                res = invoice.journal_id.sequence_id.unnext_by_id(
                    invoice.number)
                if res:
                    invoice.write({'move_name': False})

    @api.multi
    @no_raise
    def unlink(self):
        return super(AccountInvoice, self).unlink()
