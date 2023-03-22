# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-2022 Didotech s.r.l. <https://www.didotech.com>
#
{
    'name': 'Account Banking Sepa Direct Debit ITA',
    'version': '12.0.1.0.2',
    'category': 'Accounting',
    'summary': 'Account Banking Sepa Direct Debit ITA for payment modules',
    'author': 'LibrErp enterprise network and other partners',
    'website': 'https://www.librerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'account_banking_common',
        'account_banking_pain_base',
        'account_banking_mandate',
        'account_banking_fintech_initializer',
    ],
    'data': [
        'data/account_payment_method.xml',
    ],
    'installable': True,
}
