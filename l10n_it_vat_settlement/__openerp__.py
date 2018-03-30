# -*- coding: utf-8 -*-
# Copyright 2017 Didotech srl (<http://www.didotech.com>)
#                Andrei Levin <andrei.levin@didotech.com>
#                Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo-Italia.org Community
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Italian Localisation - VAT Settlement',
    'version': '7.0.0.1.0',
    'category': 'Localisation/Italy',
    'author': 'Odoo Italian Community',
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_pyxb_bindings',
        'base',
        # 'l10n_it_account',
        'l10n_it_fiscalcode',
        'account_vat_period_end_statement'
    ],
    "data": [
        'views/account_view.xml',
        'wizard/vat_settlement.xml'
    ],
    "demo": [
        # 'demo/account_tax.xml',
    ],
    'test': [
        # 'test/tax_computation.yml',
        # 'test/report_registries.yml',
    ],
    "active": False,
    "installable": True
}
