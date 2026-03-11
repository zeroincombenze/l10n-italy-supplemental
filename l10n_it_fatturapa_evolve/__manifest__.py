#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Fattura elettronica - Supporto Evolve",
    "version": "12.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Invio fatture elettroniche tramite Evolve",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_fatturapa_in",
        "l10n_it_sdi_channel",
    ],
    "external_dependencies": {'python': ['Crypto.Cipher', 'pkcs7', 'python_plus']},
    "data": [
        "views/sdi_view.xml",
        "data/sdi_channel_data.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
}
