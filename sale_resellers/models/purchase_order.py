# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    end_user_id = fields.Many2one(
        'res.partner', string='End user')
    reseller_id = fields.Many2one(
        'res.partner', string='Reseller')
    ref_user_id = fields.Many2one(
        'res.partner', string='Reference user')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.depends('product_qty', 'price_unit')
    def _compute_net_price(self):
        for line in self:
            if line.product_qty:
                unit_net_price = line.price_subtotal / line.product_qty
            else:
                unit_net_price = line.price_subtotal
            line.update({
                'unit_net_price': unit_net_price
            })

    unit_net_price = fields.Monetary(compute='_compute_net_price',
                                     string='Unit Net Price',
                                     store=True)
