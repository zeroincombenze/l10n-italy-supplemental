# -*- coding: utf-8 -*-
#
# Copyright 2019-24 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    "name": "CONAI Management",
    "summary": "CONAI data and amount evalutation",
    "version": "10.0.0.1.15",
    "category": "Localization/Italy",
    "author": "SHS-AV s.r.l.",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account",
        "l10n_it_ddt",
        "sale",
        "stock_picking_package_preparation",
    ],
    "version_depends": ["l10n_it_ddt>=10.0.1.8.26"],
    "data": [
        "security/ir.model.access.csv",
        "data/conai_product_category.xml",
        "data/conai_partner_category.xml",
        "data/product_template.xml",
        # "data/res_company.xml",
        "views/account_config_view.xml",
        "views/product_category_view.xml",
        "views/partner_category_view.xml",
        "views/picking_view.xml",
        "views/account_invoice_view.xml",
        "views/product_view.xml",
        "views/partner_view.xml",
        "views/sale_order_view.xml",
        "views/conai_statement.xml",
        "report/conai_statement.xml",
        # 'views/help_online.xml',
    ],
    "installable": True,
    "maintainer": "Zeroincombenze (R)",
    "development_status": "Beta",
    "application": True,
    "post_init_hook": "set_company_conai_product_post",
    "pre_init_hook": "check_4_depending",
}
