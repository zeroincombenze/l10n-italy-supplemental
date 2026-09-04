# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
{
    "name": "Sale Order Line Quantity Policy - DdT",
    "summary": "Bridge module: quantity policy applied to DdT based invoices",
    "version": "10.0.0.1.2",
    "category": "Hidden",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "depends": [
        "sale_order_line_qty_policy",
        "l10n_it_ddt",
    ],
    "data": [
        "views/stock_picking_package_preparation_view.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "maintainer": "Antonio Maria Vigliotti",
    "installable": True,
    "application": False,
}
