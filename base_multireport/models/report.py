# -*- coding: utf-8 -*-
#
# Copyright 2016-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from base64 import b64decode
from logging import getLogger

# from PIL import PdfImagePlugin # flake8: noqa
from os0 import os0
from PIL import Image
from pyPdf import PdfFileReader, PdfFileWriter
from pyPdf.utils import PdfReadError
from StringIO import StringIO

from odoo import api, models, tools

logger = getLogger(__name__)


class Report(models.Model):
    _inherit = "report"

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
        # model = document.__class__.__name__
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
            if rule.action == "odoo":   # pragma: no cover
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
            company = document.company_id or self.env.user.company_id
            report_model_style = company.report_model_style or None
        if hasattr(document, "pdf_report"):   # pragma: no cover
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
            if param == "custom_footer" and value == "<p><br></p>":   # pragma: no cover
                value = False
            return value

        reportname, company, report_model_style, pdf_report = self.env[
            "report"
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
                    value = False   # pragma: no cover
            if not value and template and hasattr(template, param):
                value = getattr(template, param)
                if param == "custom_footer" and value == "<p><br></p>":
                    value = False  # pragma: no cover
        if not value and report_model_style and hasattr(report_model_style, param):
            value = getattr(report_model_style, param)
            if param == "custom_footer" and value == "<p><br></p>":
                value = False  # pragma: no cover
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

    @api.multi
    def render(self, template, values=None):
        if "report" not in values:  # pragma: no cover
            values["report"] = self
        return super(Report, self).render(template, values=values)

    @api.model
    def get_html(self, docids, report_name, data=None):
        """This method generates and returns html version of a report."""
        report_model_name = "report.%s" % report_name
        report_model = self.env.get(report_model_name)
        if report_model is not None:  # pragma: no cover
            return super(Report, self).get_html(docids, report_name, data=data)
        else:
            report = self._get_report_from_name(report_name)
            docs = self.env[report.model].browse(docids)
            company = False
            if "company_id" in docs[0]:
                company = docs[0].company_id
            if not company:  # pragma: no cover
                company = self.env.user.company_id
            docargs = {
                "doc_ids": docids,
                "doc_model": report.model,
                "docs": docs,
                "doc_opts": report,
                "doc_style": company.report_model_style,
                "res_company": company,
                "report": self,
            }
            return self.render(report.report_name, docargs)

    @api.model
    def get_pdf(self, docids, report_name, html=None, data=None):  # pragma: no cover
        result = super(Report, self).get_pdf(docids, report_name, html=html, data=data)
        if not docids:
            return result
        report = self._get_report_from_name(report_name)
        if report.model not in self.RPT_BY_MODEL:
            return result
        recs = self.env[report.model].browse(docids)
        reportname, company, report_model_style, pdf_report = self.env[
            "report"
        ].get_doc_n_repo_params(recs[0], report)
        if (
            not report_model_style
            or not report_model_style.origin
            or report_model_style.origin == "odoo"
        ) and not pdf_report:
            return result
        watermark = self.get_report_attrib("pdf_watermark", recs[0], report)
        if not watermark:
            watermark = tools.safe_eval(
                self.get_report_attrib("pdf_watermark_expression", recs[0], report)
                or "None",
                dict(env=self.env, docs=recs),
            )
        if watermark:
            watermark = b64decode(watermark)
        ending_page = self.get_report_attrib("pdf_ending_page", recs[0], report)
        if ending_page:
            ending_page = b64decode(ending_page)
        if not watermark and not ending_page:
            return result

        pdf = PdfFileWriter()
        pdf_watermark = None
        try:
            pdf_watermark = PdfFileReader(StringIO(watermark))
        except PdfReadError:
            # let's see if we can convert this with pillow
            try:
                Image.init()
                image = Image.open(StringIO(watermark))
                pdf_buffer = StringIO()
                if image.mode != "RGB":
                    image = image.convert("RGB")
                resolution = image.info.get("dpi", report.paperformat_id.dpi or 90)
                if isinstance(resolution, tuple):
                    resolution = resolution[0]
                image.save(pdf_buffer, "pdf", resolution=resolution)
                pdf_watermark = PdfFileReader(pdf_buffer)
            except BaseException:
                logger.exception("Failed to load watermark")

        if not pdf_watermark:
            logger.error("No usable watermark found, got %s...", watermark[:100])
            return result

        if pdf_watermark.numPages < 1:
            logger.error("Your watermark pdf does not contain any pages")
            return result
        if pdf_watermark.numPages > 1:
            logger.debug(
                "Your watermark pdf contains more than one page, "
                "all but the first one will be ignored"
            )

        doc = PdfFileReader(StringIO(result))
        for page in doc.pages:
            watermark_page = pdf.addBlankPage(
                page.mediaBox.getWidth(), page.mediaBox.getHeight()
            )
            watermark_page.mergePage(pdf_watermark.getPage(0))
            watermark_page.mergePage(page)

        if ending_page:
            pdf_last_page = PdfFileReader(StringIO(ending_page))
            if not pdf_watermark and not recs:
                for page in doc.pages:
                    pdf.addPage(page)
            for last in pdf_last_page.pages:
                pdf.addPage(last)

        pdf_content = StringIO()
        pdf.write(pdf_content)

        return pdf_content.getvalue()
