# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Account journal Bank IBAN position',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Update view in account journal form',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'OPL-1',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/account_view.xml',
    ],
    'installable': True,
}
