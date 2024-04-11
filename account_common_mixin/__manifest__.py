#
# Copyright 2020-24 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-24 Didotech s.r.l. <https://www.didotech.com>
#
{
    "name": "Account Common Mixin",
    "version": "12.0.1.0.1",
    "category": "Accounting",
    "summary": "Common account fields",
    "author": "SHS-AV s.r.l.,Didotech s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_invoice_13_more",
        "assigned_bank",
        "l10n_it_fiscal_payment_term",
    ],
    "data": [
        "views/account_move_view.xml",
        "views/account_invoice_view.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
