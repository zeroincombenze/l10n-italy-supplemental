# Copyright 2021-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    amount_net_pay = fields.Float(string='Net to pay',
                                  store=True,
                                  digits=dp.get_precision('Account'),
                                  compute='_compute_net_pay')

    @api.depends('amount_total')
    def _compute_net_pay(self):
        for inv in self:
            inv.amount_net_pay = inv.amount_total
    # and _compute_net_pay

    @api.multi
    def action_invoice_draft(self):
        res = True
        for invoice in self:
            saved_date = invoice.date
            res = super(AccountInvoice, invoice).action_invoice_draft() and res
            if saved_date and invoice.journal_id.type == 'purchase':
                invoice.date = saved_date
        return res
