# -*- coding: utf-8 -*-
#
# Copyright 2018-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import api, models, fields


class ItalyAdeTaxAssosoftware(models.Model):
    _name = 'italy.ade.tax.assosoftware'
    _description = 'Tax Assosoftware classification'

    _sql_constraints = [('code',
                         'unique(code)',
                         'Code already exists!')]

    code = fields.Char(string='Code', size=7, required=True)
    name = fields.Char(string='Name', required=True)
    nature = fields.Char(string='Nature',
        help='Nature of tax code: may be taxable, out of scope, etc ...')

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            records = self.search([
                '|', ('name', operator, name), ('code', operator, name)
                ] + args, limit=limit)
        else:
            records = self.search(args, limit=limit)
        return records.name_get()
