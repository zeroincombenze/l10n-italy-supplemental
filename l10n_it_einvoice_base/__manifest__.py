# -*- coding: utf-8 -*-
#
# Copyright 2018-21 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    "name": "EInvoice + FatturaPA",
    "version": "10.0.2.1.27",
    "category": "Localization/Italy",
    "summary": "Infrastructure for Italian Electronic Invoice + FatturaPA",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "account",
        "l10n_it_fiscalcode",
        "document",
        "l10n_it_fiscal_ipa",
        "l10n_it_rea",
        "base_iban",
        "l10n_it_ade",
        "l10n_it_pec",
        "l10n_it_fiscal_payment_term",
        "account_invoice_partner_carrier",
    ],
    "external_dependencies": {'python': ['pyxb']},
    "version_external_dependencies": ["pyxb>=1.2.5"],
    "conflicts": ["l10n_it_fatturapa"],
    "data": [
        "security/ir.model.access.csv",
        "data/fatturapa_fiscal_position.xml",
        "data/fatturapa_data.xml",
        "data/welfare.fund.type.xml",
        "data/italy_ade_sender_data.xml",
        "views/account_invoice_view.xml",
        "views/company_view.xml",
        "views/regime_fiscale_view.xml",
        "views/fiscal_position_view.xml",
        "views/fetchmail_view.xml",
        "views/mail_server_view.xml",
        "views/sender_view.xml",
        "views/welfare_fund_type_view.xml",
        "wizard/set_invoice_type_view.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
    "pre_init_hook": "check_4_depending",
}
