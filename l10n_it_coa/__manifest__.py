# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Italy - Fiscal localization by Powerp',
    'version': '12.0.0.2.10',
    'category': 'Localization/Account Charts',
    'author': 'powERP enterprise network, SHS-AV s.r.l.',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'base_vat',
        'base_iban',
    ],
    'data': [
        'data/l10n_it_chart_data.xml',
        'data/account.group.xml',
        'data/account.account.template.csv',
        'data/account.tax.group.csv',
        'data/account.tax.template.csv',
        'data/account.fiscal.position.template.csv',
        'data/account.chart.template.csv',
        'data/account_chart_template_data.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
