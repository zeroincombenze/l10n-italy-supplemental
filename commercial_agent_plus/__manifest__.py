# -*- coding: utf-8 -*-
{
    'name': "Commercial Agent Plus",
    'summary': """
        Commercial Agent Plus.
    """,
    'description': """
        Commercial Agent Plus.
    """,
    'author': "Bloomup, Matteo Piciucchi",
    'website': "http://bloomup.it",
    'category': 'Sales',
    'version': '1.0',
    'depends': [
        'base',
        'sale',
        'contacts',
        'sale_management',
        'account',
        'stock',
        'sale_stock'
    ],
    'data': [
       'data/groups.xml',
       'security/ir.model.access.csv',
       'views/assets.xml',
       'views/partner.xml',
       'views/area.xml',
       'views/orders.xml',
       'views/product.xml',
       'views/commission.xml',
       'views/settlement.xml',
       'views/invoice.xml',
       'views/payment.xml',
       'data/agent.xml',
       'data/rules.xml',
    ],
    'application': True,
    'installable': True,
}
