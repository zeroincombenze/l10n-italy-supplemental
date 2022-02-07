# -*- coding: utf-8 -*-
#
# Copyright 2020-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#

from odoo import api, fields, models, _


class GopherConfigureWizard(models.TransientModel):
    """No yet documented"""
    _name = 'gopher.configure.wizard'
    _description = "Configure Account Environment"

    @api.model
    def _selection_profile(self):
        res = [('ord', _('Ordinary Account')),
               ('cash', _('Tax Cash Basis')),
               ('adv', _('Advisor'))]
        return res

    account_profile = fields.Selection(
        lambda self: self._selection_profile(),
        'Select account profile',
        default='ord',
        required=True)
    reload_from_coa = fields.Selection(
        [
            ('tax', 'Tax codes'),
            ('coa', 'Chart of Account'),
            ('both', 'Tax & CoA codes'),
        ],
        'Reload CoA and Tax codes')
    tracelog = fields.Html('Result History')

    @api.multi
    def html_txt(self, text, tag):
        if tag:
            if tag in ('table', '/table', 'tr', '/tr'):
                if not text and tag == 'table':
                    text = 'border="2px" cellpadding="2px" style="padding: 5px"'
                if text:
                    html = '<%s %s>' % (tag, text)
                elif tag.startswith('/'):
                    html = '<%s>\n' % tag
                else:
                    html = '<%s>' % tag
            else:
                html = '<%s>%s</%s>' % (tag, text, tag)
        else:
            html = text
        return html

    @api.multi
    def account_wizard(self):
        self.tracelog = '%s\n%s' % (
            self.html_txt(_('Result'), 'h2'),
            self.env['account.tax'].gopher_configure_tax(
                html_txt=self.html_txt)
        )
        return {
            'name': 'Configuration result',
            'type': 'ir.actions.act_window',
            'res_model': 'gopher.configure.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {'active_id': self.id},
            'view_id': self.env.ref(
                'account_gopher.result_wizard_configure_view').id,
            'domain': [('id', '=', self.id)],
        }

    def close_window(self):
        return {'type': 'ir.actions.act_window_close'}
