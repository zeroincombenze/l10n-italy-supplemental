# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2010 Odoo Italian Community (<http://www.odoo-italia.org>).
#    Copyright (C) SHS-AV s.r.l. (<http://ww.zeroincombenze.it>)
#    All Rights Reserved
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

from openerp.osv import osv
from openerp.osv import fields


class res_country(osv.osv):
    _inherit = 'res.country'

    _columns = {
        'ufficioiva': fields.char(
            'VAT Office Code', size=4,
            help='VAT Office Code'),
        'inue': fields.boolean(
            'Member of EU',
            help='This country is member of the European Union.'),
        'inue_date': fields.date(
            'Member of EU from',
            help='This country is member of the European Union since'),
        'blacklist': fields.boolean(
            'Blacklist',
            help='This country is in blacklist.'),
        'blacklist_date': fields.date(
            'Blacklist from',
            help='This country is in blacklist since this date.'),
        'insepa': fields.boolean(
            'Use SEPA',
            help='This country use SEPA standard.'),
        'insepa_date': fields.date(
            'Use SEPA from',
            help='This country use SEPA standard since this date.'),
        'ean': fields.char(
            'GTIN Code', size=3,
            help='GTIN Code. (EAN Code).'),
        'lingua': fields.char(
            'Language', size=2,
            help='Official language of this country.'),
        'chk4addr': fields.integer(
            'Check on address', size=1,
            help='Enable or disable check on address.'),
        'chk4zip': fields.integer(
            'Multizone ZIP code', size=1,
            help='Number of digits in multizone ZIP code by this country'),
    }
