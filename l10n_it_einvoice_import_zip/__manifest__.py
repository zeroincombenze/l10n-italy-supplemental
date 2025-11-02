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
    "name": "Fattura elettronica - Import ZIP",
    "summary": "Importazione di file XML di fatture elettroniche da uno ZIP",
    "version": "10.0.1.0.7",
    "category": "Localization/Italy",
    "author": "SHS-AV s.r.l.",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "LGPL-3",
    "depends": [
        "l10n_it_einvoice_base",
        "l10n_it_einvoice_in",
    ],
    "data": [
        "wizard/wizard_import_einvoice_view.xml",
    ],
    "installable": True,
    "development_status": "Alpha",
}
