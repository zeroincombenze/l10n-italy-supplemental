# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
{
    'name': 'Assets into balance',
    'version': '12.0.1.0.11',
    'category': 'Generic Modules/Accounting',
    'summary': 'Account balance with assets',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'assets_management',
        'l10n_it_balance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/generate_balance_view.xml',
        'wizard/wizard_confirm_depreciation.xml',
    ],
    'installable': True,
}
