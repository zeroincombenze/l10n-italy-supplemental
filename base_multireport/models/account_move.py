#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import fields, models


class AccountMove(models.Model):
    # account.invoice was merged into account.move at 13.0.
    _inherit = "account.move"

    due_records = fields.One2many(
        "account.move.line",
        "move_id",
        domain=[("account_id.account_type", "=", "asset_receivable")],
        string="Due Dates",
        copy=False,
    )

    # NOTE: the `invoice_print()` override that used to live here (to let
    # `report.select_reportname()` swap in an alternate report at
    # print-time) has no direct 18.0 equivalent: account.move no longer
    # has a per-record "print" Python method to intercept the way
    # account.invoice did -- printing goes straight through
    # `ir.actions.report` xmlid actions. See models/report.py for the
    # rest of this gap; not resolved here, flagged instead of guessed.


class AccountMoveLine(models.Model):
    # account.invoice.line was merged into account.move.line at 13.0.
    _inherit = ["account.move.line", "multireport.mixin"]
    _name = "account.move.line"

    def get_order_ref_text(self, doc, report, line):
        order_ref_text = self.env["ir.actions.report"].get_report_attrib(
            "order_ref_text", doc, report
        )
        if not order_ref_text:
            return ""
        lang = self.env["res.lang"].search(
            [("code", "=", line.move_id.partner_id.lang)]
        )
        if not lang:
            lang = self.env.company.partner_id.lang
        date_format = lang.date_format
        client_order_ref = ""
        order_name = ""
        date_order = ""
        if line.sale_line_ids:
            date_order = self._fmt_date_macro(
                line.sale_line_ids[0].order_id.date_order, date_format
            )
            client_order_ref = line.sale_line_ids[0].order_id.client_order_ref or ""
            order_name = line.sale_line_ids.order_id.name
        ctx = {
            "order_name": order_name,
            "date_order": date_order,
            "client_order_ref": client_order_ref,
        }
        return order_ref_text % ctx

    def get_ddt_ref_text(self, doc, report, line):
        ddt_ref_text = self.env["ir.actions.report"].get_report_attrib(
            "ddt_ref_text", doc, report
        )
        if not ddt_ref_text:
            return ""
        lang = self.env["res.lang"].search(
            [("code", "=", line.move_id.partner_id.lang)]
        )
        if not lang:
            lang = self.env.company.partner_id.lang
        date_format = lang.date_format
        date_ddt = ""
        date_done = ""
        ddt_number = ""
        # l10n_it_ddt's stock.picking.package.preparation(.line) models
        # were renamed/restructured into l10n_it_delivery_note's
        # stock.delivery.note(.line); account.move.line now links
        # straight to the header (`delivery_note_id`), no line-level hop
        # needed anymore.
        if line.delivery_note_id:
            date_ddt = self._fmt_date_macro(line.delivery_note_id.date, date_format)
            date_done = date_ddt
            ddt_number = line.delivery_note_id.name or ""
        ctx = {
            "ddt_number": ddt_number,
            "date_ddt": date_ddt,
            "date_done": date_done,
        }
        return ddt_ref_text % ctx
