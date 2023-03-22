# Copyright (c) 2020
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class WizardConfirmZeroAmount(models.TransientModel):
    _name = 'wizard.confirm.zero.amount'

    yes_no = fields.Char(default='Premere si per confermare?')

    @api.multi
    def invoice_confirm(self):
        active_id = self._context.get('active_id')
        domain = [('id', '=', active_id)]
        invoice_model = self.env['account.invoice'].search(domain)
        invalid = invoice_model.action_invoice_open()
        if invalid is None:
            return {'type': 'ir.actions.act_window_close'}
        return False
