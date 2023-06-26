import os
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)

TEST_ACCOUNT_ACCOUNT = {
    "z0bug.coa_tax_ova": {
        "code": "101300",
        "reconcile": False,
        "user_type_id": "account.data_account_type_current_assets",
        "name": "Tax Paid",
    },
    "z0bug.coa_tax_iva": {
        "code": "111200",
        "reconcile": False,
        "user_type_id": "account.data_account_type_current_liabilities",
        "name": "Tax Received",
    },
    "z0bug.coa_sale": {
        "code": "200000",
        "name": "Product Sales",
        "user_type_id": "account.data_account_type_revenue",
        "reconcile": False,
    },
    "z0bug.coa_cog": {
        "code": "210000",
        "reconcile": False,
        "user_type_id": "account.data_account_type_direct_costs",
        "name": "Cost of Goods Sold",
    },
}

TEST_ACCOUNT_FISCAL_YEAR = {
    "external.2023": {
        "name": "2023",
        "date_from": "####-01-01",
        "date_to": "####-12-31",
    }
}

TEST_ACCOUNT_JOURNAL = {
    "external.INV": {
        "code": "INV",
        "type": "sale",
        "update_posted": True,
        "name": "Fatture di vendita",
    },
    "external.BNK1": {
        "code": "BNK1",
        "type": "bank",
        "update_posted": True,
        "name": "Banca",
    },
}

TEST_ACCOUNT_TAX = {
    "external.22a": {
        "description": "22a",
        "name": "IVA 22% su acquisti",
        "amount_type": "percent",
        "account_id": "z0bug.coa_tax_ova",
        "refund_account_id": "z0bug.coa_tax_ova",
        "amount": 22,
        "type_tax_use": "purchase",
        "price_include": False,
    },
}

TEST_ACCOUNT_INVOICE = {
    "z0bug.invoice_Z0_1": {
        "partner_id": "z0bug.res_partner_1",
        "reference": "P1/2023/0001",
        "date_invoice": "####-<#-99",
        "type": "in_invoice",
        "journal_id": "external.BILL",
    },
}

TEST_ACCOUNT_INVOICE_LINE = {
    "z0bug.invoice_Z0_1_01": {
        "invoice_id": "z0bug.invoice_Z0_1",
        "name": "Prodotto Alpha",
        "quantity": 100,
        "account_id": "z0bug.coa_cog",
        "price_unit": 10.0,
        "invoice_line_tax_ids": "external.22a",
    },
}

TEST_ACCOUNT_MOVE = {
    "z0bug.move_1": {
        "partner_id": "z0bug.res_partner_2",
        "date": "####-##-99",
        "type": "entry",
        "ref": "invoice payment",
        "journal_id": "external.BNK1",
    },
}

TEST_ACCOUNT_MOVE_LINE = {
    "z0bug.move_1_1": {
        "move_id": "z0bug.move_1",
        "name": "invoice payment (SO123)",
        "account_id": "z0bug.coa_pay",
        "partner_id": "z0bug.res_partner_2",
        "debit": 1220.00,
        "ref": "invoice payment",
    },
    "z0bug.move_1_2": {
        "move_id": "z0bug.move_1",
        "name": "invoice payment (SO123)",
        "account_id": "z0bug.coa_bnk1",
        "partner_id": "z0bug.res_partner_2",
        "credit": 1220.00,
        "ref": "invoice payment",
    },
}

TEST_RES_PARTNER = {
    "z0bug.res_partner_1": {
        "name": "Prima Alpha S.p.A.",
        "street": "Via I Maggio, 101",
        "country_id": "base.it",
        "zip": "20022",
        "city": "Castano Primo",
        "state_id": "base.state_it_mi",
        "customer": True,
        "supplier": True,
        "is_company": True,
        "email": "info@prima-alpha.it",
        "phone": "+39 0255582285",
        "vat": "IT00115719999",
        "website": "http://www.prima-alpha.it",
    },
}

TEST_SETUP_LIST = [
    "account.account",
    "account.fiscal.year",
    "account.tax",
    "res.partner",
    "account.journal",
    "account.invoice",
    "account.invoice.line",
]


class MyTest(SingleTransactionCase):

    def setUp(self):
        super().setUp()
        # Add following statement just for get debug information
        self.debug_level = 3
        data = {"TEST_SETUP_LIST": TEST_SETUP_LIST}
        for resource in TEST_SETUP_LIST:
            item = "TEST_%s" % resource.upper().replace(".", "_")
            data[item] = globals()[item]
        self.declare_all_data(data)
        self.setup_company(self.default_company(),
                           recv_xref="z0bug.coa_recv",
                           pay_xref="z0bug.coa_pay",
                           bnk1_xref="z0bug.coa_bnk1",
                           values={
                               "name": "Test Company",
                               "street": "Via dei Matti, 0",
                               "country_id": "base.it",
                               "zip": "20080",
                               "city": "Ozzero",
                               "state_id": "base.state_it_mi",
                               "customer": False,
                               "supplier": False,
                               "is_company": True,
                               "email": "info@testcompany.org",
                               "phone": "+39 025551234",
                               "vat": "IT05111810015",
                               "website": "https://www.testcompany.org"})
        self.setup_env()

    def tearDown(self):
        super().tearDown()
        if os.environ.get("ODOO_COMMIT_TEST", ""):  # pragma: no cover
            # Save test environment, so it is available to dump
            self.env.cr.commit()                       # pylint: disable=invalid-commit
            _logger.info("✨ Test data committed")

    def get_templates_on_invoice(self):
        # TODO> amount_debit is 0?
        templates_assets = [
            {
                "code": self.resource_browse("z0bug.coa_tax_ova").code,
                "account_id": "z0bug.coa_tax_ova",
                # "amount_debit": 220.0,
                "amount_balance": 220.0,
            },
        ]
        template_liability = [
            # Non partner for balance without customer details + Always positive sign
            {
                "code": self.resource_browse("z0bug.coa_pay").code,
                "account_id": "z0bug.coa_pay",
                # "amount_credit": 1220.0,
                "amount_balance": 1220.0,
            },
        ]
        template_income = []
        template_expense = [
            {
                "code": self.resource_browse("z0bug.coa_cog").code,
                "account_id": "z0bug.coa_cog",
                # "amount_debit": 1000.0,
                "amount_balance": 1000.0,
            },
        ]
        return templates_assets, template_liability, template_income, template_expense

    def _do_test_balance_on_invoice(self):
        (templates_assets, template_liability,
         template_income, template_expense) = self.get_templates_on_invoice()
        self.validate_records(templates_assets,
                              self.env["italy.account.balance.line.asset"].search(
                                  [("balance_id", "=", self.report.id)]))
        self.validate_records(template_liability,
                              self.env["italy.account.balance.line.liability"].search(
                                  [("balance_id", "=", self.report.id)]))
        self.validate_records(template_income,
                              self.env["italy.account.balance.line.income"].search(
                                  [("balance_id", "=", self.report.id)]))
        self.validate_records(template_expense,
                              self.env["italy.account.balance.line.expense"].search(
                                  [("balance_id", "=", self.report.id)]))

    def get_templates_with_move(self):
        # TODO> amount_debit is 0?
        templates_assets = [
            {
                "code": self.resource_browse("z0bug.coa_tax_ova").code,
                "account_id": "z0bug.coa_tax_ova",
                # "amount_debit": 220.0,
                "amount_balance": 220.0,
            },
        ]
        template_liability = [
            # Non partner for balance without customer details + Always positive sign
            {
                "code": self.resource_browse("z0bug.coa_pay").code,
                "account_id": "z0bug.coa_pay",
                # "amount_credit": 1220.0,
                "amount_balance": 0.0,
            },
            {
                "code": self.resource_browse("z0bug.coa_bnk1").code,
                "account_id": "z0bug.coa_bnk1",
                # "amount_credit": 1220.0,
                "amount_balance": 1220.0,
            },
        ]
        template_income = []
        template_expense = [
            {
                "code": self.resource_browse("z0bug.coa_cog").code,
                "account_id": "z0bug.coa_cog",
                # "amount_debit": 1000.0,
                "amount_balance": 1000.0,
            },
        ]
        return templates_assets, template_liability, template_income, template_expense

    def _do_test_balance_with_move(self):
        (templates_assets, template_liability,
         template_income, template_expense) = self.get_templates_with_move()
        self.validate_records(templates_assets,
                              self.env["italy.account.balance.line.asset"].search(
                                  [("balance_id", "=", self.report.id)]))
        self.validate_records(template_liability,
                              self.env["italy.account.balance.line.liability"].search(
                                  [("balance_id", "=", self.report.id)]))
        self.validate_records(template_income,
                              self.env["italy.account.balance.line.income"].search(
                                  [("balance_id", "=", self.report.id)]))
        self.validate_records(template_expense,
                              self.env["italy.account.balance.line.expense"].search(
                                  [("balance_id", "=", self.report.id)]))

    def _test_generate_from_invoice(self):
        for xref in TEST_ACCOUNT_INVOICE.keys():
            invoice = self.resource_browse(xref)
            invoice.compute_taxes()
            invoice.action_invoice_open()
        self.report = self.resource_edit(
            resource="italy.account.balance",
            default={"balance_type": "ordinary"},
            web_changes=[
                ("name", "Test #1"),
                ("fiscalyear_id", "external.2023"),
            ]
        )
        act_windowss = self.wizard(
            module=".",
            action_name="action_generate_balance",
            records=self.report,
            button_name="generate_balance")
        self.assertTrue(self.is_action(act_windowss))

        self._do_test_balance_on_invoice()

    def _test_draft_moves(self):
        data = {"TEST_SETUP_LIST": ["account.move", "account.move.line"]}
        for resource in data["TEST_SETUP_LIST"]:
            item = "TEST_%s" % resource.upper().replace(".", "_")
            data[item] = globals()[item]
        self.declare_all_data(data, group="move_entry")
        self.setup_env(group="move_entry")

        # Draft move are ignored, so test is the same of above invoice test
        self._do_test_balance_on_invoice()

        # Now regenerate balance with draft moves
        self.resource_edit(
            resource=self.report,
            default={"balance_type": "ordinary"},
            web_changes=[
                ("name", "Test #1.1"),
                # ("fiscalyear_id", "external.2023"),
                ("target_move", "all"),
            ]
        )
        act_windowss = self.wizard(
            module=".",
            action_name="action_generate_balance",
            records=self.report,
            button_name="generate_balance")
        self.assertTrue(self.is_action(act_windowss))

        self._do_test_balance_with_move()

    def _test_generate_with_moves(self):
        self._test_draft_moves()

    def test_balance(self):
        _logger.info(
            "🎺 Testing test_balance"
        )
        self._test_generate_from_invoice()
        self._test_generate_with_moves()
