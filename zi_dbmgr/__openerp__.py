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
{
    'name': 'zi_dbmgr',
    'version': '0.2',
    'category': 'Utilities',
    'description': """
Zeroincombenze®
===============
[EN] zeroincombenze® create new database
----------------------------------------
This utility creates a new empty database with incremental name.
DB name has a prefix, progressive number and suffix.


\n
[IT] zeroincombenze® crea nuovo database
----------------------------------------
Utility che permette di creare un nuovo database vuoto
con un nome costruito in modo incrementale.
Il nome è definito da un prefisso, un progressivo numerico e un suffisso.
""",
    'author': 'SHS-AV s.r.l.',
    'maintainer': 'Alessandro Camilli',
    'website': 'http://www.zeroincombenze.it',
    'license': 'AGPL-3',
    # 'depends' : ['base', 'auth_oauth', 'auth_signup'],
    'data': [
        'security/ir.model.access.csv',
        'zi_dbmgr_view.xml',
        'wizard/database_create_view.xml',
    ],
    # 'js': ['static/src/js/auth_dbmgr_signup.js'],
    'demo': [],
    "active": False,
    'installable': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
