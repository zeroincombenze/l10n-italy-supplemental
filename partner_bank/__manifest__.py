# -*- coding: utf-8 -*-
#
# Copyright 2018-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    "name": "Bank account in partner",
    "version": "10.0.0.3",
    "category": "Accounting & Finance",
    "summary": "Add bank account sheet in partner view like previous Odoo 10.0",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "LGPL-3",
    "depends": [
        "base",
        "base_iban",
        "account",
    ],
    "data": [
        "views/res_partner_view.xml",
        "views/account_invoice_view.xml",
        "views/bank_view.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "application": True,
}
