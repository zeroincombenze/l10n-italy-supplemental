#
# Copyright 2019-23 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import fields, models

import odoo.addons.decimal_precision as dp


class ItalyConaiPartnerCategory(models.Model):
    _name = "italy.conai.partner.category"
    _description = "CONAI partner category"

    _sql_constraints = [("code", "unique(code)", "Code already exists!")]

    code = fields.Char(string="Code", size=64, required=True, help="Category code")
    name = fields.Char(string="Name", required=True)
    conai_percent = fields.Float(
        string="Exemption percent",
        digits=dp.get_precision("Product Price"),
        default=100.0,
    )
    sector = fields.Selection(
        [
            ("producer", "Producer"),
            ("user", "User"),
            ("excluded", "Excluded"),
        ],
        string="Type",
        required=True,
        default="user",
    )
    active = fields.Boolean(string="Active", default=True)
