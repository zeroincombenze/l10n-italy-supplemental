#
# Copyright 2016-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from logging import getLogger

from os0 import os0

from odoo import api, models

logger = getLogger(__name__)


class IrActionsReport(models.Model):
    # The old abstract `report` helper model these methods lived on was
    # folded into `ir.actions.report` long before 18.0; the pure
    # attribute-lookup/selection-rule logic below has no other
    # version-specific dependency and is ported as-is (`@api.multi`
    # dropped, `self.env.user.company_id` -> `self.env.company`).
    #
    # NOT ported (see below): `render()`/`get_html()`/`get_pdf()`. Those
    # overrode the pre-14.0 report-rendering pipeline
    # (`report.render/get_html/get_pdf(self, docids, report_name, data)`),
    # which no longer exists in this shape -- rendering now goes through
    # `ir.actions.report._render_qweb_html/_render_qweb_pdf(self,
    # report_ref, res_ids, data=None)` classmethods with a materially
    # different contract. They also depended on Python-2-only `StringIO`
    # and the long-abandoned `pyPdf` library. Re-implementing the
    # watermark/ending-page PDF overlay feature against the current
    # rendering hooks is a real redesign, not a mechanical port; flagged
    # here rather than guessed. `stock.delivery.note.get_docs_to_attach()`
    # (a simpler, self-contained PDF merge) was however modernized to the
    # current `pypdf` API in models/stock_delivery_note.py.
    _inherit = "ir.actions.report"

    RPT_BY_MODEL = {
        "sale.order": "sale.report_saleorder",
        "account.invoice": "account.report_invoice",
        "stock.picking.package.preparation": "l10n_it_ddt.report_ddt",
        "purchase.order": "purchase.report_purchaseorder_document",
        "stock.picking": "stock.report_picking",
    }
    BOOL_PARAMS = [
        "no_header_logo",
    ]
    DEFAULT_VALUES = {
        "logo_style": "max-height: 45px;",
        "custom_footer": "$company.rml_footer",
    }

    @api.model
    def select_reportname(self, document, force=True):
        model_name = document._name
        rule_model = self.env["multireport.selection.rules"]
        ir_model_model = self.env["ir.model"]
        ir_ui_view_model = self.env["ir.ui.view"]
        model_id = ir_model_model.search([("model", "=", model_name)])
        if model_id:
            domain = [
                ("active", "=", True),
                "|",
                ("model_id", "=", model_id.id),
                ("model_name", "=", model_name),
            ]
        else:
            domain = [("active", "=", True)]
        reportname = self.RPT_BY_MODEL.get(model_name, None) if force else None
        for rule in rule_model.search(domain, order="sequence"):
            if rule.action == "odoo":
                break
            elif rule.action == "report" and rule.report_id:
                reportname = ir_ui_view_model.browse(rule.report_id.id).xml_id
                break
        return reportname

    @api.model
    def get_doc_n_repo_params(self, document, report):
        reportname = self.select_reportname(document, force=True)
        company = False
        report_model_style = False
        if hasattr(document, "company_id"):
            company = document.company_id or self.env.company
            report_model_style = company.report_model_style or None
        if hasattr(document, "pdf_report"):
            pdf_report = document.pdf_report
        else:
            pdf_report = False
        return reportname, company, report_model_style, pdf_report

    @api.model
    def get_report_attrib(self, param, doc, report):
        def get_obj_value(param, object=None, ttype=None):
            value = False
            params = param.split(".")
            if len(params) == 2:
                object = object or params[0]
                param = params[1]
            elif object is None:
                object = report
            if object:
                if hasattr(object, param):
                    if ttype == "many2one":
                        value = getattr(object, param).name
                    else:
                        value = getattr(object, param)
            if param == "custom_footer" and value == "<p><br></p>":
                value = False
            return value

        reportname, company, report_model_style, pdf_report = self.env[
            "ir.actions.report"
        ].get_doc_n_repo_params(doc, report)
        model = doc._name.replace(".", "_")
        # Fallback value path: report, template, style, partner, company
        value = get_obj_value(param)
        template = False
        if report_model_style and report_model_style.origin != "odoo":
            template_in_style = "template_%s" % model
            if (
                not template
                and report_model_style
                and hasattr(report_model_style, template_in_style)
            ):
                template = getattr(report_model_style, template_in_style)

            if param in ("custom_header", "custom_footer"):
                value = False
            elif hasattr(report, param):
                value = getattr(report, param)
                if param == "custom_footer" and value == "<p><br></p>":
                    value = False
            if not value and template and hasattr(template, param):
                value = getattr(template, param)
                if param == "custom_footer" and value == "<p><br></p>":
                    value = False
        if not value and report_model_style and hasattr(report_model_style, param):
            value = getattr(report_model_style, param)
            if param == "custom_footer" and value == "<p><br></p>":
                value = False
        if param in ("custom_header", "custom_footer") and not value:
            value = get_obj_value(param)
        if param == "footer_mode" and (not value or value == "standard"):
            if company.custom_footer:
                value = "custom"
            else:
                value = "auto"
        elif not value and param in self.DEFAULT_VALUES:
            value = self.DEFAULT_VALUES[param]
            if value.startswith("$company"):
                value = getattr(company, value.split(".")[1])
        if param in self.BOOL_PARAMS:
            value = os0.str2bool(value, True)
        elif param in ("custom_header", "custom_footer"):
            banks = ""
            for bank in company.partner_id.bank_ids:
                if bank.journal_id and any(
                    [x.display_on_footer for x in bank.journal_id]
                ):
                    banks = banks + " </br>" + bank.acc_number
            banks = banks.strip()
            param = {
                "banks": banks,
                "city": company.city,
                "email": company.email,
                "fax": company.fax,
                "name": company.name,
                "phone": company.phone,
                "street": company.street,
                "street2": company.street2,
                "vat": company.vat,
                "website": company.website,
                "zip": company.zip,
            }
            for nm in (
                "codice_destinatario",
                "fatturapa_rea_capital",
                "fatturapa_rea_number",
                "fatturapa_rea_office",
                "fiscalcode",
                "ipa_code",
                "mobile",
            ):
                if hasattr(company.partner_id, nm):
                    param[nm] = getattr(company.partner_id, nm)
                else:
                    param[nm] = ""
            for nm in ("country_id", "state_id"):
                if hasattr(company.partner_id, nm):
                    param[nm] = getattr(company.partner_id, nm).name
                else:
                    param[nm] = ""
            value = value % param
            if param == "custom_header":
                value = 'div class="header">%s</div>' % value
        return value or None
