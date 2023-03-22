# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Invoice entry dates',
    'version': '12.0.2.6.32',
    'category': 'Accounting',
    'summary': 'Registration, vat/balance application dates',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'OPL-1',
    'depends': [
        'account',
        'l10n_it_fiscal_payment_term',
        'account_fiscal_year',
        'account_invoice_13_more',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/account_journal_view.xml',
        'view/account_move_view.xml',
        'view/account_invoice_view.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
