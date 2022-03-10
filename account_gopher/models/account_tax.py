# -*- coding: utf-8 -*-
#
# Copyright 2020-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
import re
from python_plus import _u
from odoo import models, fields, _

# Zeroincombenze use "italy.ade.tax.nature", OCA "account.tax.kind" 
# NATURE_MODEL = 'account.tax.kind'
# NATURE_ID = 'kind_id'
NATURE_MODEL = 'italy.ade.tax.nature'
NATURE_ID = 'nature_id'

# Nature(text), law number(number), law supplemental(text), \
# law section(number), law letter(text), law ref (text)
# - law supplemental -> (bis|ter|quater|quinques|sexies|septies|octies|novies)
RE_ESCL = 'E[scl.]+'
RE_FC = r'(F\.?C|F[uori.]+ C[ampo.]+)( IVA )?'
RE_NSOGG = 'N[on]*[. ]+S'
RE_MIN = 'Contr[ib. ]+Min'
RE_NI = 'N[on]*[. ]+I[mp. ]+'
RE_ESE = 'Es[ente.]+'
ASSOCODES = {
    'N010100': (RE_ESCL, '15', None, None, None, None),
    'N020100': (RE_FC, '(1|17)', None, None, None, None),
    'N020101': (RE_FC, '2', None, None, None, None),
    'N020102': (RE_FC, '3', None, None, None, None),
    'N020103': (RE_FC, '4', None, None, None, None),
    'N020104': (RE_FC, '5', None, None, None, None),
    'N020201': (None, '7', 'bis', None, None, None),
    'N020202': (None, '7', 'ter', None, None, None),
    'N020203': (None, '7', 'quater', None, None, None),
    'N020204': (None, '7', 'quinquies', None, None, None),
    'N020206': (None, '7', 'sexies', None, None, None),
    'N020207': (None, '7', 'septies', None, None, None),
    'N020208': (None, '38', None, '5', None, r'D?\.?L.? *331'),
    'N020209': ('no.? res', '17', None, '3', None, None),
    'N020210': (
        None,
        '7',
        None,
        None,
        None,
        '19[- .,]*c[- .,]*3[- .,/]*l[etr.]*b',
    ),
    'N020212': (RE_NSOGG, '50', 'bis', '4', '[cehi .]+', r'D?\.?L.? *331'),
    'N020213': (None, '7', 'octies', None, None, None),
    'N020300': (RE_NSOGG, '74', None, '[12]', None, None),
    'N020400': (RE_ESCL, '13', None, None, None, None),
    'N020501': (
        RE_MIN,
        '(1|27)',
        None,
        None,
        None,
        r'(D?\.?L.? *98|L.? *244)',
    ),
    'N020502': ('Forf', '1', None, None, None, 'L.? *190'),
    'N020601': ('Var[iazione.]?', '26', None, '3', None, None),
    'N030101': (RE_NI, '8', None, '1', 'a', None),
    'N030106': (RE_NI, '8', None, '1', 'b', None),
    'N030109': (RE_NI, '8', 'bis', None, None, None),
    'N030110': (RE_NI, '9', None, '1', None, None),
    'N030111': (RE_NI, '72', None, None, None, None),
    'N030112': (RE_NI, '71', None, None, None, '(RSM|Marino)'),
    'N030113': (RE_NI, '71', None, None, None, '(SCV|Vaticano)'),
    'N030201': (
        RE_NI,
        '8',
        None,
        '1',
        'c',
        '(Let[tera.]+|Dich[iarzone]*)[ di]* Int[ento.]+',
    ),
    'N030202': (
        RE_NI,
        '8',
        '(bis)?',
        '2',
        None,
        '(Let[tera.]+|Dich[iarzone]*)[ di]* Int[ento.]+',
    ),
    'N030203': (
        RE_NI,
        '9',
        None,
        '2',
        None,
        '(Let[tera.]+|Dich[iarzone]*)[ di]* Int[ento.]+',
    ),
    'N030204': (
        RE_NI,
        '72',
        None,
        '1',
        None,
        '(Let[tera.]+|Dich[iarzone]*)[ di]* Int[ento.]+',
    ),
    'N030401': (RE_NI, '41', None, None, None, r'D?\.?L.? *331'),
    'N030501': (RE_NI, '38', 'quater', '1', None, None),
    'N040101': (RE_ESE, '10', None, None, None, None),
    'N040102': (RE_ESE, '10', None, '[123456789]', None, None),
    'N040103': (RE_ESE, '10', None, '11', None, None),
    'N040105': (RE_ESE, '10', None, '27', None, 'quinques'),
    'N050100': (
        'R[egime.]+[ di]+Marg',
        '3[67]',
        None,
        None,
        None,
        r'D?\.?L.? *41',
    ),
    'N060101': (None, '17', None, '6', 'a', 'bis'),
    'N060102': (None, '74', None, '[78]', None, None),
    'N060103': (None, '17', None, '5', None, None),
    'N060104': (None, '17', None, '6', 'a', None),
    'N060105': (None, '17', None, '6', 'b', None),
    'N060106': (None, '17', None, '6', 'c', None),
    'N060107': (None, '17', None, '6', 'a', 'ter'),
    'N060109': (None, '7', 'bis', None, None, None),
    'N060201': (None, '7', 'ter', None, None, None),
    'N060202': (None, '7', 'quater', None, None, None),
    'N060203': (None, '7', 'quinques', None, None, None),
    '*SP': (None, '17', 'ter', None, None, None),
    '*DF': (None, '32', 'bis', None, None, '83'),
    '*N6.9': (None, '17', None, 'c', None, None),
}


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def gopher_configure_tax(self, html_txt=None):
        """Set default values"""

        def search_4_tokens(
            tax_name,
            number,
            nature=None,
            bis=None,
            comma=None,
            letter=None,
            roman=None,
            law=None,
        ):
            regex = '(Oper[azione]?)?'
            if nature:
                regex += '[- (,./]?%sArt[ .]+%s' % (nature, number)
            else:
                regex += '[- (,./]?Art[ .]+%s' % number
            plus = False
            if bis:
                regex += '[- ]?%s' % bis
                plus = True
            if comma:
                regex += '[- ,.]*[nc](omma)?[- .,/]*%s' % comma
                plus = True
            if letter:
                regex += '[- ,./]*l[etr. ]*%s' % letter
                plus = True
            if roman:
                regex += '[- ,./]+%s' % roman
                plus = True
            if not plus:
                regex += '[^0-9]'
            if law:
                regex += '.*%s' % law
            if re.search(regex, tax_name, re.I):
                return True
            return False

        def set_result(tax, assosoftware, weight, res):
            res[tax]['wgt'] = weight
            if assosoftware == '*SP':
                res[tax]['axc'] = False
                res[tax]['nat'] = ''
                res[tax]['pay'] = 'S'
                res[tax]['law'] = 'IVA in split-payment - Art. 17ter'
            elif assosoftware == '*DF':
                res[tax]['axc'] = False
                res[tax]['nat'] = ''
                res[tax]['pay'] = 'D'
            elif assosoftware.startswith('*N'):
                res[tax]['axc'] = False
                res[tax]['nat'] = assosoftware[1:]
                res[tax]['pay'] = False
            else:
                assosoftware_rec = assosoftware_model.search(
                    [('code', '=', assosoftware)]
                )
                res[tax]['axc'] = assosoftware
                res[tax]['nat'] = assosoftware_rec.nature
                res[tax]['pay'] = False
                res[tax]['law'] = assosoftware_rec.name

        tax_model = self.env['account.tax']
        nature_model = self.env[NATURE_MODEL]
        assosoftware_model = self.env['italy.ade.tax.assosoftware']
        # company_model = self.env['res.company']
        html = ''
        if html_txt:
            html += html_txt(_('Analyzing Taxes'), 'h3')
            html += html_txt('', 'table')
            html += html_txt('', 'tr')
            html += html_txt(_('Code'), 'td')
            html += html_txt(_('Name'), 'td')
            html += html_txt(_('Action'), 'td')
            html += html_txt('', '/tr')
        cur_company_id = False
        cur_company_pay = False
        res = {}
        parsed = []
        for tax in tax_model.search([]):
            parsed.append(tax)
            if tax.company_id.id != cur_company_id:
                cur_company_pay = 'I'
                try:
                    self.env.cr.execute(
                        """select f.code from
                        res_company c,fatturapa_fiscal_position f
                        where c.fatturapa_fiscal_position_id=f.id and
                        c.id=%d"""
                        % tax.company_id.id
                    )
                    code = self.cr.fetchone()[0]
                    if code in ('RF16', 'RF17'):
                        cur_company_pay = 'D'
                except:
                    pass
                cur_company_id = tax.company_id.id
            res[tax] = {
                'wgt': 0,
                'nat': '',
                'pay': cur_company_pay if tax.type_tax_use == 'sale' else 'I',
                'amt': tax.amount,
                'des': tax,
                'nme': tax.name,
            }
            for assosoftware in ASSOCODES.keys():
                if search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    nature=ASSOCODES[assosoftware][0],
                    bis=ASSOCODES[assosoftware][2],
                    comma=ASSOCODES[assosoftware][3],
                    letter=ASSOCODES[assosoftware][4],
                    law=ASSOCODES[assosoftware][5],
                ):
                    # Full match
                    weight = 4 + len(
                        [x for x in ASSOCODES[assosoftware] if x is not None]
                    )
                    if weight < res[tax]['wgt']:
                        continue
                    set_result(tax, assosoftware, weight, res)
                elif search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    bis=ASSOCODES[assosoftware][2],
                    comma=ASSOCODES[assosoftware][3],
                    letter=ASSOCODES[assosoftware][4],
                    law=ASSOCODES[assosoftware][5],
                ):
                    # match w/o nature
                    weight = 3 + len(
                        [x for x in ASSOCODES[assosoftware] if x is not None]
                    )
                    if weight <= res[tax]['wgt']:
                        continue
                    set_result(tax, assosoftware, weight, res)
                elif search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    nature=ASSOCODES[assosoftware][0],
                    comma=ASSOCODES[assosoftware][3],
                    letter=ASSOCODES[assosoftware][4],
                    law=ASSOCODES[assosoftware][5],
                ):
                    # match w/o supplemental (bis/ter/...)
                    weight = 3 + len(
                        [x for x in ASSOCODES[assosoftware] if x is not None]
                    )
                    if weight <= res[tax]['wgt']:
                        continue
                    set_result(tax, assosoftware, weight, res)
                elif search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    nature=ASSOCODES[assosoftware][0],
                    bis=ASSOCODES[assosoftware][2],
                    comma=ASSOCODES[assosoftware][3],
                    letter=ASSOCODES[assosoftware][4],
                ):
                    # Match w/o law reference
                    weight = 2 + len(
                        [x for x in ASSOCODES[assosoftware] if x is not None]
                    )
                    if weight <= res[tax]['wgt']:
                        continue
                    set_result(tax, assosoftware, weight, res)
                elif search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    nature=ASSOCODES[assosoftware][0],
                    bis=ASSOCODES[assosoftware][2],
                    comma=ASSOCODES[assosoftware][3],
                ):
                    # Match w/o law ref neither law letter
                    weight = 2 + len(
                        [x for x in ASSOCODES[assosoftware] if x is not None]
                    )
                    if weight <= res[tax]['wgt']:
                        continue
                    set_result(tax, assosoftware, weight, res)
                elif search_4_tokens(
                    tax.name,
                    ASSOCODES[assosoftware][1],
                    nature=ASSOCODES[assosoftware][0],
                ):
                    # Finally match just nature and law number
                    weight = 1
                    if weight <= res[tax]['wgt']:
                        continue
                    set_result(tax, assosoftware, weight, res)
        for tax in parsed:
            actioned = ''
            if res[tax].get('wgt') or res[tax].get('amt'):
                vals = {}
                nature = False
                if res[tax].get('nat'):
                    nature = nature_model.search(
                        [('code', '=', res[tax]['nat'])]
                    )[0]
                    vals[NATURE_ID] = nature.id
                elif 'nat' in res[tax]:
                    vals[NATURE_ID] = False
                if vals.get(NATURE_ID, False) != getattr(tax, NATURE_ID).id:
                    if vals.get(NATURE_ID):
                        actioned += _('set nature to %s; ') % res[tax]['nat']
                    else:
                        actioned += _('reset nature; ')
                if (hasattr(tax, 'vsc_exclude_operation') and
                        hasattr(tax, 'vsc_exclude_vat')):
                    if nature and nature.code == 'N1':
                        vals['vsc_exclude_operation'] = True
                        vals['vsc_exclude_vat'] = True
                    else:
                        vals['vsc_exclude_operation'] = False
                        vals['vsc_exclude_vat'] = False
                    if (vals['vsc_exclude_operation'] !=
                            tax.vsc_exclude_operation):
                        if vals['vsc_exclude_operation']:
                            actioned += _('IP18 excluded; ')
                        else:
                            actioned += _('IP18 included; ')
                if 'pay' in res[tax]:
                    vals['payability'] = res[tax]['pay']
                    if vals.get('payability', False) != tax.payability:
                        if vals.get('payability'):
                            actioned += _('set payability to %s; ') % res[
                                tax
                            ].get('pay')
                        else:
                            actioned += _('reset payability; ')
                if res[tax].get('axc'):
                    vals['assosoftware_id'] = assosoftware_model.search(
                        [('code', '=', res[tax]['axc'])]
                    )[0].id
                elif 'axc' in res[tax]:
                    vals['assosoftware_id'] = False
                if (
                    vals.get('assosoftware_id', False)
                    != tax.assosoftware_id.id
                ):
                    if vals.get('assosoftware_id'):
                        actioned += _('set ax code to %s; ') % res[tax].get(
                            'axc'
                        )
                    else:
                        actioned += _('reset ax code; ')
                if 'law' in res[tax]:
                    vals['law_reference'] = res[tax]['law']
                if vals.get('law_reference', False) != tax.law_reference:
                    if vals.get('law_reference'):
                        actioned += _('set law reference to %s; ') % res[
                            tax
                        ].get('law')
                    else:
                        actioned += _('reset law reference; ')
                tax.write(vals)
            if html_txt:
                html += html_txt('', 'tr')
                html += html_txt(tax.description, 'td')
                html += html_txt(tax.name, 'td')
                if actioned:
                    html += html_txt(actioned, 'td')
                else:
                    html += html_txt(_('No action'), 'td')
                html += html_txt('', '/tr')
        if html_txt:
            html += html_txt('', '/table')
        return html

    def gopher_reload_taxes(self, html_txt=None):
        """Reaload tax records from account.tax.template"""

        def get_tmpl_values(tmpl, rec=None):
            company_id = self.env.user.company_id.id
            vals = {}
            if not rec:
                vals['company_id'] = company_id
            for name in ('description',
                         'name',
                         'amount_type',
                         'type_tax_use',
                         'amount',
                         'sequence'):
                if not rec or getattr(rec, name) != getattr(tmpl, name):
                    vals[name] = getattr(tmpl, name)
            for name in ('tax_group_id', ):
                if not rec or (getattr(tmpl, name) and
                               getattr(rec, name) != getattr(tmpl, name)):
                    vals[name] = getattr(tmpl, name).id
            for name in ('account_id', 'refund_account_id'):
                if getattr(tmpl, name) and (
                        (not rec or not getattr(rec, name)) or (
                        getattr(rec, name).code != getattr(tmpl, name).code)):
                    code = getattr(tmpl, name).code
                    acc = self.env['account.account'].search(
                        [('code', '=', code),
                         ('company_id', '=', company_id)]
                    )
                    vals[name] = acc.id
            return vals

        html = ''
        if html_txt:
            html += html_txt(_('Reload Taxes'), 'h3')
            html += html_txt('', 'table')
            html += html_txt('', 'tr')
            html += html_txt(_('Code'), 'td')
            html += html_txt(_('Name'), 'td')
            html += html_txt(_('Action'), 'td')
            html += html_txt('', '/tr')

        template_model = self.env['account.tax.template']
        tax_model = self.env['account.tax']
        company = self.env.user.company_id
        chart_template_id = company.chart_template_id
        for tmpl in template_model.search(
                [('chart_template_id', '=', chart_template_id.id)],
                order='sequence'):
            tax = tax_model.search(
                [
                    ('description', '=', tmpl.description),
                    ('company_id', '=', company.id)]
            )
            actioned = ''
            if len(tax) == 1:
                vals = get_tmpl_values(tmpl, rec=tax)
                if vals:
                    try:
                        tax[0].write(vals)
                        actioned = _('Updated')
                        self._cr.commit()  # pylint: disable=invalid-commit
                    except BaseException as e:
                        self._cr.rollback()  # pylint: disable=invalid-commit
                        actioned = _u('** %s **' % e)
            elif not tax:
                try:
                    tax_model.create(get_tmpl_values(tmpl))
                    actioned = _('New record created')
                    self._cr.commit()  # pylint: disable=invalid-commit
                except BaseException as e:
                    self._cr.rollback()  # pylint: disable=invalid-commit
                    actioned = _u('** %s **' % e)
            if html_txt and actioned:
                html += html_txt('', 'tr')
                html += html_txt(tmpl.description, 'td')
                html += html_txt(tmpl.name, 'td')
                html += html_txt(actioned, 'td')
                html += html_txt('', '/tr')
        if html_txt:
            html += html_txt('', '/table')
        return html
