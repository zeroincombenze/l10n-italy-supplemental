# -*- coding: utf-8 -*-
{
    "name": "Send pdf scheduler",
    "version": "10.0.0.1.1",
    "category": "Accounting",
    "summary": "Schedule sending invoice pdf by cron",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Alpha",
    "license": "LGPL-3",
    "depends": ["base", "account"],
    "external_dependencies": {
        "python": ["holidays", ],
    },
    "data": [
        "views/account_invoice_view.xml",
        "views/account_fiscal_position_view.xml",
        "views/res_partner_view.xml",
        "views/config_settings_view.xml",
        "data/ir_cron.xml",
        "data/ir_config_parameter.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
