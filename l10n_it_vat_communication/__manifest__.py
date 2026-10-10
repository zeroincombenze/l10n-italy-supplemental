# -*- coding: utf-8 -*-
# Copyright (C) 2017-22    SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    "name": "Comunicazione periodica IVA",
    "version": "10.0.0.2.4",
    "category": "Generic Modules/Accounting",
    "author": "SHS-AV s.r.l.",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account_cancel",
        "account_period",
        "l10n_it_ade",
        "l10n_it_fiscalcode",
        # "account_invoice_entry_date",
        "date_range",
    ],
    "external_dependencies": {"python": ["pyxb", "unidecode"]},
    "data": [
        "security/ir.model.access.csv",
        "wizard/views/add_period.xml",
        "wizard/views/remove_period.xml",
        "views/account_view.xml",
        "wizard/views/wizard_export_view.xml",
        "wizard/views/set_invoice_commtype_view.xml",
    ],
    "installable": True,
    "maintainer": "Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>",
}
