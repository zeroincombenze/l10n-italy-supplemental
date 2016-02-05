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
    'name': 'zeroincombenze - Bottone Aggiorna',
    'version': '0.1',
    'depends': ['base', 'sale', 'purchase', 'account'],
    'author': 'SHS-AV s.r.l.',
    'description': """
    Aggiunge il bottone Aggiorna nell'header delle seguenti viste: \n 
    - Ordine di vendita : sale.order.form \n 
    - Ordine di acquisto : purchase.order.form \n 
    - Fatture Clienti : account.invoice.form \n 
    - Fatture Fornitori : account.invoice.supplier.form \n 
    """,
    'license': 'AGPL-3',
    'category': 'zeroincombenze',
    'website': 'http://www.zeroincombenze.it',
    'data': ['zi_bottone_aggiorna.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
