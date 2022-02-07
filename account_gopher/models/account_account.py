# -*- coding: utf-8 -*-
#
# Copyright 2020-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from odoo import models, fields, _


class AccountAccount(models.Model):
    _inherit = 'account.account'

    def gopher_reload_coa(self, html_txt=None):
        """Reaload account records from account.tax.template"""

        def get_tmpl_values(tmpl, rec=None):
            vals = {}
            for name in ('code', 'name', 'reconcile'):
                if not rec or getattr(rec, name) != getattr(tmpl, name):
                    vals[name] = getattr(tmpl, name)
            for name in ('user_type_id', 'group_id'):
                if not rec or getattr(rec, name) != getattr(tmpl, name):
                    vals[name] = getattr(tmpl, name).id
            return vals

        html = ''
        if html_txt:
            html += html_txt(_('Reload Chart of Account'), 'h3')
            html += html_txt('', 'table')
            html += html_txt('', 'tr')
            html += html_txt(_('Code'), 'td')
            html += html_txt(_('Name'), 'td')
            html += html_txt(_('Action'), 'td')
            html += html_txt('', '/tr')
        template_model = self.env['account.account.template']
        acc_model = self.env['account.account']
        company = self.env.user.company_id
        for tmpl in template_model.search([]):
            acc = acc_model.search(
                [('code', '=', tmpl.code),
                 ('company_id', '=', company.id)])
            actioned = ''
            if len(acc) == 1:
                vals = get_tmpl_values(tmpl, rec=acc)
                if vals:
                    try:
                        acc[0].write(vals)
                        actioned = _('Updated')
                    except BaseException as e:
                        actioned = '** %s **' % e
            elif not acc:
                try:
                    acc_model.create(get_tmpl_values(tmpl))
                    actioned = _('New record created')
                except BaseException as e:
                    actioned = '** %s **' % e
            if html_txt and actioned:
                html += html_txt('', 'tr')
                html += html_txt(tmpl.code, 'td')
                html += html_txt(tmpl.name, 'td')
                html += html_txt(actioned, 'td')
                html += html_txt('', '/tr')
        if html_txt:
            html += html_txt('', '/table')
        return html
