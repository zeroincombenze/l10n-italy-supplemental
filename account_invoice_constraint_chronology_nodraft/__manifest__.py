# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Account Invoice Constraint Chronology No Draft',
    'version': '12.0.1.1.3',
    'category': 'Accounting',
    'summary': 'Validate using check on invoice not in state "draft" ',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'OPL-1',
    'depends': ['account'],
    'data': ['views/account_view.xml'],
    'installable': True,
    'pre_init_hook': 'pre_init_hook',
}
