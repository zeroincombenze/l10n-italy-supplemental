# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Incoterms Plus',
    'version': '12.0.2.1.2',
    'category': 'Accounting',
    'summary': 'Incoterms Plus',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale',
        'sale_stock',
        'sale_partner_incoterm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/res_config.xml',
    ],
    'installable': True,
}
