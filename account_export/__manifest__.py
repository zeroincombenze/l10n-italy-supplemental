# -*- coding: utf-8 -*-
# Copyright 2018 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
{
    'name': "account_export",

    'summary': """Export account moves""",

    'description': """
Export Account Moves
--------------------

""",

    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",

    'category': 'Accounting',
    'version': '10.0.0.1.0',

    'depends': ['account',],

    'data': ['security/ir.model.access.csv',],
    'installable': True
}
