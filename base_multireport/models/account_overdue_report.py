# -*- coding: utf-8 -*-
import time
from datetime import datetime

from odoo import api, fields, models


class ReportOverdue(models.AbstractModel):
    _name = "report.base_multireport.report_overdue"

    def fmt_date(self, date):
        return datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%d-%m-%Y")

    def _get_account_move_lines(self, partner_ids):
        res = dict(map(lambda x: (x, []), partner_ids))
        self.env.cr.execute(
            "SELECT m.name AS move_id,l.date,l.name,l.ref,l.date_maturity,"
            "l.partner_id,l.blocked,l.amount_currency,l.currency_id,"
            "CASE WHEN at.type = 'receivable' and l.amount_residual > 0.0 "
            "THEN SUM(l.amount_residual) "
            "ELSE 0.0 "
            "END AS debit,"
            "CASE WHEN at.type = 'receivable'  and l.amount_residual < 0.0 "
            "THEN SUM(l.amount_residual * -1) "
            "ELSE 0.0 "
            "END AS credit,"
            "CASE WHEN l.date_maturity < %s "
            "THEN SUM(l.amount_residual) "
            "ELSE 0.0 "
            "END AS mat "
            "FROM account_move_line l "
            "JOIN account_account_type at ON (l.user_type_id = at.id) "
            "JOIN account_move m ON (l.move_id = m.id) "
            "WHERE l.partner_id IN %s AND "
            "at.type IN ('receivable', 'payable') AND "
            "l.full_reconcile_id IS NULL AND "
            "l.amount_residual <> 0.0 "
            "GROUP BY l.partner_id,l.date_maturity,l.date,l.name,l.ref,"
            "at.type,l.blocked,l.amount_currency,l.currency_id,l.amount_residual,"
            "m.name,move_id "
            "ORDER BY l.partner_id,l.date_maturity,l.date",
            ((fields.date.today(),) + (tuple(partner_ids),)),
        )
        for row in self.env.cr.dictfetchall():
            row["date"] = self.fmt_date(row["date"])
            row["date_maturity"] = self.fmt_date(row["date_maturity"])
            res[row.pop("partner_id")].append(row)
        return res

    @api.model
    def render_html(self, docids, data=None):
        totals = {}
        lines = self._get_account_move_lines(docids)
        lines_to_display = {}
        company_currency = self.env.user.company_id.currency_id
        for partner_id in docids:
            lines_to_display[partner_id] = {}
            totals[partner_id] = {}
            for line_tmp in lines[partner_id]:
                line = line_tmp.copy()
                currency = (
                    line["currency_id"]
                    and self.env["res.currency"].browse(line["currency_id"])
                    or company_currency
                )
                if currency not in lines_to_display[partner_id]:
                    lines_to_display[partner_id][currency] = []
                    totals[partner_id][currency] = {
                        fn: 0.0 for fn in ["due", "paid", "mat", "total"]
                    }
                for field, tot_field in (
                    ("debit", "due"),
                    ("credit", "paid"),
                    ("mat", "mat"),
                ):
                    if line[field] and line["currency_id"]:
                        line[field] = line["amount_currency"]
                    if not line["blocked"]:
                        totals[partner_id][currency][tot_field] += line[field]
                        totals[partner_id][currency]["total"] += (
                            line["debit"] - line["credit"]
                        )
                lines_to_display[partner_id][currency].append(line)

        docargs = {
            "doc_ids": docids,
            "doc_model": "res.partner",
            "docs": self.env["res.partner"].browse(docids),
            "time": time,
            "Lines": lines_to_display,
            "Totals": totals,
            "Date": datetime.strftime(fields.date.today(), "%d-%m-%Y"),
        }
        return self.env["report"].render(
            "base_multireport.report_overdue", values=docargs
        )
