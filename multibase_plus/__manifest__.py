# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "multibase_plus",

    'summary': """Enhanced Odoo Features""",

    'description': """
Enhanced Odoo Features
----------------------

This module add some features in order to make Odoo installation more enjoyable
and with coherent interface independent by Odoo version

  Features                              | 6.1 | 7.0 | 8.0 | 9.0 | 10.0 | 11.0

  Add customer ref in sal.order tree    | x   | x   | x   | x   | YES  | x

  Add refund (credit note) invoice menu | N/N | N/N | N/N | x   | YES  | N/N

Legend:

    x:   not avaiable

    YES: avaiable with thie module

    N/N: not needed, already in Odoo core

""",

    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",

    'category': 'Base',
    'version': '10.0.0.1.1',

    'depends': ['base',
                'sale'],

    'data': [
        "views/sale_order_view.xml",
        "views/account_invoice_view.xml",
    ],
    'installable': True
}
