# -*- coding: utf-8 -*-
#
# Copyright 2022-23 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
{
    "name": "Prodotti Espresso",
    "version": "10.0.1.0.6",
    "category": "Accounting",
    "summary": "Prodotti espresso",
    "author": "SHS-AV s.r.l.",
    "website": "",
    "development_status": "Beta",
    "license": "LGPL-3",
    "depends": [
        "base",
        "sale",
        "mrp",
        "l10n_it_ddt",
    ],
    "data": [
        "views/product_views.xml",
        "views/stock_picking_package_preparation.xml",
        "views/account_invoice_view.xml",
        "views/sale_order_view.xml",
        "views/action_generate_ddt.xml",
        "wizard/wizard_create_ddt_espresso_view.xml",
        "data/ir_cron.xml",
        "report/account_invoice_report_view.xml",
        "report/sale_order_report_view.xml",
    ],
    "installable": True,
}
