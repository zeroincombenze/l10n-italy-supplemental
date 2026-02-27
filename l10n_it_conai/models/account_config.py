# -*- coding: utf-8 -*-
#
# Copyright 2021-23 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = "account.config.settings"

    conai_product_id = fields.Many2one(
        related="company_id.conai_product_id",
        help="CONAI product",
        domain=[("type", "=", "service")],
    )


class ResCompany(models.Model):
    _inherit = "res.company"

    conai_product_id = fields.Many2one("product.product", string="CONAI product")
