# -*- coding: utf-8 -*-
#
# Copyright 2026 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import re

from odoo import fields
from odoo.tests.common import TransactionCase


class TestReportOverdue(TransactionCase):
    def test_dates_dd_mm_yyyy(self):
        receivable = self.env.ref("account.data_account_type_receivable")
        account = self.env["account.account"].create(
            {
                "code": "Z0REC",
                "name": "Test receivable",
                "user_type_id": receivable.id,
                "reconcile": True,
            }
        )
        income = self.env["account.account"].create(
            {
                "code": "Z0INC",
                "name": "Test income",
                "user_type_id": self.env.ref(
                    "account.data_account_type_revenue"
                ).id,
            }
        )
        journal = self.env["account.journal"].create(
            {"name": "Test misc", "code": "Z0MIS", "type": "general"}
        )
        partner = self.env["res.partner"].create({"name": "Test customer"})
        move = self.env["account.move"].create(
            {
                "journal_id": journal.id,
                "date": "2026-03-15",
                "line_ids": [
                    (0, 0, {
                        "name": "Due",
                        "account_id": account.id,
                        "partner_id": partner.id,
                        "debit": 100.0,
                        "date_maturity": "2026-04-30",
                    }),
                    (0, 0, {
                        "name": "Income",
                        "account_id": income.id,
                        "partner_id": partner.id,
                        "credit": 100.0,
                    }),
                ],
            }
        )
        move.post()
        html = self.env["report"].get_html(
            partner.ids, "account.report_overdue"
        )
        self.assertIn("15-03-2026", html)
        self.assertIn("30-04-2026", html)
        today = fields.Date.from_string(fields.Date.today())
        self.assertIn(today.strftime("%d-%m-%Y"), html)
        self.assertFalse(re.search(r"\b2026-0[34]-\d\d\b", html))
