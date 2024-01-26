# Copyright 2021-24 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
{
    "name": "ITA - Liquidazione IVA evoluta",
    "version": "12.0.1.9.2",
    "category": "Localization/Italy",
    "summary": "Allow to create the 'VAT Statement'",
    "author": "SHS-AV s.r.l.,Didotech s.r.l.",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "account",
        "l10n_it_vat_common",
        "account_tax_balance",
        "date_range_plus",
        "l10n_it_account",
        "l10n_it_fiscalcode",
        "web",
        "l10n_it_account_tax_kind",
        "account_invoice_entry_dates",
        "account_move_plus",
        "account_tax_group_plus",
    ],
    "data": [
        "wizard/add_period.xml",
        "wizard/remove_period.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "report/reports.xml",
        "views/report_vatperiodendstatement.xml",
        "views/config.xml",
        "views/account_view.xml",
        "views/account_move_view.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
