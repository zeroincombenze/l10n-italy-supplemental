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


{   'name': 'zeroincombenze - Cliente Attivo',
    'version': '0.1',
    'depends': ['base', 'account'],
    'author': 'SHS-AV s.r.l. - Italy',
    'maintainer': 'Valerio Grosso',
    'description': """
Gestione dei Clienti Attivi: abilitati a effettuare registrazioni in determinati mesi dell'anno. \n
Controllo in fase di creazione e modifica fatture sulla data documento e data scadenza. \n
Nuovo menu per la gestione dei Clienti Attivi in Configurazione - Utenti - Clienti Attivi. \n
    """,
    'category': 'zeroincombenze',
    'license': 'AGPL-3',
    'website': 'http://www.zeroincombenze.it',
    'data': ['zi_cliente_attivo_view.xml'],
    'demo_xml': [],
    'test': [],
    'installable': False,
    'active': False,
}
