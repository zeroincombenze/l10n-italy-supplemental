# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Date Range Plus',
    'version': '12.0.1.0.3',
    'category': 'Uncategorized',
    'summary': 'Manage all kind of date range',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Mature',
    'license': 'AGPL-3',
    'depends': [
        'date_range',
        'web',
    ],
    'data': ['views/assets.xml'],
    'installable': True,
    'maintainers': [
        'Didotech Srl',
        'Zeroincombenze (SHS Srl)',
    ],
}
