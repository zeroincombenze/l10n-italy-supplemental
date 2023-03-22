# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-2022 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'account_invoice_zero_amount',
    'version': '12.0.1.0.4',
    'category': 'Generic Modules/Accounting',
    'summary': 'Account invoice zero amount',
    'author': 'LibrERP enterprise network and other partners',
    'website': 'https://www.librerp.it',
    'development_status': 'Alpha',
    'license': 'OPL-1',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/account_invoice_button.xml',
        'wizard/wizard_confirm.xml',
    ],
    'installable': True,
}
