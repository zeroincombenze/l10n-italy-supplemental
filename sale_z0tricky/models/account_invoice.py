# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sale_id = fields.Many2one('sale.order', string='Add Sale Order',
        help='When selected, the associated sae order lines are added.')


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    sale_line_id = fields.Many2one('sale.order.line', 'Sale Order Line', ondelete='set null', index=True, readonly=True)
    sale_id = fields.Many2one('sale.order', related='sale_line_id.order_id', string='Sale Order', store=False, readonly=True, related_sudo=False,
        help='Associated Sale Order. Filled in automatically when a SO is chosen on the customer bill.')
