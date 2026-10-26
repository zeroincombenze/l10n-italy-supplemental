# Copyright 2026 Zeroincombenze srls <https://www.zeroincombenze.it>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
import base64
import datetime
from io import BytesIO

from openpyxl import Workbook

from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


def make_xlsx(rows):
    wb = Workbook()
    sheet = wb.active
    for row in rows:
        sheet.append(row)
    buf = BytesIO()
    wb.save(buf)
    return base64.b64encode(buf.getvalue())


@tagged("post_install", "-at_install")
class TestImportXlsx(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tax_22 = cls.env["account.tax"].create(
            {
                "name": "IVA 22% test",
                "amount": 22.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "company_id": cls.company_data["company"].id,
                "sequence": 1,
            }
        )
        cls.product_a.default_code = "AAA"
        cls.product_b.default_code = "BBB"
        cls.partner_a.write({"name": "Prima Alpha SpA", "vat": "IT00115719999"})
        cls.partner_b.write({"name": "Latte Beta Due Snc", "vat": "IT02345670018"})
        cls.journal = cls.company_data["default_journal_sale"]

    def _wizard(self, rows, **vals):
        vals.setdefault("journal_id", self.journal.id)
        return self.env["wizard.import.invoice.file.xlsx"].create(
            dict(vals, data_file=make_xlsx(rows), filename="test.xlsx")
        )

    def test_01_lines_into_draft_invoice(self):
        invoice = self.init_invoice("out_invoice", partner=self.partner_a)
        wizard = self._wizard(
            [
                ["Nome", "Codice", "Quantita"],
                ["Prodotto Alpha", "AAA", 10],
                ["Prodotto Beta", "BBB", "2,5"],
            ]
        ).with_context(active_model="account.move", active_ids=invoice.ids)
        wizard.import_file_xlsx()
        lines = invoice.invoice_line_ids
        self.assertEqual(lines.product_id, self.product_a + self.product_b)
        line_a = lines.filtered(lambda r: r.product_id == self.product_a)
        line_b = lines.filtered(lambda r: r.product_id == self.product_b)
        self.assertEqual(line_a.quantity, 10)
        self.assertEqual(line_b.quantity, 2.5)
        self.assertEqual(line_a.name, "Prodotto Alpha")
        # Price and taxes come from the product
        self.assertEqual(line_a.price_unit, self.product_a.lst_price)
        reference = self.init_invoice(
            "out_invoice", partner=self.partner_a, products=self.product_a
        )
        self.assertEqual(line_a.tax_ids, reference.invoice_line_ids.tax_ids)
        self.assertTrue(invoice.amount_total > 0)

    def test_02_create_invoices(self):
        wizard = self._wizard(
            [
                [
                    "Denominazione Cliente",
                    "Partita Iva",
                    "Nome",
                    "Codice",
                    "Imponibile",
                    "Iva",
                    "Numero",
                    "Data",
                ],
                [
                    "Prima Alpha SpA",
                    "00115719999",
                    "Prodotto Alpha",
                    "AAA",
                    "2.049,18",
                    "450,82",
                    "INV/TEST/0001",
                    "05/03/2026",
                ],
                [
                    "Latte Beta Due Snc",
                    "IT02345670018",
                    "Prodotto Beta",
                    "BBB",
                    "200,00",
                    "44,00",
                    "INV/TEST/0002",
                    datetime.datetime(2026, 3, 6),
                ],
            ],
            invoice_date=datetime.date(2026, 3, 1),
        )
        action = wizard.import_file_xlsx()
        self.assertEqual(action["res_model"], wizard._name)
        moves = self.env["account.move"].search(
            [
                ("partner_id", "in", (self.partner_a + self.partner_b).ids),
                ("journal_id", "=", self.journal.id),
            ]
        )
        self.assertEqual(len(moves), 2)
        inv_a = moves.filtered(lambda m: m.partner_id == self.partner_a)
        inv_b = moves.filtered(lambda m: m.partner_id == self.partner_b)
        self.assertEqual(inv_a.move_type, "out_invoice")
        self.assertEqual(inv_a.state, "draft")
        self.assertEqual(inv_a.invoice_date, datetime.date(2026, 3, 5))
        self.assertEqual(inv_b.invoice_date, datetime.date(2026, 3, 6))
        self.assertEqual(inv_a.invoice_line_ids.price_unit, 2049.18)
        self.assertEqual(inv_a.invoice_line_ids.quantity, 1)
        self.assertEqual(inv_a.invoice_line_ids.tax_ids, self.tax_22)
        self.assertAlmostEqual(inv_a.amount_total, 2500.0, places=2)
        self.assertAlmostEqual(inv_b.amount_total, 244.0, places=2)

    def test_03_dry_run(self):
        wizard = self._wizard(
            [
                ["Denominazione Cliente", "Partita Iva", "Nome", "Imponibile"],
                ["Prima Alpha SpA", "00115719999", "Service", "100,00"],
            ],
            dry_run=True,
        )
        before = self.env["account.move"].search_count([])
        wizard.import_file_xlsx()
        self.assertEqual(self.env["account.move"].search_count([]), before)
        self.assertIn("Invoice will be created.", wizard.tracelog)

    def test_04_unknown_partner_and_bad_number(self):
        wizard = self._wizard(
            [
                ["Denominazione Cliente", "Nome", "Imponibile"],
                ["Nobody Srl", "Service", "100,00"],
            ]
        )
        before = self.env["account.move"].search_count([])
        wizard.import_file_xlsx()
        self.assertEqual(self.env["account.move"].search_count([]), before)
        self.assertIn("No partner found.", wizard.tracelog)
        wizard = self._wizard(
            [
                ["Denominazione Cliente", "Nome", "Imponibile"],
                ["Prima Alpha SpA", "Service", "12abc"],
            ]
        )
        with self.assertRaises(UserError):
            wizard.import_file_xlsx()

    def test_05_posted_invoice_refused(self):
        invoice = self.init_invoice(
            "out_invoice", partner=self.partner_a, products=self.product_a, post=True
        )
        wizard = self._wizard(
            [["Nome", "Codice", "Quantita"], ["Prodotto Alpha", "AAA", 1]]
        ).with_context(active_model="account.move", active_ids=invoice.ids)
        with self.assertRaises(UserError):
            wizard.import_file_xlsx()

    def test_06_tracelog_is_escaped(self):
        wizard = self._wizard(
            [
                ["Denominazione Cliente", "Nome", "Imponibile"],
                ["<script>alert(1)</script>", "Service", "1,00"],
            ],
            dry_run=True,
        )
        wizard.import_file_xlsx()
        self.assertNotIn("<script>", wizard.tracelog)
