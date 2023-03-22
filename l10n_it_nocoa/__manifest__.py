# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Italy - Fiscal localization',
    'version': '12.0.0.1.3',
    'category': 'Localization/Account Charts',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'OPL-1',
    'depends': [
        'account',
        'base_vat',
        'base_iban',
        'payment',
    ],
    'data': [
        'data/l10n_it_chart_data.xml',
        'data/account.account.template.csv',
        'data/account.tax.template.csv',
        'data/account.chart.template.csv',
        'data/account_chart_template_data.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
