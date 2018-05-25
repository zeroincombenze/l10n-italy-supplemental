# -*- coding: utf-8 -*-
#
# Copyright 2017-2018, Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    'name': 'Import CRM leads from csv file',
    'version': '8.0.0.1.0',
    'category': 'Tools',
    'description': """(en)

Import CRM leads from csv file
------------------------------


(it)

Importa contatti CRM da un file csv
-----------------------------------
""",
    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",
    'depends': [
        'base',
        'crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_import_view.xml',
    ],
    'external_dependencies': {
        'python': [
            'os0',
        ],
    },
    'installable': True,
}
