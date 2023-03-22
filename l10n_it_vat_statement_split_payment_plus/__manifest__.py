# Copyright 2018 Silvio Gregorini <silviogregorini@openforce.it>
# Copyright (c) 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright (c) 2019 Matteo Bilotta
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'ITA - Liquidazione IVA + Scissione dei pagamenti plus',
    'version': '12.0.1.0.4',
    'category': 'Accounting & Finance',
    'summary': 'Migliora la liquidazione dell"IVA tenendo in considerazione la scissione dei pagamenti',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_vat_statement',
        'l10n_it_split_payment',
    ],
    'data': ['views/account_config_view.xml'],
    'installable': False,
    'application': False,
    'auto_install': False,
}
