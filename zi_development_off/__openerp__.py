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


{   'name': 'zeroincombenze - Development Mode OFF',
    'version': '0.1',
    'category': 'zeroincombenze',
    'description': """
    Disattiva il link \"Attiva la modalità sviluppatore\" in \"Informazioni su openERP\". \n
    """,
    'author': 'SHS-AV s.r.l.',
    'website': 'http://www.zeroincombenze.it',
    'depends': ['base'],
    'data': [],
    'demo_xml': [],
    'test': [],
    'installable': False,
    'active': False,
    'qweb' : ["static/src/base.xml",],


}
