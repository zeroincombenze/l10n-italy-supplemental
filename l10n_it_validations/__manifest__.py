# Copyright 2021-23 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-23 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-23 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
{
    "name": "Account validations",
    "version": "12.0.1.9.30",
    "category": "Accounting",
    "summary": "Account validation for Italian Localization",
    "author": "LibrERP enterprise network,SHS-AV s.r.l.,Didotech s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "AGPL-3",
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
    "maintainer": "LibrERP enterprise network",
    "installable": True,
}
