# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Alessandro Camilli (a.camilli@yahoo.it)
#    Copyright (C) 2014
#    Associazione Odoo Italia (<http://www.openerp-italia.org>)
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
    'name': 'Comunicazione Polivalente (c.d. Spesometro)',
    'version': '0.3',
    'category': 'Localisation/Italy',
    'description': """

Comunicazione Polivalente (Spesometro)
======================================
[EN] Fiscal communication called Spesometro
-------------------------------------------

This software is just for Italian Fiscal Law.
It is not usable in another country.

[IT] Comunicazione fiscale Spesometro
-------------------------------------

Permette di adempiere all'obbligo di comunicazione dati inerenti le fatture
clienti e fornitori da inviare all'Agenzia delle Entrate in forma telematica.

Funzionalità:

- Creazione comunicazione in forma Aggregata

- Export file formato Agenzia delle Entrate

""",
    'author': 'Alessandro Camilli',
    'website': 'http://www.odoo-italia.org',
    'license': 'AGPL-3',
    "depends": ['account',
                'l10n_it_base',
                'l10n_it_fiscalcode'],
    "data": [
              'security/ir.model.access.csv',
              'spesometro_view.xml',
              'wizard/wizard_crea_comunicazione_view.xml',
              'wizard/wizard_default_view.xml',
              'wizard/wizard_export_view.xml',
              'data/res.country.csv',
    ],
    "demo": [],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
