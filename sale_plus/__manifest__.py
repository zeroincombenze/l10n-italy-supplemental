# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Driven invoice from multiple sale order',
    'category': 'Sales',
    'author': 'SHS-AV s.r.l.',
    'website': 'http://www.zeroincombenze.it',
    'summary': 'Operator can full invoice multiple sale orders.',
    'version': '10.0.0.1.0',
    'depends': ["sale"],
    'data': [
        "wizard/sale_make_invoice_advance_views.xml",
        ],
    'installable': True,
}
