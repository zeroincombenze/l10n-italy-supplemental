# -*- coding: utf-8 -*-
#
# Copyright 2018, Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    'name': "z0_invoice_report",

    'summary': """Zeroincombenze customized invoice report""",

    'description': """
Customized invoice report
-------------------------

Add fiscalcode after vat in customer box
    """,

    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",

    'category': 'Report',
    'version': '7.0.0.1.0',

    'depends': ['account',
                'l10n_it_fiscalcode'],

    'data': [
        "report/account_report.xml",
    ],
    'installable': True
}
