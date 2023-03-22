{
    'name': 'Account Payment Order Plus',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Account Payment Order extension',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account_payment_order',
        'account_banking_invoice_financing',
    ],
    'data': ['views/account_payment_order_view.xml'],
    'installable': True,
}
