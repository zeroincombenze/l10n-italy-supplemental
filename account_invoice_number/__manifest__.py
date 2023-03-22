# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Invoice Sequence Number',
    'version': '12.0.1.0.1',
    'category': 'Accounting',
    'summary': 'Add methods to get invoice number as integer extending ir_sequence and account_invoice',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'OPL-1',
    'depends': [
        'base',
        'account',
    ],
    'installable': True,
}
