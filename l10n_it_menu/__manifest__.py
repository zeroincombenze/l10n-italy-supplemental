# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'l10n_it_menu',
    'version': '12.0.0.1.5',
    'category': 'Generic Modules/Accounting',
    'summary': 'Accounting menu',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'OPL-1',
    'depends': [
        'base',
        'account',
    ],
    'data': ['views/accounting_menuitem.xml'],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
