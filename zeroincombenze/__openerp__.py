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
    'active': True,            # Auto-installable when create!!
    'name': 'zeroincombenze®',
    'version': '0.1',
    'depends': ['l10n_it_fiscal',
                'l10n_it_bbone',
                'base_iban',
                'account_cancel',
                # 'account_banking_sepa_credit_transfer',
                'account_chart_update',
                'multi_company',
                'point_of_sale',
                'report_webkit',
                'account_vat_period_end_statement',
                'account_invoice_entry_date',
                'l10n_it_partially_deductible_vat',
                'zi_account_control',
                'zi_headers_webkit',
                # 'zi_invoice_webkit',
                # 'zi_purchase_order_webkit',
                # 'zi_sale_order_webkit',
                ],
    'author': 'SHS-AV s.r.l.',
    'maintainer': 'Antonio Maria Vigliotti',
    'description': """
Zeroincombenze®
===============
[EN] zeroincombenze® installer
------------------------------
This module is a bunch which keeps together all needed modules
for zeroincombenze® standard installation.
Installing this module, full set of modules are installed.

Please, wait for completion: might be required a bit of time
\n
[IT] zeroincombenze® installatore
---------------------------------
Questo modulo è un contenitore per mantenere insieme tutti
i moduli necessari all'installazione standard di zeroincombenze®.
L'installazione di questo modulo, installa tutti i moduli necessari.

Attenzione! L'installazione dei moduli potrebbe richiedere un po' di tempo.
    """,
    'license': 'AGPL-3',
    'category': 'Hidden',
    'website': 'http://www.zeroincombenze.it',
    'data': [
        'security/ir.model.access.csv',
        'saas_account_view.xml',
        #             'zi_alignment_view.xml',
    ],
    'demo': [],
    'init_xml': ['data/res_users.xml'],
    'update_xml': [],
    'installable': False,
    'auto_install': True,
    'images': [],
    'js': ['static/src/js/announcement.js'],
}
