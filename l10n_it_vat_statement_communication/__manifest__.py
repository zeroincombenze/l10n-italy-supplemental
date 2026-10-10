# -*- coding: utf-8 -*-
# Copyright 2017-25 Alessandro Camilli - Openforce
# Copyright 2017-2019 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "ITA - Comunicazione liquidazione IVA",
    "version": "10.0.1.5.6",
    "category": "Account",
    "summary": "Esportazione file xml LIPE",
    "author": ("Openforce di Camilli Alessandro,Odoo Community Association (OCA)"
               ",SHS-AV s.r.l."),
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Alpha",
    "license": "LGPL-3",
    "depends": [
        "account_vat_period_end_statement",
        "l10n_it_ade",
        "l10n_it_fiscalcode",
        "l10n_it_account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/comunicazione_liquidazione.xml",
        "views/config.xml",
        "views/account.xml",
        "views/report_comunicazione.xml",
        "report/report_statement.xml",
        "wizard/export_file_view.xml",
        "security/security.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
