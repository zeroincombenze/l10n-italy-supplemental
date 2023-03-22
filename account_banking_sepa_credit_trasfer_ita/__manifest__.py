# Copyright 2022 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2022 Didotech s.r.l. <https://www.didotech.com>
#
{
    'name': 'Account SEPA Credit Tranfer ITA CBI',
    'version': '12.0.1.0.0',
    'category': 'Banking addons',
    'summary': 'Gestione SCT/Bonifico ',
    'author': 'Librerp and other partners',
    'website': 'https://www.librerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'account_banking_common',
        'account_banking_pain_base',
        'account_banking_fintech_initializer',
    ],
    'data': [
        'data/account_payment_method.xml',
    ],
    'installable': True,
}
