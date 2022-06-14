# -*- coding: utf-8 -*-
# Copyright 2018 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Import file Excel into sale order",

    'summary': 'Import sale order lines from a Excel',
    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",

    'category': 'Generic Modules/Accounting',
    'version': '10.0.0.1.1',

    'depends': [
        'sale',
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "wizard/import_file_view.xml",
    ],
    'installable': True
}
