# -*- coding: utf-8 -*-
#
# Copyright 2016-15    - AgileBG SAGL <http://www.agilebg.com>
# Copyright 2016-15    - innoviu Srl <http://www.innoviu.com>
# Copyright 2018       - Lorenzo Battistini
# Copyright 2018       - Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2018-19 - Odoo Italia Associazione <https://www.odoo-italia.org>
# Copyright 2018-26 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
{
    "name": "ITA - Fattura elettronica - Ricezione",
    "version": "10.0.1.3.58",
    "category": "Localization/Italy",
    "summary": "E-invoice receive",
    "author": (
        "Agile Business Group sagl,Innoviu srl,Pointec s.r.l.,SHS-AV s.r.l."
        ",Odoo Community Association (OCA),Innoviu Srl"
    ),
    "website": "https://github.com/OCA/l10n-italy/l10n_it_fatturapa_in",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_invoice_partner_carrier",
        "l10n_it_account",
        "l10n_it_ade",
        "account_invoice_check_total",
        "l10n_it_einvoice_base",
        "l10n_it_fiscal_ipa",
        "l10n_it_causali_pagamento",
        "l10n_it_reverse_charge",
        "l10n_it_withholding_tax",
    ],
    "version_depends": ["l10n_it_einvoice_base>=10.0.2.1.26"],
    "data": [
        "security/ir.model.access.csv",
        "data/product.xml",
        "views/account_view.xml",
        "views/partner_view.xml",
        "views/company_view.xml",
        "wizard/wizard_import_fatturapa_view.xml",
        "wizard/attachment_refresh_info_view.xml",
        "wizard/link_to_existing_invoice.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
