# Copyright (c) 2020
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals_list):
        if 'tax_id' in vals_list and vals_list['tax_id'] and vals_list[
            'tax_id'][0][2]:
            how_many_tax_ids = len(vals_list['tax_id'][0][2])
            if how_many_tax_ids > 1:
                raise UserError(_(
                    "ATTENZIONE!\nImpostare un unico codice "
                    "per le imposte."))
        lines = super().create(vals_list)
        return lines

    @api.multi
    def write(self, values):
        if 'tax_id' in values and values['tax_id'] and values[
            'tax_id'][0][2]:
            how_many_tax_ids = len(values['tax_id'][0][2])
            if how_many_tax_ids > 1:
                raise UserError(_(
                    "ATTENZIONE!\nImpostare un unico codice "
                    "per le imposte."))
        result = super(SaleOrderLine, self).write(values)
        return result
