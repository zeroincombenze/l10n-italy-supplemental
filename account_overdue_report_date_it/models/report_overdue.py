# -*- coding: utf-8 -*-
#
# Copyright 2026 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from datetime import date

from odoo import api, fields, models


def fmt_date_it(value):
    """Return value as 'dd-mm-yyyy'; accept date, 'yyyy-mm-dd' or 'dd-mm-yyyy'."""
    if not value:
        return ""
    if isinstance(value, date):
        return value.strftime("%d-%m-%Y")
    if value[4:5] == "-":
        return fields.Date.from_string(value[:10]).strftime("%d-%m-%Y")
    return value


class ReportOverdue(models.AbstractModel):
    _inherit = "report.account.report_overdue"

    @api.model
    def _get_account_move_lines(self, partner_ids):
        # Core may or may not already format these dates (OCB patch)
        res = super(ReportOverdue, self)._get_account_move_lines(partner_ids)
        for rows in res.values():
            for row in rows:
                row["date"] = fmt_date_it(row["date"])
                row["date_maturity"] = fmt_date_it(row["date_maturity"])
        return res
