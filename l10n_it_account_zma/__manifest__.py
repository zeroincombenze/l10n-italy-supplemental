#
# Copyright 2021-26 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Contabilità base (ZMA)',
    'summary': 'Modulo Zeorincombenze di estesione l10n_it_account',
    'version': '12.0.1.4.5',
    'category': 'Hidden',
    'author': "SHS-AV s.r.l.",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_account',
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_account',
    ],
    "data": [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
}
