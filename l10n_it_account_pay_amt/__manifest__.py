# -*- coding: utf-8 -*-
# Copyright 2021-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Importo netto a pagare (RC/SP/RA)",
    "version": "12.0.1.0.0",
    "category": "Hidden",
    "summary": "Combines split payment, reverse charge and withholding tax"
    " into a single Amount Net to Pay",
    "author": "Zeroincombenze srls",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_account_zma",
        "l10n_it_split_payment",
        "l10n_it_reverse_charge",
        "l10n_it_withholding_tax",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
