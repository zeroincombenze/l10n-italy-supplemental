# -*- coding: utf-8 -*-
#
# Copyright 2017-2018, Didotech srl (http://www.didotech.com).
# Copyright 2017-2018, Andrei Levin <andrei.levin@didotech.com>
# Copyright 2018, Associazione Odoo Italia <https://odoo-italia.org>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    'name': 'Stock Parzial Move',
    'version': '8.0.0.1.0',
    'category': 'Warehouse Management',
    'license': 'AGPL-3',
    'author': 'Didotech srl',
    'website': 'http://www.didotech.com/',
    'depends': [
        'stock',
        'sale',
    ],
    'data': [
        'views/stock_view.xml'
    ],
    'installable': True,
}
