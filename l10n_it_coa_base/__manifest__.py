# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
#
{
    'name': 'Chart of Account improvements',
    'version': '12.0.0.1.25',
    'category': 'Accounting',
    'summary': 'Chart of Account improvements',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/profile_account.xml',
        'data/account_account_type.xml',
        'views/account_account_view.xml',
        'views/account_group_view.xml',
        'views/profile_account_view.xml',
        'views/config_view.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
    'post_init_hook': 'set_default_nature_post',
    'conflicts': [
        'account_type_menu',
        'account_group_menu',
    ],
}
