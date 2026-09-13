#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from base64 import b64decode
from io import BytesIO

from pypdf import PdfWriter

from odoo import fields, models


class StockDeliveryNote(models.Model):
    # l10n_it_ddt's stock.picking.package.preparation was renamed/
    # restructured into l10n_it_delivery_note's stock.delivery.note.
    _inherit = "stock.delivery.note"

    report_doc_ids = fields.Many2many(
        "ir.attachment",
        "stock_picking_package_preparation_rel",
        "picking_id",
        "ir_attachment_id",
        string="Documents to be appended to DdT (PDF only):",
        copy=False,
    )

    def get_docs_to_attach(self):
        """Returns a merged PDF document from a list of all attached PDFs."""
        self.ensure_one()
        new_pdf = PdfWriter()
        for pdf_doc in self.report_doc_ids.filtered(
            lambda d: d.mimetype == "application/pdf"
        ).sorted(key="attach_seq"):
            new_pdf.append(BytesIO(b64decode(pdf_doc.datas)))
        pdf_content = BytesIO()
        new_pdf.write(pdf_content)
        return pdf_content.getvalue()


class StockDeliveryNoteLine(models.Model):
    _inherit = ["stock.delivery.note.line", "multireport.mixin"]
    _name = "stock.delivery.note.line"

    def get_order_ref_text(self, doc, report, line):
        order_ref_text = self.env["ir.actions.report"].get_report_attrib(
            "order_ref_text", doc, report
        )
        if not order_ref_text:
            return ""
        lang = self.env["res.lang"].search(
            [("code", "=", line.delivery_note_id.partner_id.lang)]
        )
        if not lang:
            lang = self.env.company.partner_id.lang
        date_format = lang.date_format
        order_name = ""
        date_order = ""
        client_order_ref = ""
        if line.sale_line_id:
            order = line.sale_line_id.order_id
            date_order = self._fmt_date_macro(order.date_order, date_format)
            client_order_ref = order.client_order_ref or ""
            order_name = order.name
        ctx = {
            "order_name": order_name,
            "date_order": date_order,
            "client_order_ref": client_order_ref,
        }
        return order_ref_text % ctx
