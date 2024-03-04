#
# Copyright 2020-24 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
{
    "name": "Assigned Banks",
    "version": "12.0.0.2.2",
    "category": "Generic Modules/Accounting",
    "summary": "Assign internal banks to customer or supplier",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "LGPL-3",
    "depends": [
        "base",
        "account",
    ],
    "data": [
        "views/res_config_settings_views.xml",
        "views/partner_view.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
