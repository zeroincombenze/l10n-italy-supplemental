# -*- coding: utf-8 -*-
#
# Copyright 2020-21 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#

from odoo import api, fields, models


class TutorConfigureWizard(models.TransientModel):
    """No yet documented"""
    _name = 'tutor.configure.wizard'
    _description = "Configure Account Environment"

    @api.model
    def _selection_profile(self):
        res = [('ord', 'Ordinary Account'),
               ('cash', 'Tax Cash Basis'),
               ('adv', 'Advisor')]
        return res

    account_profile = fields.Selection(
        lambda self: self._selection_profile(),
        'Select account profile',
        default='ord',
        required=True)
    tracelog = fields.Html('Result History')

    @api.multi
    def account_wizard(self):
        self.tracelog = '<h2>Result</h2>'
        self.tracelog = self.env['account.tax'].tutor_configure_tax(
            log=self.tracelog)
        return {
            'name': 'Configuration result',
            'type': 'ir.actions.act_window',
            'res_model': 'tutor.configure.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {'active_id': self.id},
            'view_id': self.env.ref(
                'account_tutor.result_wizard_configure_view').id,
            'domain': [('id', '=', self.id)],
        }

    def close_window(self):
        return {'type': 'ir.actions.act_window_close'}
