# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
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


{'name': 'zeroincombenze - Report Webkit Fatture',
    'version': '0.1',
    'category': 'zeroincombenze',
    'description': """
    Sostituisce il report Fattura con uno personalizzato da zeroincombenze
    """,
    'author': 'SHS-AV s.r.l.',
    'website': 'http://www.zeroincombenze.it',
    'depends': ['base', 'account', 'report_webkit', 'zi_headers_webkit'],
    'data': ['security/ir.model.access.csv',
             'invoice_report.xml',
             'view/invoice_view.xml'],
    'demo_xml': [],
    'test': [],
    'installable': False,
    'active': False,
 }
