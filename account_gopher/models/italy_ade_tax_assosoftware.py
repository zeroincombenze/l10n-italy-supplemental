#
# Copyright 2020-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from odoo import fields, models


class ItalyAdeTaxAssosoftware(models.Model):
    _name = "italy.ade.tax.assosoftware"
    _description = "Tax Assosoftware classification"
    _rec_names_search = ["name", "code"]

    _sql_constraints = [("code", "unique(code)", "Code already exists!")]

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Name", required=True)
    nature = fields.Char(
        string="Nature",
        help="Nature of tax code: may be taxable, out of scope, etc ...",
    )
