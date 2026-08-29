# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from odoo import fields, models

import odoo.addons.decimal_precision as dp


class ProductCategory(models.Model):
    _inherit = "product.category"

    delivered_threshold = fields.Float(
        string="Delivered threshold (%)",
        digits=dp.get_precision("Discount"),
        default=0.0,
        help="Default delivered threshold for every product of this category."
             "\nIt is used when the product itself does not declare its own"
             " threshold.\n"
             "Set 0 to disable this policy for the whole category.",
    )
