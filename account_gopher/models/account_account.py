#
# Copyright 2020-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from python_plus import _u
from odoo import models, fields, _


class AccountAccount(models.Model):
    _inherit = 'account.account'

    def gopher_reload_coa(self, html_txt=None):
        """Reaload account records from account.account.template"""

        def get_tmpl_values(tmpl, rec=None):
            company_id = self.env.user.company_id.id
            vals = {}
            if not rec:
                vals['company_id'] = company_id
            name = 'name'
            if (not rec or (rec.code.endswith('0') and
                            getattr(rec, name) != getattr(tmpl, name))):
                vals[name] = getattr(tmpl, name)
            for name in ('code', 'reconcile'):
                if not rec or getattr(rec, name) != getattr(tmpl, name):
                    vals[name] = getattr(tmpl, name)
            for name in ('user_type_id', 'group_id'):
                if not rec or getattr(rec, name) != getattr(tmpl, name):
                    vals[name] = getattr(tmpl, name).id
            name = 'nature'
            if hasattr(tmpl.user_type_id, name):
                if not rec or getattr(rec, name) != getattr(tmpl.user_type_id,
                                                            name):
                    vals[name] = getattr(tmpl.user_type_id, name)
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
        chart_template_id = company.chart_template_id
        for tmpl in template_model.search(
                [('chart_template_id', '=', chart_template_id.id)]):
            acc = acc_model.search(
                [('code', '=', tmpl.code), ('company_id', '=', company.id)]
            )
            actioned = ''
            if len(acc) == 1:
                vals = get_tmpl_values(tmpl, rec=acc)
                if vals:
                    try:
                        acc[0].write(vals)
                        actioned = _('Updated')
                        self._cr.commit()  # pylint: disable=invalid-commit
                    except BaseException as e:
                        self._cr.rollback()  # pylint: disable=invalid-commit
                        actioned = _u('** %s **' % e)
            elif not acc:
                try:
                    acc_model.create(get_tmpl_values(tmpl))
                    actioned = _('New record created')
                    self._cr.commit()  # pylint: disable=invalid-commit
                except BaseException as e:
                    self._cr.rollback()  # pylint: disable=invalid-commit
                    actioned = _u('** %s **' % e)
            if html_txt and actioned:
                html += html_txt('', 'tr')
                html += html_txt(tmpl.code, 'td')
                html += html_txt(tmpl.name, 'td')
                html += html_txt(actioned, 'td')
                html += html_txt('', '/tr')
        if html_txt:
            html += html_txt('', '/table')
        return html
