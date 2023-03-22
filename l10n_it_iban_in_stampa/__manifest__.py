# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Iban in stampa',
    'version': '12.0.1.1.33',
    'category': 'Generic Modules/Accounting',
    'summary': 'Impostazione iban per la stampa nei documenti',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'sale',
        'purchase',
        'l10n_eu_account',
        'assigned_bank',
        'l10n_it_fiscal_payment_term',
        'account_payment_partner',
        'account_invoice_13_more',
        'l10n_it_ddt',
        'account_common_mixin',
    ],
    'data': [
        'views/account_invoice_view.xml',
        'views/account_move_view.xml',
        'views/purchase_order_view.xml',
        'views/res_partner_bank.xml',
        'views/sale_order_view.xml',
        'report/report_invoice.xml',
        'report/report_sale_order.xml',
        'report/report_purchase_order.xml'
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
