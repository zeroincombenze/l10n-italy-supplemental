#
# Copyright 2020-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
{
    'name': 'Account Assistant',
    'version': "14.0.1.0.0",
    'category': 'Localization/Italy',
    'summary': 'Configure account records',
    'author': 'SHS-AV s.r.l.',
    'website': 'https://www.zeroincombenze.it',
    'development_status': 'Beta',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'l10n_it_account_tax_kind',
        'l10n_it_fatturapa',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_gopher_menu.xml',
        'views/tax_assosoftware_view.xml',
        'wizard/wizard_configure_view.xml',
        'data/italy_ade_tax_assosoftware.xml',
    ],
    'maintainer': 'Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>',
    'installable': True,
}
