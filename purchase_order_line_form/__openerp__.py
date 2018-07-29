# -*- coding: utf-8 -*-
#
# Copyright 2017-2018, Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# Copyright 2017-2018, Associazione Odoo Italia <https://odoo-italia.org>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    'name': 'Purchase Order lines easy editor',
    'version': '8.0.0.1.0',
    'category': 'Accounting & Finance',
    'description': """(en)

Edit Purchase Order Lines in a separate view
---------------------------------------------


(it)

Modifica le linee di ordine fornitore in una vista separata
-----------------------------------------------------------
""",
    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",
    'depends': [
        'base',
        'purchase',
    ],
    'data': [
        "views/purchase_order_view.xml",
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {}
}
