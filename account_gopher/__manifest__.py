# -*- coding: utf-8 -*-
#
# Copyright 2020-24 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    "name": "Account Assistant",
    "version": "10.0.0.2.9",
    "category": "Localization/Italy",
    "summary": "Configure account records",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
        "l10n_it_ade",
        "l10n_it_einvoice_base",
        "l10n_it_reverse_charge",
    ],
    "data": [
        "wizard/wizard_configure_view.xml",
        "wizard/wizard_reconcile_view.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
