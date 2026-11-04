# -*- coding: utf-8 -*-
#
# Copyright 2026 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestInvoiceReferenceYear(TransactionCase):
    def setUp(self):
        super(TestInvoiceReferenceYear, self).setUp()
        company = self.env.user.company_id
        self.payable = self.env["account.account"].create(
            {
                "code": "Z0PAY",
                "name": "Test payable",
                "user_type_id": self.env.ref(
                    "account.data_account_type_payable"
                ).id,
                "reconcile": True,
                "company_id": company.id,
            }
        )
        self.expense = self.env["account.account"].create(
            {
                "code": "Z0EXP",
                "name": "Test expense",
                "user_type_id": self.env.ref(
                    "account.data_account_type_expenses"
                ).id,
                "company_id": company.id,
            }
        )
        self.journal = self.env["account.journal"].create(
            {
                "name": "Test purchases",
                "code": "Z0PUR",
                "type": "purchase",
                "company_id": company.id,
                "default_debit_account_id": self.expense.id,
                "default_credit_account_id": self.expense.id,
            }
        )
        self.partner = self.env["res.partner"].create(
            {"name": "Test supplier", "supplier": True}
        )

    def _bill(self, date, reference="FT/1"):
        return self.env["account.invoice"].create(
            {
                "type": "in_invoice",
                "partner_id": self.partner.id,
                "account_id": self.payable.id,
                "journal_id": self.journal.id,
                "date_invoice": date,
                "reference": reference,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Service",
                            "account_id": self.expense.id,
                            "quantity": 1,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )

    def test_same_reference_other_year_is_accepted(self):
        self._bill("2025-03-10").action_invoice_open()
        bill = self._bill("2026-03-10")
        bill.action_invoice_open()
        self.assertEqual(bill.state, "open")

    def test_same_reference_same_year_is_rejected(self):
        self._bill("2026-01-10").action_invoice_open()
        with self.assertRaises(UserError):
            self._bill("2026-12-20").action_invoice_open()
