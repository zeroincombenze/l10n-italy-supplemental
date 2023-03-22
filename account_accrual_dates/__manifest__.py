# Copyright 2019-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Account accrual dates',
    'version': '12.0.1.0.0',
    'category': 'Accounting & Finance',
    'summary': 'Adds start/end accrual dates on invoice lines and move lines',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'OPL-1',
    'depends': ['account'],
    'data': [
        'views/account_invoice.xml',
        'views/account_move.xml',
    ],
    'installable': True,
}
