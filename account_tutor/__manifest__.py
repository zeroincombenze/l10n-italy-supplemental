# -*- coding: utf-8 -*-
#
# Copyright 2020-21 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
{
    'name': 'Account Tutor',
    'version': '10.0.0.1.0',
    'category': 'Localization/Italy',
    'summary': 'Configure account records',
    'author': 'SHS-AV s.r.l.',
    'website': 'https://www.zeroincombenze.it',
    'development_status': 'Beta',
    'license': 'LGPL-3',
    'depends': ['base', 'account', 'l10n_it_ade', 'l10n_it_einvoice_base'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_tutor_menu.xml',
        'wizard/wizard_configure_view.xml',
    ],
    'maintainer': 'Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>',
    'installable': True,
}
