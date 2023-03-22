#
# Copyright 2022 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
{
    'name': 'Prodotti Espresso',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Prodotti espresso',
    'author': 'SHS-AV s.r.l. and other partners',
    'website': '',
    'development_status': 'Beta',
    'license': 'OPL-1',
    'depends': [
        'base',
        'sale',
        'l10n_it_delivery_note',
        'l10n_it_delivery_note_base',
        'l10n_it_delivery_note_batch',
    ],
    'data': [
        'views/product_views.xml',
        'views/action_generate_ddt.xml',
    ],
    'installable': True,
}
