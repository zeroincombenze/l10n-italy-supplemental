# Copyright 2021-24 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
from .testenv import MainTest as SingleTransactionCase

TEST_SETUP_LIST = [
    "account.account",
    "account.tax",
    "date.range.type",
    "date.range",
    "account.invoice",
    "account.invoice.line",
]


class TestVatStatement(SingleTransactionCase):

    def setUp(self):
        super().setUp()
        self.debug_level = 0
        self.odoo_commit_test = True
        self.setup_env()                                      # Create test environment

        self.tax_model = self.env["account.tax"]
        self.account_model = self.env["account.account"]
        self.term_model = self.env["account.payment.term"]
        self.term_line_model = self.env["account.payment.term.line"]
        self.invoice_model = self.env["account.invoice"]
        self.invoice_line_model = self.env["account.invoice.line"]
        self.vat_statement_model = self.env["account.vat.period.end.statement"]

        # In order to validate results we cannot use current month to recorc invoices
        # because there are some invoices by account module.
        # So, conventionally we use last year novembre and decembre to record invoices
        # and test vat statement results
        self.prior_period = self.resource_browse("z0bug.daterange_year-1_11")
        self.current_period = self.resource_browse("z0bug.daterange_year-1_12")
        self.last_prior_date = self.compute_date("<001-11-30")
        self.last_recent_date = self.compute_date("<001-12-31")

        self.account_payment_term = self.term_model.create({
            "name": "16 Days End of Month",
            "note": "16 Days End of Month",
            })
        self.term_line_model.create({
            "value": "balance",
            "days": 16,
            "option": "after_invoice_month",
            "payment_id": self.account_payment_term.id,
            })

    def tearDown(self):
        super().tearDown()

    def test_vat_statement(self):
        for xref in ("z0bug.purchase_invoice_1",
                     "z0bug.purchase_invoice_2",
                     "z0bug.sale_invoice_1"):
            self.resource_browse(xref).action_invoice_open()
            self.assertEqual(
                self.resource_browse(xref).state,
                "open",
            )

        vat_statement = self.resource_edit(
            "account.vat.period.end.statement",
            web_changes=[
                ("date", "<001-11-30"),
                ("journal_id", "external.MISC"),
                ("authority_vat_account_id", "l10n_generic_coa.current_liabilities"),
                ("date_range_ids", "z0bug.daterange_year-1_11"),
            ]
        )
        self.assertIsNotNone(vat_statement)
        self.resource_edit(
            vat_statement,
            actions=["compute_amounts"]
        )
        self.assertEqual(vat_statement.authority_vat_amount, -88.0)
        self.assertEqual(vat_statement.residual, 0.0)

        vat_statement = self.resource_edit(
            "account.vat.period.end.statement",
            web_changes=[
                ("date", "<001-12-31"),
                ("journal_id", "external.MISC"),
                ("authority_vat_account_id", "l10n_generic_coa.current_liabilities"),
                ("date_range_ids", "z0bug.daterange_year-1_12"),
            ]
        )
        self.assertIsNotNone(vat_statement)
        self.resource_edit(
            vat_statement,
            actions=["compute_amounts"]
        )
        self.assertEqual(vat_statement.authority_vat_amount, 22.0)
        # self.assertEqual(vat_statement.residual, 22.0)
