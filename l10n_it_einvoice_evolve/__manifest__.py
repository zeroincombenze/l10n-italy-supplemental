#
# Copyright 2018-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    "name": "Send E-Invoice through Evolve",
    "version": "12.0.1.0.54",
    "category": "Localization/Italy",
    "summary": "Send sale E-Invoice to customer through Evolve infrastructure",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_sdi_channel",
        # "l10n_it_split_payment",
        "l10n_it_fatturapa_in",
        "l10n_it_fatturapa_out",
    ],
    "external_dependencies": {
        "python": [
            "Crypto.Cipher",
            "pkcs7",
            "os0",
        ],
    },
    "data": [
        # "views/account.xml",
        # "views/attachment_view.xml",
        "views/sdi_channel_view.xml",
        # "data/ir_cron.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
