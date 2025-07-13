# -*- coding: utf-8 -*-

from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = ["purchase.order.line", "multireport.mixin"]
    _name = "purchase.order.line"
