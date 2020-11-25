# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Refocus reports',
    'version': '10.0.0.1.7',
    'category': 'Report Templates',
    'author': 'SHS-AV s.r.l.',
    'website': 'http://www.zeroincombenze.it',
    'summary': 'Customized report for Refocus',
    'depends': ['account',
                'purchase',
                'sale',
                'sale_resellers',
                'l10n_it_rea',
                'l10n_it_pec',
                'so_convert_po'],
    "data": [
        'views/sale_order_view.xml',
        'report/paper_format.xml',
        'report/external_layout.xml',
        'report/report_invoice.xml',
        'report/report_sale.xml',
        'report/purchase_order_templates.xml',
        'report/purchase_quotation_templates.xml',],
    "installable": True,
}
