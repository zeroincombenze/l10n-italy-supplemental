# -*- coding: utf-8 -*-
#
# Copyright 2018-23 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    "name": "Agenzia delle Entrate (italian IRS)",
    "version": "10.0.0.3.10",
    "category": "Localization/Italy",
    "summary": "Codes & Definitions from IRS",
    "author": "SHS-AV s.r.l.",
    "website": "https://github.com/OCA/l10n-italy",
    "development_status": "Beta",
    "license": "LGPL-3",
    "depends": ["account"],
    "external_dependencies": {"python": ["pyxb"]},
    "data": [
        "security/ir.model.access.csv",
        "data/italy_ade_tax_nature.xml",
        "data/italy_ade_codice_carica.xml",
        "data/italy_ade_invoice_type.xml",
        "data/italy_ade_tax_assosoftware.xml",
        "views/ir_ui_menu.xml",
        "views/account_tax_view.xml",
        "views/account_journal.xml",
        "views/codice_carica_view.xml",
        "views/tax_nature_view.xml",
        "views/tax_assosoftware_view.xml",
        "views/invoice_type_view.xml",
        "views/account_invoice_view.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
