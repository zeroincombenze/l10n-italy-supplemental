# -*- coding: utf-8 -*-
#
# Copyright 2020-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
{
    "name": "Italian Localization - Fattura elettronica - Import",
    "version": "110.0.1.3.30",
    "category": "Localization/Italy",
    "summary": "Import fatture elettroniche clienti",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account",
        "l10n_it_ade",
        "account_invoice_check_total",
        "l10n_it_einvoice_base",
        "l10n_it_fiscal_ipa",
        "l10n_it_causali_pagamento",
        "l10n_it_einvoice_out",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_view.xml",
        "wizard/wizard_import_fatturapa_view.xml",
        "wizard/attachment_refresh_info_view.xml",
        "wizard/link_to_existing_invoice.xml",
    ],
    "installable": False,
}
