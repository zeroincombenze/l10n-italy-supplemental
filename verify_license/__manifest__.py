# -*- coding: utf-8 -*-
{
    'name': 'License Checker',
    'version': '12.0.0.2',
    'category': 'Accounting & Finance',
    'summary': 'Verifica licenza ad ogni accesso sulla contabilità',
    'author': 'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'OPL-1',
    'depends': [
        'base',
        'check_license',
    ],
    'external_dependencies': {'python': ['cryptography']},
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
