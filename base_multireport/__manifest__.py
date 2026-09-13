# -*- coding: utf-8 -*-
#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
{
    "name": "base_rule_multireport",
    "version": "18.0.1.0.0",
    "category": "Generic Modules/Accounting",
    "summary": "Manage document multiple reports",
    "author": "SHS-AV s.r.l.",
    "website": "https://github.com/OCA/l10n-italy",
    "development_status": "Alpha",
    "license": "LGPL-3",
    "depends": [
        "base",
        "account",
        "sale",
        "purchase",
        # NOTE (unresolved, out of this migration's scope): the four
        # deps below have no confirmed 18.0 equivalent in this
        # environment (they stop at 16.0 in the l10n-italy checkouts
        # available here, likely superseded by the l10n_it_edi* core
        # modules similarly to l10n_it_fatturapa -- see account_gopher's
        # migration notes). l10n_it_ddt -> l10n_it_delivery_note is the
        # one rename that *is* confirmed and applied throughout this
        # module's code.
        "l10n_it_fiscalcode",
        "l10n_it_delivery_note",
        "l10n_it_ade",
        "l10n_it_ricevute_bancarie",
        "l10n_it_einvoice_base",
    ],
    "external_dependencies": {
        "python": [
            "pypdf",
            "os0",
        ],
    },
    "data": [
        "security/ir.model.access.csv",
        "data/multireport_style.xml",
        "data/multireport_template.xml",
        "data/multireport_selection_rules.xml",
        "wizard/wizard_build_report_view.xml",
        "views/multireport_style_view.xml",
        "views/ir_actions_report_xml_view.xml",
        "views/multireport_template_view.xml",
        "views/multireport_selection_rules_view.xml",
        "views/config_view.xml",
        "report/paper_format.xml",
        "report/header-footer.xml",
        "report/multireport_sale_order.xml",
        "report/multireport_ddt.xml",
        "report/multireport_invoice.xml",
        "report/multireport_purchase_order.xml",
        "report/multireport_picking.xml",
        "report/multireport_overdue.xml",
        "report_ddt/report_ddt.xml",
        "report_ddt/report_ddt_header.xml",
        "report_ddt/report_ddt_lines.xml",
        "report_ddt/report_ddt_footer.xml",
        "report_sale_order/report_sale_order.xml",
        "report_sale_order/report_sale_order_header.xml",
        "report_sale_order/report_sale_order_lines.xml",
        "report_sale_order/report_sale_order_footer.xml",
        "report_account_invoice/report_invoice.xml",
        "report_account_invoice/report_invoice_header.xml",
        "report_account_invoice/report_invoice_lines.xml",
        "report_account_invoice/report_invoice_footer.xml",
        "report_purchase_order/report_purchase_order.xml",
        "report_purchase_order/report_purchase_order_header.xml",
        "report_purchase_order/report_purchase_order_lines.xml",
        "report_purchase_order/report_purchase_order_footer.xml",
        "report_overdue/report_overdue.xml",
        "report_picking/report_deliveryslip.xml",
        "report_picking/report_stockpicking_operations.xml",
    ],
    # Was views/layout_templates.xml, inheriting the (now-removed)
    # `report.assets_pdf` QWeb assets template (15.0 boundary: asset
    # links move out of templates into the manifest).
    "assets": {
        "web.report_assets_pdf": [
            "base_multireport/static/src/css/report_qweb_pdf_watermark.css",
        ],
    },
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
    "post_init_hook": "update_template_ref_post",
}
