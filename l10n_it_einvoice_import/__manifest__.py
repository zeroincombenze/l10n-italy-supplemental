# -*- coding: utf-8 -*-
#
# Copyright 2018-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    "name": "ITA - Fattura elettronica - Importazione fatture di vendita",
    "version": "10.0.1.3.32",
    "category": "Localization/Italy",
    "summary": "E-invoice sale import",
    "author": "SHS-AV s.r.l.,Odoo Community Association (OCA)",
    "website": "https://github.com/zeroincombenze/l10n-italy-supplemental",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_einvoice_in",
        "l10n_it_einvoice_out",
        "account_invoice_force_number",
    ],
    "version_depends": [
        "l10n_it_einvoice_in>=10.0.1.3.62",
        "l10n_it_einvoice_out>=10.0.1.3.32"
    ],
    "external_dependencies": {"python": ["pyxb", "unidecode"]},
    "data": [
        "views/account_view.xml",
        "wizard/wizard_import_fatturapa_view.xml",
        "wizard/wizard_import_zip_view.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
