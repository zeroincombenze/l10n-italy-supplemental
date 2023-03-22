# -*- coding: utf-8 -*-
{
    'name': "Credit Notes Journal",

    'summary': """
        Module to handle credit notes""",

    'description': """
        Module to handle credit notes
    """,

    'author': "Didotech Srl",
    'website': "http://www.didotech.com",

    'category': 'Generic Modules/Accounting',
    'version': '12.0.4.6.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'views/account_journal_view.xml',
        'views/res_company_view.xml'
    ]
}