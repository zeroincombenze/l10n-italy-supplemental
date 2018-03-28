# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
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

{
    'name': 'Italian SEPA Credit Transfer',
    'summary': 'Create SEPA XML files for Italian Credit Transfers',
    'version': '0.2',
    'author': 'SHS-AV s.r.l.',
    'maintainer': 'Antonio Maria Vigliotti',
    'license': 'AGPL-3',
    'category': 'Banking addons',
    'depends': ['account_banking_sepa_credit_transfer'],
    'data': [
        'wizard/export_sepa_view.xml',
        'data/payment_type_sepa_sct.xml',
    ],
    'description': '''
This module is Italian Localization to export payment orders
in SEPA XML file format.
Italian Banks use a no standard V4 PAIN format by CBI
    ''',
    'active': False,
    'installable': False,
}
