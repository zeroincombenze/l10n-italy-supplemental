# -*- coding: utf-8 -*-
# Copyright 2019 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class EU_accountConfigureWizard(models.TransientModel):
    """No yed documented"""
    _name = 'eu_account.configure.wizard'

    @api.multi
    def configure_eu_account(self):
        pass
        return {'type': 'ir.actions.act_window_close'}