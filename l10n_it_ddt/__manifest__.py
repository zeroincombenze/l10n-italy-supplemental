# Copyright 2014-2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - DDT invoicing groups",
    "summary": "Choose how delivery notes (DDT) are grouped into invoices",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/crm",
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "license": "AGPL-3",
    "development_status": "Alpha",
    "depends": ["l10n_it_delivery_note"],
    "data": [
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
    ],
    "installable": True,
}
