# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "CRM lead Area",
    "version": "10.0.1.0.1",
    "category": "Customer Relationship Management",
    "summary": "Assign CRM lead to Commercial Area",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/crm",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "partner_area",
        "account",
        "crm",
        "sale",
        "sale_crm"
    ],
    "data": [
        "views/crm_lead_view.xml",
        "views/sale_order_view.xml",
        "views/account_invoice_view.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
    "application": False,
}
