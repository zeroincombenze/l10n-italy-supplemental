# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "crm_n_phonecalls",

    'summary': """Link phone calls to crm leads and opportunity""",

    'description': """
Link phone calls to crm leads and opportunity
---------------------------------------------

With this module you can view list of phonecalls in crm lead and opportunity
and you can link from phonecall to crm lead or opportuniy
    """,

    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",

    'category': 'crm',
    'version': '8.0.0.1.0',

    'depends': ['crm'],

    'data': [
        "views/crm_lead_view.xml",
        "views/crm_phonecall_view.xml",
    ],
    'installable': True
}
