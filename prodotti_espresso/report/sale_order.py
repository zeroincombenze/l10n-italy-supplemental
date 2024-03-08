# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    espresso = fields.Boolean(string="Documento con prodotti espresso")

    def _select(self):
        return super(SaleReport, self)._select(
        ) + ", t.espresso"

    def _group_by(self):
        return super(SaleReport, self)._group_by() + ", t.espresso"
