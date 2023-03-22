# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Suddivisione dei costi',
    'version': '12.0.0.1.19',
    'category': 'Accounting',
    'summary': 'Suddivisione dei costi',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'OPL-1',
    'depends': [
        'account',
        'sale',
        'product',
        'base',
    ],
    'data': [
        'views/product_views.xml',
        'views/sale_views.xml',
        'views/invoice_views.xml',
    ],
    'installable': True,
}
