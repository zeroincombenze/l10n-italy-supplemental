# -*- coding: utf-8 -*-


class SaleReport(models.Model):
    _inherit = "sale.report"

    hs_code = fields.Many2one('product.hs_code', 'HS Code', readonly=True)
