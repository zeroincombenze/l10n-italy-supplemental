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
    'name': 'zeroincombenze - Controlli su codici PdC',
    'version': '0.1',
    'depends': ['base', 'account'],
    'author': 'SHS-AV s.r.l.',
    'maintainer': 'Valerio Grosso',
    'description': """
Zeroincombenze(R)
=================
[EN] chart of account code validate
-----------------------------------
Zeroincombenze®, with module l10n_it_fiscal,
suppplies Italian standard chart of account
which covers full Italian fiscal laws.

However every company should be able to adapt own specific chart of account
without override schema.
Every chart of account code ending with '0' is reserved
to Zeroincombenze® schema.
\n

.. image:: /zi_account_control/static/src/img/icon.jpg

[IT] validazione codici piano dei conti
---------------------------------------
Zeroincombenze®, tramite il modulo l10n_it_fiscal,
fornisce un piano dei conti che copre tutte le esigenze fiscali italiane.

Tuttavia, ogni società deve essere in grado di apportare modifiche
per le proprie specifiche esigenze mantenendo la struttura di codifica.
Ogni codice terminante con la cifra '0' è riservato a Zeroincombenze®.

    """,
    'license': 'AGPL-3',
    'category': 'zeroincombenze',
    'website': 'http://www.zeroincombenze.it',
    'data': [],
    'demo': [],
    'installable': True,
    'auto_install': True,
}
