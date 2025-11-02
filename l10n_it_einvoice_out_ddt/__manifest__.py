# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "ITA - Fattura elettronica - Integrazione DDT",
    "version": "10.0.1.0.3",
    "category": "Hidden",
    "summary": "Modulo ponte tra emissione fatture elettroniche e DDT",
    "author": "Agile Business Group,Odoo Community Association (OCA),SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_einvoice_out",
        "l10n_it_ddt",
    ],
    "data": ["wizard/wizard_export_fatturapa_view.xml"],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
    "application": False,
}
