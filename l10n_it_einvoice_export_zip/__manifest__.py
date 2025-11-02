# -*- coding: utf-8 -*-
# Copyright 2019 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Fattura elettronica - Export ZIP",
    "summary": "Esportazione di file XML di fatture elettroniche "
    "in uno ZIP da esportare.",
    "version": "10.0.1.0.0",
    "development_status": "Beta",
    "category": "other",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Efatto.it di Sergio Corato, Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "l10n_it_einvoice_out",
        "l10n_it_einvoice_in",
    ],
    "data": [
        "wizard/export_fatturapa_view.xml",
        "views/attachment_view.xml",
    ],
}
