# Copyright (c) 2021
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        if 'vat' in vals and vals['vat']:
            if 'company_type' in vals and vals['company_type'] == 'company':
                vals['vat'] = self._capitalize_first_n_second(vals['vat'])
        # enf if

        return super().create(vals)
    # end create

    @api.multi
    def write(self, vals):
        if 'vat' in vals and vals['vat']:
            vals['vat'] = self._capitalize_first_n_second(vals['vat'])
        # end if
        return super().write(vals)
    # end write

    @api.onchange('vat')
    def onchange_vat(self):
        res = {}
        if self.vat and self.company_type:
            if self.company_type == 'company':
                self.vat = self._capitalize_first_n_second(self.vat)
            # end if
        # end if
        if self.vat:
            ids = self.search([('vat', 'ilike', self.vat),
                               ('is_company', '=', True)])
            if ids:
                name = self.browse(ids[0].id).name
                res['warning'] = {
                    'title': 'Attenzione!',
                    'message': 'Esiste un altro nominativo con partita iva: %s'
                               % name
                }
            # end if
        # end if
        return res
    # end onchange_vat

    @staticmethod
    def _capitalize_first_n_second(s):
        if s and len(s) > 2:
            first_n_second = s[:2].upper()
            tail = s[2:]
            return first_n_second + tail
        else:
            return s
        # end if
    # end _capitalize_first_n_second
