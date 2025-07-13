# -*- coding: utf-8 -*-
#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from base64 import b64decode
from datetime import datetime

from PyPDF2 import PdfFileReader, PdfFileWriter
from StringIO import StringIO

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class StockPickingPackagePreparation(models.Model):
    _inherit = ["stock.picking.package.preparation"]

    report_doc_ids = fields.Many2many(
        "ir.attachment",
        "stock_picking_package_preparation_rel",
        "picking_id",
        "ir_attachment_id",
        string="Documents to be appended to DdT (PDF only):",
        copy=False,
    )

    @api.multi
    def get_docs_to_attach(self):
        """Returns a merged PDF document from a list of all attached PDFs."""
        self.ensure_one()
        new_pdf = PdfFileWriter()
        for pdf_doc in self.report_doc_ids.filtered(
            lambda d: d.mimetype == "application/pdf"
        ).sorted(key="attach_seq"):
            pdf = PdfFileReader(StringIO(b64decode(pdf_doc.datas)))
            for page in pdf.pages:
                new_pdf.addPage(page)
        pdf_content = StringIO()
        new_pdf.write(pdf_content)
        return pdf_content.getvalue()


class StockPickingPackagePreparationLine(models.Model):
    _inherit = ["stock.picking.package.preparation.line", "multireport.mixin"]
    _name = "stock.picking.package.preparation.line"

    def get_order_ref_text(self, doc, report, line):
        order_ref_text = self.env["report"].get_report_attrib(
            "order_ref_text", doc, report
        )
        if not order_ref_text:
            return ""
        lang = self.env["res.lang"].search(
            [("code", "=", line.package_preparation_id.partner_id.lang)]
        )
        if not lang:
            lang = self.env.user.company_id.partner_id.lang
        date_format = lang.date_format
        order_name = ""
        date_order = ""
        client_order_ref = ""
        if line.sale_id:
            date_order = line.sale_id.date_order
            if date_order:
                date_order = datetime.strptime(
                    date_order, DEFAULT_SERVER_DATETIME_FORMAT
                ).strftime(date_format)
            else:
                date_order = ""
            client_order_ref = line.sale_id.client_order_ref or ""
            order_name = line.sale_id.name
        ctx = {
            "order_name": order_name,
            "date_order": date_order,
            "client_order_ref": client_order_ref,
        }
        return order_ref_text % ctx
