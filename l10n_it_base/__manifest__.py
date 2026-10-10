# -*- coding: utf-8 -*-
#
# Copyright 2017-2018, Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# Copyright 2010-2018, Associazione Odoo Italia <https://odoo-italia.org>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
{
    "name": "Italian Localisation - Base",
    "version": "10.0.0.2.18",
    "category": "Generic Modules/Accounting",
    "summary": "Managing Italian addresses",
    "author": ("Odoo Community Association (OCA),Pexego,Agile Business Group sagl"
               ",Innoviu Srl,SHS-AV s.r.l."),
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Alpha",
    "license": "LGPL-3",
    "depends": [
        "base",
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "views/city_view.xml",
        "data/res.city.xml",
    ],
    "maintainer": "Antonio Maria Vigliotti",
    "installable": True,
}
