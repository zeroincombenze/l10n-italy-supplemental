# -*- coding: utf-8 -*-
# Author: Red Lab.
# Copyright: Red Lab.

{
    'name': 'Convert Sale Order to Purchase Order/RFQ',
    'images': ['images/main_screenshot.png'],
    'version': '10.0.0.6.11',
    'category': 'Sales',
    'summary': 'Converting Sale Order to Purchase Order/RFQ with single button click,'
               ' transfer all important and compatible data. Configurable in settings.',
    'author': 'Red Lab',
    'website': 'lab.stone.red@gmail.com',
    'currency': 'EUR',
    'depends': [
        'purchase_discount',
    ],
    'data': [
        'views/partner_view.xml',
        'views/sale_config_views.xml',
        'views/sale_views.xml',
        'views/purchase_views.xml',
    ],
}
