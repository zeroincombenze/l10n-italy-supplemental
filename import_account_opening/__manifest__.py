# -*- coding: utf-8 -*-
# © 2021-2022 SHS-AV srl (www.shs-av.com)
{
    'name': 'Import account opening',
    'version': '10.0.0.1.7',
    'category': 'Tools',
    'author': 'SHS-AV s.r.l.',
    'website': 'https://www.zeroincombenze.it',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': ['base'],
    'external_dependencies': {'python': ['openpyxl']},
    'data': [
        'wizard/wizard_file_import_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}