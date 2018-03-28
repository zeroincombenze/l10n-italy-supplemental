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
{
    'name': 'zeroincombenze - Webkit Headers',
    'version': '0.1',
    'depends': ['base', 'report_webkit'],
    'author': 'SHS-AV s.r.l.',
    'description': """
Headers zeroincombenze: \n
- zi_header_ordini: zeroincombenze Header Ordini \n
- zi_small_header: zeroincombenze Small Header Standard \n
- zi_small_footer: zeroincombenze Small Footer Standard \n

- zi_header_ordini_datetime: zeroincombenze Header Ordini (Data e Ora) \n
- zi_small_header_datetime: zeroincombenze Small Header Std (Data e Ora) \n
- zi_small_footer_datetime: zeroincombenze Small Footer Std (Data e Ora) \n
    """,
    'license': 'AGPL-3',
    'category': 'zeroincombenze',
    'website': 'http://www.zeroincombenze.it',
    'init_xml': [],
    'update_xml': ['zi_headers_data.xml'],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
}
