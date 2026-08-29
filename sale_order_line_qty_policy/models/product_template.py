# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from odoo import fields, models

import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    delivered_threshold = fields.Float(
        string="Delivered threshold (%)",
        digits=dp.get_precision("Discount"),
        default=0.0,
        help="Maximum accepted deviation, as a percentage of the ordered"
             " quantity, between ordered and delivered quantity.\n"
             "When the deviation of a sale order line is within this threshold,"
             " the line is declared fully delivered even if the delivered"
             " quantity does not match the ordered one.\n"
             "The deviation is evaluated on its absolute value, so both"
             " under and over delivery are covered.\n"
             "Delivered quantity is never altered: the customer is still"
             " invoiced for the quantity really delivered.\n"
             "Leave 0 to inherit the threshold declared on the product"
             " category.",
    )
    auto_line_invoiced = fields.Boolean(
        string="Auto declare invoiced",
        default=False,
        help="Sale order lines of this product are automatically declared fully"
             " invoiced, whatever the invoiced quantity is.\n"
             "Use this policy for products whose amount is evaluated again at"
             " invoice level, i.e. the environmental contribution (CONAI), so"
             " the order is not kept open waiting for an invoice which will"
             " never match the ordered quantity.",
    )
