# -*- coding: utf-8 -*-
#
# Copyright 2014    - Davide Corio
# Copyright 2015-16 - Lorenzo Battistini - Agile Business Group
# Copyright 2018-19 - Odoo Italia Associazione <https://www.odoo-italia.org>
# Copyright 2018-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
{
    "name": "Italian Localization - FatturaPA - Emissione",
    "version": "10.0.1.0.30",
    "category": "Localization/Italy",
    "summary": "E-Invoice emission",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_einvoice_base",
    ],
    "version_depends": ["l10n_it_einvoice_base>=10.0.2.1.27"],
    "external_dependencies": {'python': ['unidecode']},
    "data": [
        "wizard/wizard_export_fatturapa_view.xml",
        "wizard/attachment_refresh_info_view.xml",
        "views/attachment_view.xml",
        "views/account_view.xml",
        "security/ir.model.access.csv",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
    "pre_init_hook": "check_4_depending",
}
