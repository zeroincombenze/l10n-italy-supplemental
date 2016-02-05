# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
#    All Rights Reserved
#
#    Written by Alessando Camilli (alessandrocamilli@openforce.it).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""
    Project to import purchase invoices from mail
"""
from osv import osv
# from openerp import pooler
from datetime import date
import re


class res_partner(osv.osv):
    _inherit = 'res.partner'

    def get_def_partner(self):
        partner_ids = self.pool.get('res.parter')
        if partner_ids:
            return partner_ids[0]
        else:
            return None


class res_company(osv.osv):
    _inherit = 'res.company'

    def get_def_company(self):
        company_ids = self.pool.get('res.company')
        if company_ids:
            return company_ids[0]
        else:
            return None


class res_partner_mail(osv.Model):
    _name = "res.partner"
    _inherit = ['res.partner', 'mail.thread']

    def parse_description(self, description):
        """
        Read mail text and search for some keyword
        in order to set invoice fields
        """
        xtls = {'fattura': 'invoice',
                'totale': 'amount',
                'data': 'date',
                }
        dict = self.set_default_dict()
        for line in description.split('\n'):
            while line:
                line = skip_blanks(line)
                line, word = get_word(line)
                word = word.lower()
                if word in xtls:
                    field = xtls[word]
                    line = skip_delimiters(line)
                    if field == 'amount':
                        line, value = get_number(line)
                    else:
                        line, value = get_token(line)
                    dict[field] = value
        return dict


class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def set_default_dict(self):
        dict = {}
        # company = self.pool.get('res.company')
        # dict['company_id'] = company.get_def_company()
        dict['company_id'] = 4
        # partner = self.pool.get('res.partner')
        # dict['partner_id'] = partner.get_def_partner()
        dict['partner_id'] = 61
        dict['account_id'] = 1066
        dict['type'] = 'in_invoice'
        dict['state'] = 'draft'
        dict['reference'] = 'email draft invoice'
        dfmt = "%Y-%m-%d"
        dict['date_invoice'] = date.today().strftime(dfmt)
        dict['currency_id'] = 1
        return dict


class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'


def skip_blanks(txt):
    x = re.match('[ \t]*', txt)
    if x:
        i = x.end()
    else:
        i = 0
    return txt[i:]


def skip_delimiters(txt):
    x = re.match('[^a-zA-Z0-9]*', txt)
    if x:
        i = x.end()
    else:
        i = 0
    return txt[i:]


def get_word(txt):
    x = re.match('[a-zA-Z]*', txt)
    if x:
        i = x.end()
        w = txt[0:i].strip()
    else:
        i = 0
        w = ''
    return txt[i:], w


def get_number(txt):
    x = re.match(r'[+-]?[0-9\.]*[,]?[0-9]*', txt)
    if x:
        i = x.end()
        w = txt[0:i].strip()
    else:
        i = 0
        w = ''
    return txt[i:], w


def get_token(txt):
    x = re.match(r'[a-zA-Z0-9_\.-/]*', txt)
    if x:
        i = x.end()
    else:
        i = 0
    return txt[i:]
