# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
{
    "name": "Sale Order Line Quantity Policy",
    "summary": "Declare sale order line delivered or invoiced by product policy",
    "version": "10.0.0.1.6",
    "category": "Sales",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        "views/product_view.xml",
        "views/sale_order_view.xml",
    ],
    "maintainer": "Antonio Maria Vigliotti",
    "installable": True,
}
