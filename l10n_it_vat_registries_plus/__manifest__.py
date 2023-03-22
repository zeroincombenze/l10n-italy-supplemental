# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    'name': 'ITA - Registri IVA Extended',
    'version': '12.0.1.0.5',
    'category': 'Localization/Italy',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'l10n_it_vat_registries',
        'account_move_number',
    ],
    'data': ['wizard/wizard_confirm_print_journal.xml'],
    'installable': True,
}
