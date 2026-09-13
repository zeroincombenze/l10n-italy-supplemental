# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "multibase_plus",
    "summary": """Enhanced Odoo Features""",
    "description": """
Enhanced Odoo Features
----------------------

This module adds some features in order to make Odoo installation more
enjoyable, with a coherent interface independent from the Odoo version.

  Features                              | 6.1 | 7.0 | 8.0 | 9.0 | 10.0 | 11.0 | 18.0

  Add customer ref in sale.order list   | x   | x   | x   | x   | YES  | x    | N/N

  Add refund (credit note) invoice menu | N/N | N/N | N/N | x   | YES  | N/N  | N/N

Legend:

    x:   not available

    YES: available with this module

    N/N: not needed, already in Odoo core

As of 18.0, both the customer reference column and the credit note menus
already exist natively in Odoo core (the reference/untaxed-amount columns
are optional/hidden columns on the Sales list views; the credit note menus
are ``Accounting > Customers > Credit Notes`` and
``Accounting > Vendors > Credit Notes``). This module now only makes those
core columns visible by default; the old ``account.invoice``-based refund
menus were dropped since the ``account.invoice`` model no longer exists
(merged into ``account.move`` since 13.0) and its exact duplicate is
already provided by Odoo core.
""",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/",
    "category": "Base",
    "version": "18.0.1.0.0",
    "depends": ["base", "sale"],
    "data": [
        "views/sale_order_view.xml",
    ],
    "installable": True,
}
