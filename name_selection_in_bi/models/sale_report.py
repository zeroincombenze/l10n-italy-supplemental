# -*- coding: utf-8 -*-
#
# Copyright 2026 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    line_name = fields.Char(string="Line Description", readonly=True)

    def _select(self):
        return super(SaleReport, self)._select() + ",l.name as line_name"

    def _group_by(self):
        # Lines of the same order and product are no more merged in one row
        # when they carry a different description
        return super(SaleReport, self)._group_by() + ",l.name"
