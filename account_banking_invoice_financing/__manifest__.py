# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Account banking invoice financing',
    'version': '12.0.8.9.19',
    'category': 'Accounting',
    'summary': 'Account banking invoice financing',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'account_due_list',
        'account_duedates',
        'account_payment_order',
        'account_payment_mode',
        'account_banking_common',
        'account_invoice_13_more',
    ],
    'data': [
        'views/account_due_list_view.xml',
        'views/account_payment_order_form_view.xml',
        'views/account_view_move_line_form.xml',
        'reports/print_account_payment_order_ita.xml',
        'reports/account_payment_order_financing_report.xml',
        'data/account_payment_method.xml',
        'wizard/wizard_payment_order_invoice_financing.xml',
        'wizard/wizard_payment_order_close_financing.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
