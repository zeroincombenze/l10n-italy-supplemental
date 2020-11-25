# -*- coding: utf-8 -*-
# Copyright 2019 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'l10n_eu_account',

    'summary': 'EU invoicing & accounting base',

    'author': 'SHS-AV s.r.l.',
    'website': 'https://www.zeroincombenze.it/',

    'category': 'Generic Modules/Accounting',
    'version': '10.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
         'wizard/wizard_configure.xml',
    ],
    'installable': True
}
