# Copyright 2022 SHS-AV s.r.l. <https://www.zeroincombenze.it/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Fattura elettronica - Ricezione fatture attive",
    "version": "12.0.1.0",
    "category": "Localization/Italy",
    "summary": "Ricezione fatture elettroniche",
    "author": "Odoo Community Association (OCA) and other partners",
    "website": "https://odoo-community.org",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "base_vat_sanitized",
        "l10n_it_fatturapa",
        "l10n_it_withholding_tax_causali",
    ],
    "data": [
        "views/account_view.xml",
        "views/partner_view.xml",
        "wizard/wizard_import_fatturapa_view.xml",
        "wizard/link_to_existing_invoice.xml",
        "views/company_view.xml",
        "security/ir.model.access.csv",
        "security/rules.xml",
    ],
    "installable": True,
}
