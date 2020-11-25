# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Resellers',
    'category': 'Sales',
    'author': 'SHS-AV s.r.l.',
    'website': 'http://www.zeroincombenze.it',
    'summary': 'Manage Sale Resellers',
    'version': '10.0.1.5.4',
    'description': """
Manager Sale Resellers
======================
""",
    'depends': ['purchase',
                'sale',
                # 'base_geolocalize'
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
