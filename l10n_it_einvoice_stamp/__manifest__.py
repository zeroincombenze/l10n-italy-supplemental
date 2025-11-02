# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Enrico Ganzaroli (enrico.gz@gmail.com)
# Copyright 2018 Ermanno Gnan (ermannognan@gmail.com)
# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# Copyright 2018 Sergio Zanchetta (https://github.com/primes2h)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Italian Localization - Tax Stamp",
    "summary": "Tax stamp automatic management",
    "version": "10.0.1.0.5",
    "category": "Localization/Italy",
    "author": "Odoo Community Association (OCA) and other subjects",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "LGPL-3",
    "depends": [
        "product",
        "account",
        "l10n_it_einvoice_out",
    ],
    "data": [
        "data/data.xml",
        "views/invoice_view.xml",
        "views/product_view.xml",
        "views/company_view.xml",
        "report/stamp_statement.xml",
    ],
    "installable": True,
    "development_status": "Beta",
}
