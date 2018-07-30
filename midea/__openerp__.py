# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
#                Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "midea",

    'summary': """Odoo Module Example""",

    'description': """
How to make a new Odoo Module
-----------------------------

This module does nothing, it is a just a simple example of Odoo Module
    """,

    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",

    'category': 'Generic Modules/Accounting',
    'version': '10.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        "views/midea_partner_view.xml",
        "security/ir.model.access.csv",
    ],
    "qweb": [],
    "demo": [],
    "test": [],
    "active": False,
    'installable': True
}
