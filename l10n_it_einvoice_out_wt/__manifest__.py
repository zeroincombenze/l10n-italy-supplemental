# -*- coding: utf-8 -*-
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - E-Invoice - Withholding tax integration",
    "version": "10.0.1.0.1",
    "category": "Hidden",
    "summary": "Bridge module between e-invoice and withholding tax",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_einvoice_base",
        "l10n_it_einvoice_out",
        "l10n_it_withholding_tax",
    ],
    "version_depends": ["l10n_it_einvoice_out>=10.0.1.0.29"],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
    "pre_init_hook": "check_4_depending",
    "auto_install": True,
}
