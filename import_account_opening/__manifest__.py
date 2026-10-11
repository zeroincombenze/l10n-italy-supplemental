# -*- coding: utf-8 -*-
# Copyright 2021-26 Zeroincombenze srls <https://www.zeroincombenze.it>
{
    'name': 'Import account opening',
    'version': '10.0.0.1.8',
    'category': 'Tools',
    'author': 'Zeroincombenze srls',
    'website': 'https://www.zeroincombenze.it',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': ['account'],
    'external_dependencies': {'python': ['openpyxl']},
    'data': [
        'wizard/wizard_file_import_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}