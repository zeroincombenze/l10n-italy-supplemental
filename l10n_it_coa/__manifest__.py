# -*- coding: utf-8 -*-
{
    "name": "ITA - Fiscal localization by Zeroincombenze(R)",
    "version": "10.0.0.2.11",
    "category": "Localization/Account Charts",
    "summary": "ITA - Fiscal localization by Zeroincombenze(R)",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Production/Stable",
    "license": "AGPL-3",
    "depends": [
        "account_group",
        "base_vat",
        "base_iban",
    ],
    "data": [
        "data/l10n_it_chart_data.xml",
        "data/account.group.xml",
        "data/account.account.template.csv",
        "data/account.tax.group.csv",
        "data/account.tax.template.csv",
        "data/account.fiscal.position.template.csv",
        "data/account.chart.template.csv",
        "data/account_chart_template_data.yml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
    "application": True,
}
