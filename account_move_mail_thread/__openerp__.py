# -*- coding: utf-8 -*-
# Copyright 2017 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
#                Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "account_move_mail_thread",

    'summary': """Add mail thread to account move""",

    'description': """
Add mail thread to account move
-------------------------------

This module add mail thread feature to account move.
Like invoices, user can write notes or sen messages to followers.
    """,

    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",

    'category': 'Generic Modules/Accounting',
    'version': '7.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        # "views/account_move_view.xml",
    ],
    "qweb": [],
    "demo": [],
    "test": [],
    "active": False,
    'installable': True
}
