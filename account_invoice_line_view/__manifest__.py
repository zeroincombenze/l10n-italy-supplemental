# -*- coding: utf-8 -*-
#    Odoo, Open Source Management Solution
#    Copyright (C) 2014 Rooms For (Hong Kong) Limited T/A OSCG
#    <https://www.odoo-asia.com>
{
    'name': 'Invoice Line View',
    'version': '10.0.1.0.3',
    'category': 'Account',
    'summary': 'Adds Customer/Supplier Invoice Line menu items',
    'description': """
Main Features
==================================================
* Add menu items Customer Invoice Lines and Supplier Invoice Lines
* Captures exchange rates as of the invoice dates and shows the base currency amounts in the output.
    """,
    'author': 'Rooms For (Hong Kong) Limited T/A OSCG',
    'website': 'https://www.odoo-asia.com',
    'license': 'AGPL-3',
    'images' : [],
    'depends': ['account',
                'sale_commission'],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
}
