# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'profile_vg7_report',
    'version': '10.0.0.1.1',
    'category': 'Report Templates',
    'author': 'SHS-AV s.r.l.',
    'website': 'http://www.zeroincombenze.it',
    'summary': 'Customized report for VG7',
    'depends': ['account',
                'purchase',
                'sale',
                'l10n_it_fiscalcode'],
    "data": [
        'report/paper_format.xml',
        'report/external_layout.xml',
        'report/report_invoice.xml',
        'report/report_sale.xml',
        'report/purchase_order_templates.xml',
        'report/purchase_quotation_templates.xml',],
    "installable": True,
}
