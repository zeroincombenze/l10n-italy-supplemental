# -*- coding: utf-8 -*-
#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from datetime import datetime

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class AccountInvoice(models.Model):
    _inherit = ["account.invoice"]

    due_records = fields.One2many(
        "account.move.line",
        "invoice_id",
        domain=[("account_id.user_type_id.type", "=", "receivable")],
        string="Due Dates",
        copy=False,
    )

    # Override print_quotation method in sale module
    @api.multi
    def invoice_print(self):
        action = super(AccountInvoice, self).invoice_print()
        reportname = self.env["report"].select_reportname(self)
        if reportname:
            action["reportname"] = reportname
        return action


class AccountInvoiceLine(models.Model):
    _inherit = ["account.invoice.line", "multireport.mixin"]
    _name = "account.invoice.line"

    def get_order_ref_text(self, doc, report, line):
        order_ref_text = self.env["report"].get_report_attrib(
            "order_ref_text", doc, report
        )
        if not order_ref_text:
            return ""
        lang = self.env["res.lang"].search(
            [("code", "=", line.invoice_id.partner_id.lang)]
        )
        if not lang:
            lang = self.env.user.company_id.partner_id.lang
        date_format = lang.date_format
        client_order_ref = ""
        order_name = ""
        date_order = ""
        if line.sale_line_ids:
            date_order = line.sale_line_ids[0].order_id.date_order
            if date_order:
                date_order = datetime.strptime(
                    date_order, DEFAULT_SERVER_DATETIME_FORMAT
                ).strftime(date_format)
            else:
                date_order = ""
            client_order_ref = line.sale_line_ids[0].order_id.client_order_ref or ""
            order_name = line.sale_line_ids.order_id.name
        ctx = {
            "order_name": order_name,
            "date_order": date_order,
            "client_order_ref": client_order_ref,
        }
        return order_ref_text % ctx

    def get_ddt_ref_text(self, doc, report, line):
        ddt_ref_text = self.env["report"].get_report_attrib("ddt_ref_text", doc, report)
        if not ddt_ref_text:
            return ""
        lang = self.env["res.lang"].search(
            [("code", "=", line.invoice_id.partner_id.lang)]
        )
        if not lang:
            lang = self.env.user.company_id.partner_id.lang
        date_format = lang.date_format
        date_ddt = ""
        date_done = ""
        ddt_number = ""
        if line.ddt_line_id:
            date_ddt = line.ddt_line_id.package_preparation_id.date
            if date_ddt:
                date_ddt = datetime.strptime(
                    date_ddt, DEFAULT_SERVER_DATETIME_FORMAT
                ).strftime(date_format)
            else:
                date_ddt = ""
            date_done = line.ddt_line_id.package_preparation_id.date
            if date_done:
                date_done = datetime.strptime(
                    date_done, DEFAULT_SERVER_DATETIME_FORMAT
                ).strftime(date_format)
            else:
                date_done = ""
            ddt_number = line.ddt_line_id.package_preparation_id.ddt_number or ""
        ctx = {
            "ddt_number": ddt_number,
            "date_ddt": date_ddt,
            "date_done": date_done,
        }
        return ddt_ref_text % ctx
