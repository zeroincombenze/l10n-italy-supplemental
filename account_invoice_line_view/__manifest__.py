# -*- coding: utf-8 -*-
# Copyright (C) 2014 Rooms For Limited T/A OSCG <https://www.odoo-asia.com>
# Copyright (C) 2016-22 SHS-AV s.r.l. <https://zeroincombenze.it>
#
{
    'name': 'Invoice Line View',
    'version': '10.0.1.0.4',
    'category': 'Account',
    'summary': 'Adds Invoice Line menu items',
    'author': 'SHS-AV s.r.l',
    'website': 'https://zeroincombenze.it',
    'license': 'AGPL-3',
    'images' : [],
    'depends': ['account',
                'sale_commission'],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
}