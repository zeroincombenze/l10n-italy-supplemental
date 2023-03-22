# Copyright 2021-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    "name": "Account validations",
    "version": "12.0.1.9.29",
    "category": "Accounting",
    "summary": "Account validation for Italian Localization",
    "author": "powERP enterprise network and other partners",
    "website": "https://github.com/OCA/l10n-italy",
    "development_status": "Beta",
    "license": "LGPL-3",
    "depends": [
        "account",
        "base",
        "date_range_plus",
        "account_invoice_entry_dates",
        "account_move_plus",
        "account_invoice_13_more",
        "account_fiscal_year_plus",
    ],
    "data": ["views/account_invoice_view.xml"],
    "installable": True,
}
