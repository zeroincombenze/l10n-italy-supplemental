# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    end_user_id = fields.Many2one('res.partner',
                                  related='order_line.end_user_id',
                                  string='End user')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    end_user_id = fields.Many2one(
        'res.partner', string='End user',
        index=True)
    ref_user_id = fields.Many2one(
        'res.partner', string='Reference user')
    # assigned_reseller = fields.Many2one(
    #     'res.partner', string='Assigned Reseller',
    #     default=self.order_partner_id)
