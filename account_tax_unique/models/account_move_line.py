# Copyright (c) 2020
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import models, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('tax_ids', False) and vals['tax_ids'] and \
                    vals['tax_ids'][0][2]:
                how_many_tax_code = len(vals['tax_ids'][0][2])
                if how_many_tax_code > 1:
                    raise UserError(_(
                        "ATTENZIONE!\nImpostare un unico codice "
                        "per le imposte nella riga del movimento contabile."))

        return super().create(vals_list)

    @api.multi
    def write(self, values):
        if 'tax_ids' in values and values['tax_ids'] and \
                values['tax_ids'][0][2]:
            how_many_tax_code = len(values['tax_ids'][0][2])
            if how_many_tax_code > 1:
                raise UserError(_(
                    "ATTENZIONE!\nImpostare un unico codice per le imposte "
                    "nella riga del movimento contabile."))
        return super().write(values)
