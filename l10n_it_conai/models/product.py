#
# Copyright 2019-23 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import api, fields, models

import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    conai_category_id = fields.Many2one(
        "italy.conai.product.category", string="CONAI Category"
    )
    conai_category2_id = fields.Many2one(
        "italy.conai.product.category", string="CONAI 2nd Category"
    )
    weight2 = fields.Float(
        string="CONAI 2nd Category Weight", digits=dp.get_precision("Stock Weight")
    )

    @api.multi
    @api.onchange("weight2")
    def _check_4_weight2(self):
        if self.weight2 and self.weight and self.weight2 >= self.weight:
            self.weight2 = 0.0
            return {
                "warning": {
                    "title": "Wrong weight!",
                    "message": "The 2nd weight must be lesser than %s!" % self.weight,
                }
            }


class ProductProduct(models.Model):
    _inherit = "product.product"

    conai_category_id = fields.Many2one(
        "italy.conai.product.category", string="CONAI Category"
    )
    conai_category2_id = fields.Many2one(
        "italy.conai.product.category", string="CONAI 2nd Category"
    )
    weight2 = fields.Float(
        string="CONAI 2nd Category Weight", digits=dp.get_precision("Stock Weight")
    )

    @api.multi
    @api.onchange("weight2")
    def _check_4_weight2(self):
        if self.weight2 and self.weight and self.weight2 >= self.weight:
            self.weight2 = 0.0
            return {
                "title": "Wrong weight!",
                "message": "The 2nd weight must be lesser than weight!",
            }
