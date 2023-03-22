# Copyright 2021-2022 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later
#   https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps)
#
{
    "name": "l10n_it_mastrini",
    "version": "12.0.10.12.34",
    "category": "Mastrini",
    "summary": "Mastrini",
    "author": "powERP enterprise network and other partners",
    "website": "https://www.powerp.it",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
        "date_range_plus",
        "l10n_it_coa_base",
        "l10n_it_menu",
        "l10n_it_validations",
        "account_accrual_dates",
    ],
    "data": [
        "wizard/account_mastrini.xml",
        "views/ir_ui_menu.xml",
    ],
    "installable": True,
}
