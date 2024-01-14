# -*- coding: utf-8 -*-
{
    "name": "Rectify Negative Invoice / Refund",
    "version": "10.0.0.1.1",
    "category": "Accounting",
    "summary": "User can rectify negative invoice or negative refund",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_invoice_check_total",
    ],
    "data": [
        "views/account_invoice_view.xml",
        "views/account_move_view.xml",
    ],
    "maintainer": "Antonio Maria Vigliotti",
    "installable": True,
}
