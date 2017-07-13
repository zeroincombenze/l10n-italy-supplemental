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
    'version': '7.0.0.3.1',
    'category': 'Localization/Italy',
    'description': """

Enhanced localization for Partners and Companies.
-------------------------------------------------

[en]  This module expands l10n_it_base functionality.

Warning! This module works better with Zeroincombenze® version of l10n_it_base
See https://github.com/zeroincombenze/l10n-italy/tree/7.0/l10n_it_base


Localizzazione evoluta per Clienti, Fornitori e Società.
--------------------------------------------------------

[it]  Espande le funzionalità di l10n_it_base

Attenzione! Questo modulo funziona meglio in conginzione con la versione
Zeroincombenze® di l10n_it_base
https://github.com/zeroincombenze/l10n-italy/tree/7.0/l10n_it_base

""",
    'author': "SHS-AV s.r.l.,"
              "Odoo Italian Community,Odoo Community Association (OCA)",
    'maintainer': 'Antonio Maria Vigliotti',
    'website': 'http://www.zeroincombenze.it',
    'license': 'AGPL-3',
    "depends": ['l10n_it_base'],
    "init_xml": [
    ],
    "update_xml": ['views/city_view.xml',
                   'views/company_view.xml',
                   'views/country_view.xml',
                   'views/partner_view.xml',
                   'views/state_view.xml',
                   # 'view/fiscalcode_view.xml',
                   # "security/ir.model.access.csv",
                   'data/res.city.csv',
                   # 'data/res.country.state.csv',
                   'data/res.country.csv'],
    "demo_xml": [],
    "test": ['test/res_partner.yml',
             ],
    "active": False,
    "installable": True
}

# http://www.istat.it/strumenti/definizioni/comuni/
# i dati dovrebbero essere sincronizzati con questi
