#
# Copyright 2020-24 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-24 librERP enterprise network <https://www.librerp.it>
# Copyright 2020-24 Didotech s.r.l. <https://www.didotech.com>
#
{
    "name": "Due dates",
    "version": "12.0.4.8.38",
    "category": "Accounting",
    "summary": "Enhanced due dates management",
    "author": "SHS-AV s.r.l.,Didotech s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "account",
        "base",
        "account_due_list",
        "account_move_plus",
        "account_payment_order",
        "account_invoice_13_more",
        "account_move_line_type",
        "date_range_plus",
        "account_payment_term_plus",
        "account_payment_method",
        "account_common_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "view/account_invoice_view.xml",
        "view/account_move_view.xml",
        "view/account_move_line_view.xml",
        "view/account_due_list_view.xml",
        "view/partner_view.xml",
        "view/report_invoice.xml",
        "data/update_year_cron.xml",
        "data/date_range_type.xml",
    ],
    "maintainer": "librERP enterprise network <False>",
    "installable": True,
    "post_init_hook": "post_init_hook",
}
