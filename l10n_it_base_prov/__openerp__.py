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
    'name': 'Italy - Italian districts/provinces',
    'version': '0.2',
    'category': 'Localization/Italy',
    'description': """
Italian districts/provinces
===========================
[EN] Import provinces of Italy
------------------------------
Expand state_id table with Italian values.
\n
[IT] Importa le province italiane
---------------------------------
Espande la tabella degli stati con i valori delle province italiane
\n
""",
    'author': 'SHS-AV s.r.l.',
    'maintainer': 'Antonio Maria Vigliotti',
    'license': 'AGPL-3',
    "depends": ['base'],
    'website': 'http://www.zeroincombenze.it',
    'data': [
        'data/res.country.state.csv',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'images': [],
}
