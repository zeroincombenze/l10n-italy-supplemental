# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    'name': 'ITA - Registri IVA Reverse Charge',
    'version': '12.0.1.0.0',
    'category': 'Localization/Italy',
    'author': 'librERP and other partners',
    'website': 'https://www.librerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'l10n_it_vat_registries',
    ],
    'data': [
        'report/inherit_report.xml'
    ],
    'installable': True,
}
