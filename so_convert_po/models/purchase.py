# -*- coding: utf-8 -*-

from odoo import models, fields, api 


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # sale_order_line_ids = fields.Many2many(
    #     'sale.order.line',
    #     'sale_to_purchase_lines_rel',
    #     'purchase_order_line_id',
    #     'sale_order_line_id')
    sale_order_line_id = fields.Many2one(
        'sale.order.line',
        "Sale Order Line",
        help="Reference to Sale Order",
    )
    sale_order_id = fields.Many2one('sale.order',
                                    related='sale_order_line_id.order_id',
                                    string='Sale Order')
