# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2010 Odoo Italian Community (<http://www.odoo-italia.org>).
#    Copyright (C) SHS-AV s.r.l. (<http://ww.zeroincombenze.it>)
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
    'name': 'Italian Localization - Base',
    'version': '8.0.0.2.0',
    'category': 'Localization/Italy',
    'description': """

[EN] Italian localization for Partners and Companies.
-----------------------------------------------------

* Check for ZIP code from table.
* Check for City from table.
* Check for District/State from table.
* Supplied just with Italian data.

* May be easily extended with other countries data.


Table based check works well for Italy, France, Spain and other countries.\n
It works bad for UK.
However without validation any address data can be loaded.\n
\n
[IT] Localizzazione italiana per Clienti, Fornitori e Società.
---------------------------------------------------------------
Adattabile a numerosi altri paesi, tra cui Francia e Spagna,\n
ma non adattabile al Regno Unito.\n
In ogni caso è possibile caricare qualsiasi dato, senza validazione.\n
""",
    'author': 'OpenERP Italian Community',
    'maintainer': 'Antonio Maria Vigliotti',
    'website': 'http://www.zeroincombenze.it',
    'license': 'AGPL-3',
    "depends": ['base'],
    "init_xml": [
    ],
    "update_xml": ['partner/partner_view.xml',
                   # 'wizard/partner_update_wizard_view.xml',
                   # 'view/fiscalcode_view.xml',
                   "security/ir.model.access.csv",
                   'partner/data/res.region.csv',
                   'partner/data/res.province.csv',
                   'partner/data/res.country.state.csv',
                   'partner/data/res.city.csv',
                   'partner/data/res.partner.title.csv',
                   'partner/data/res.country.csv'],
    "demo_xml": [],
    "active": False,
    "installable": True
}

# http://www.istat.it/strumenti/definizioni/comuni/
# i dati dovrebbero essere sincronizzati con questi
