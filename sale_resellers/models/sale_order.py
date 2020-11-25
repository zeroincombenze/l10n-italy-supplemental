# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    end_user_id = fields.Many2one('res.partner',
                                  related='order_line.end_user_id',
                                  string='End user')
    hs_code = fields.Char('HS Code',
                          related='order_line.hs_code',
                          readonly=True)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    end_user_id = fields.Many2one(
        'res.partner', string='End user',
        index=True)
    ref_user_id = fields.Many2one(
        'res.partner', string='Reference user')
    hs_code = fields.Char('HS Code',
                          compute='_compute_hs',
                          store=True,
                          readonly=True)

    @api.multi
    @api.depends('product_id', 'product_uom_qty', 'discount',
                 'price_unit', 'price_subtotal')
    def _compute_hs(self):
        for rec in self:
            rec.hs_code = rec.product_id.hs_code or False
