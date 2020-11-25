# -*- coding: utf-8 -*-
#
# Copyright 2019-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    'name': 'Renumber customer account invoice lines',
    'summary': 'Sort invoice lines by sale order, DdT, sequence, id',
    'version': '10.0.0.1.1',
    'category': 'Generic Modules/Accounting',
    'author': 'SHS-AV s.r.l.',
    'website': 'https://www.zeroincombenze.it/servizi-le-imprese/',
    'depends': [
        'account',
        'sale',
        'l10n_it_ddt',
    ],
    'data': [
        'views/account_invoice_view.xml',
        'views/package_preparation_view.xml',
    ],
    'installable': True,
    'development_status': 'Alpha',
}
