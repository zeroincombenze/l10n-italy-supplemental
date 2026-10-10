# -*- coding: utf-8 -*-
#
# Copyright 2019-24 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    "name": "Lettere di intento",
    "version": "10.0.0.1.11",
    "category": "Generic Modules/Accounting",
    "summary": "Lettere di intento",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Alpha",
    "license": "LGPL-3",
    "depends": [
        "base",
        "l10n_it_einvoice_stamp",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/italy_lettera_intento_view.xml",
        "views/account_fiscal_position_view.xml",
        "views/config_view.xml",
        "views/account_invoice_view.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
