# -*- coding: utf-8 -*-
#
# Copyright 2018-23 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    "name": "Send E-Invoice to SdI",
    "version": "10.0.1.0.62",
    "category": "Localization/Italy",
    "summary": "Send E-Invoice to customer through SdI",
    "author": "SHS-AV s.r.l.,Pointec s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_einvoice_base",
        "l10n_it_split_payment",
        "l10n_it_einvoice_in",
        "l10n_it_einvoice_out",
    ],
    "external_dependencies": {'python': ['Crypto.Cipher', 'pkcs7', 'os0']},
    "data": [
        "views/account.xml",
        "views/attachment_view.xml",
        "views/sender_view.xml",
        "data/ir_cron.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
