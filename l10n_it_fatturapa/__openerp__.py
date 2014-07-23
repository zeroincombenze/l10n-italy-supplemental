# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Italian Localization - FatturaPA',
    'version': '0.1',
    'category': 'Localization/Italy',
    'summary': 'Fatturazione Elettronica per la Pubblica Amministrazione',
    'description': """
    Fatturazione Elettronica per la Pubblica Amministrazione.
    """,
    'author': 'OpenERP Italian Community',
    'website': 'http://www.openerp-italia.org',
    'license': 'AGPL-3',
    "depends": ['base', 'account', 'l10n_it_base', 'l10n_it_fiscalcode'],
    "data": [
        'views/account_view.xml',
        'views/company_view.xml',
        'views/partner_view.xml',
        'wizard/wizard_export_fatturapa_view.xml',
        'data/fatturapa_data.xml',
    ],
    "test": [],
    "demo": ['demo/account_invoice_fatturapa.xml'],
    "installable": True
}
