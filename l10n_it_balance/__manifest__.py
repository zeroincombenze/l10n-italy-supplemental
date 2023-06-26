# Copyright 2020-23 LibrERP enterprise network <https://www.powerp.it>
# Copyright 2020-23 Didotech s.r.l. <https://www.didotech.com>
# Copyright 2020-23 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License OPL-1 or later
# (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps)
#
{
    'name': 'l10n_it_balance',
    'version': '12.0.0.3.77',
    'category': 'Generic Modules/Accounting',
    'summary': 'Account balance',
    'author': 'LibrERP enterprise network and other partners',
    'website': 'https://www.librerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'date_range_plus',
        'account_fiscal_year_plus',
        'l10n_it_coa_base',
        'account_accrual_dates',
        'l10n_it_menu',
        'l10n_it_validations',
    ],
    'data': [
        'security/ir.model.access.csv',
        'reports/templates/trial_balance.xml',
        'reports/templates/ordinary_balance.xml',
        'reports/templates/opposite_balance.xml',
        'reports/templates/client_supplier_balance.xml',
        'wizard/generate_balance_view.xml',
        'wizard/export_xls.xml',
        'wizard/export_opposite_xls.xml',
        'views/account_balance_view.xml',
        'views/ir_ui_menu.xml',
        'views/account_invoice_view.xml',
        'views/account_move_view.xml',
        'views/account_view.xml',
    ],
    'installable': True,
}
