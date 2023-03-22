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


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('invoice_line_tax_ids', False):
                how_many_tax_code = len(vals['invoice_line_tax_ids'][0][2])
                if how_many_tax_code > 1:
                    raise UserError(_(
                        "ATTENZIONE!\nImpostare un unico codice "
                        "per le imposte."))

        return super(AccountInvoiceLine, self).create(vals_list)

    @api.multi
    def write(self, values):
        if 'invoice_line_tax_ids' in values:
            how_many_tax_code = len(values['invoice_line_tax_ids'][0][2])
            if how_many_tax_code > 1:
                raise UserError(_(
                    "ATTENZIONE!\nImpostare un unico codice per le imposte."))
        return super(AccountInvoiceLine, self).write(values)
