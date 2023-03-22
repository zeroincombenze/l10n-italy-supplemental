# -*- coding: utf-8 -*-
#
# Copyright 2019-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    'name': 'Fattura elettronica - Import ZIP',
    'summary': 'Importazione di file XML di fatture elettroniche da uno ZIP',
    'version': '12.0.1.0.4',
    'category': 'Localization/Italy',
    'author': 'SHS-AV s.r.l.',
    'website': 'https://www.zeroincombenze.it/servizi-le-imprese/',
    'license': 'LGPL-3',
    'depends': [
        'l10n_it_fatturapa',
        'l10n_it_fatturapa_in',
    ],
    'data': [
        'wizard/wizard_import_einvoice_view.xml',
    ],
    'installable': True,
    'development_status': 'Alpha',
}
