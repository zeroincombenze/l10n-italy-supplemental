# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    area_id = fields.Many2one(
        "res.partner.area",
        "Area",
        related="partner_id.area_id",
        store=True,
    )
