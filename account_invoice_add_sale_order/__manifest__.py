# -*- coding: utf-8 -*-
# Copyright 2018 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "account_invoice_add_sale_order",

    'summary': """Add sale order to sale account invoice""",

    'description': """
Add sale order to invoice
-------------------------

Add sale order when editing sale invoice like Odoo standard
purchase invoice.
Sale order state is updated conseguently.
    """,

    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",

    'category': 'Generic Modules/Accounting',
    'version': '10.0.0.1.1',

    'depends': [
        'account',
        'sale',
        'multibase_plus',
    ],

    'data': [
        "views/account_invoice_views.xml",
    ],
    'installable': True
}
