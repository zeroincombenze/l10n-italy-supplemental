# -*- coding: utf-8 -*-
#
# Copyright 2018-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import api, fields, models


class ItalyAdeTaxNature(models.Model):
    _name = "italy.ade.tax.nature"
    _description = "Tax Italian Nature"

    _sql_constraints = [("code", "unique(code)", "Code already exists!")]

    code = fields.Char(string="Code", size=4, required=True)
    name = fields.Char(string="Name", required=True)
    help = fields.Text(string="Help")
    active = fields.Boolean(string="Active", default=True)

    @api.multi
    def name_get(self):
        res = []
        for tax_kind in self:
            res.append((tax_kind.id, "[%s] %s" % (tax_kind.code, tax_kind.name)))
        return res

    @api.model
    def name_search(self, name="", args=[], operator="ilike", limit=100):
        if name:
            records = self.search(
                ["|", ("name", operator, name), ("code", operator, name)] + args,
                limit=limit,
            )
        else:
            records = self.search(args, limit=limit)
        return records.name_get()
