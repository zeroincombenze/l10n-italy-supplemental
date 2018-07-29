# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "sale_z0tricky",

    'summary': """Add sale order to invoice""",

    'description': """
Add sale order to invoice
-------------------------

Add sale order to invoice
    """,

    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",

    'category': 'Generic Modules/Accounting',
    'version': '10.0.0.1.0',

    'depends': ['account', 'sale'],

    'data': [
        "views/account_invoice_views.xml",
        # "security/ir.model.access.csv",
    ],
    'installable': True
}
