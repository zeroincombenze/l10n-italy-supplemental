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
    'name': 'sepa italian cuc',
    'version': '0.1',
    "depends": ['base',
                'base_iban',
                'account_banking_pain_base',
                ],
    'author': 'SHS-AV s.r.l.',
    'maintainer': 'Antonio Maria Vigliotti',
    'description': """
Add CUC to company
==================
[EN]
Add CUC code to company profile useb by Sepa SCT.

This module contains additional italian party_issuer_per_country field
for Sepa transaction.

Tag InitgPty -> Nm -> Id -> OrgId -> Othr -> Id
\n
[IT]
Aggiunge il codice CUC (codice SIA) usato nei file xml dei
bonifici bancari Sepa, che entreranno in vigore
dal 1 febbraio 2016.

Il CUC è inserito nel tag InitgPty, subito dopo il tag nm
insieme al tag issr di valore CBI, come previsto dallo standard

CBI-EU STIP-MO-001 00.04.00
    """,
    'license': 'AGPL-3',
    'category': 'Localisation/Italy',
    'website': 'http://www.zeroincombenze.it',
    "data": [
        'view/company_view.xml',
    ],
    'demo': [],
    'update_xml': [],
    'installable': False,
    'auto_install': False,
    'images': [],
}
