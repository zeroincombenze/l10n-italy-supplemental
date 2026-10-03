# Copyright 2019-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License OPL-1 or later
# (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    "name": "Transnational Account",
    "version": "12.0.0.2.7",
    "category": "Accounting",
    "summary": "Replace standard Odoo validation",
    "author": "Zeroincombenze srls",
    "website": "https://www.zeroincombenze.it",
    "development_status": "Beta",
    "license": "OPL-1",
    "depends": [
        "account",
        "base",
    ],
    "data": [
        "views/account_view.xml",
        "report/style_invoice.xml",
        "report/report_invoice.xml",
        "report/format_report_invoice.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
