# Copyright (c) 2020
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import api, models, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def create(self, vals_list):
        if 'taxes_id' in vals_list and vals_list['taxes_id']:
            how_many_tax_ids = len(vals_list['taxes_id'][0][2])
            if how_many_tax_ids > 1:
                raise UserError(_(
                    "ATTENZIONE!\nImpostare un unico codice "
                    "per le imposte di vendita."))
        if 'supplier_taxes_id' in vals_list and vals_list['supplier_taxes_id']:
            how_many_tax_ids = len(vals_list['supplier_taxes_id'][0][2])
            if how_many_tax_ids > 1:
                raise UserError(_(
                    "ATTENZIONE!\nImpostare un unico codice "
                    "per le imposte di vendita."))

        template = super().create(vals_list)
        return template

    @api.multi
    def write(self, vals):
        if 'taxes_id' in vals and vals['taxes_id']:
            how_many_tax_ids = len(vals['taxes_id'][0][2])
            if how_many_tax_ids > 1:
                raise UserError(_(
                    "ATTENZIONE!\nImpostare un unico codice "
                    "per le imposte di vendita."))
        if 'supplier_taxes_id' in vals and vals['supplier_taxes_id']:
            how_many_tax_ids = len(vals['supplier_taxes_id'][0][2])
            if how_many_tax_ids > 1:
                raise UserError(_(
                    "ATTENZIONE!\nImpostare un unico codice "
                    "per le imposte di acquisto."))

        res = super().write(vals)
        return res
