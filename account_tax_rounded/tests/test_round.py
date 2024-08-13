# -*- coding: utf-8 -*-
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)


# Record data for base models


TEST_SETUP_LIST = [
    "account.account",
    "account.tax",
    "account.journal",
    "account.fiscal.position",
    "account.payment.term",
    "account.payment.term.line",
    "product.template",
    "res.partner",
    "account.invoice",
    "account.invoice.line",
]


class TestInvoiceRound(SingleTransactionCase):
    def setUp(self):
        super(TestInvoiceRound, self).setUp()
        # Add following statement just for get debug information
        self.debug_level = 0
        self.odoo_commit_test = True
        self.setup_company(
            self.default_company(),
            xref="z0bug.mycompany",
            partner_xref="z0bug.partner_mycompany",
            recv_xref="z0bug.coa_recv",
            values={
                "name": "Test Company",
                "vat": "IT05111810015",
                "country_id": "base.it",
            },
        )
        # self.setup_env(precision={"Product Price": 4})
        self.setup_env()

    def tearDown(self):
        super(TestInvoiceRound, self).tearDown()

    def _test_1_purchase(self):
        xref = "z0bug.invoice_ZI_6"
        self.resource_browse(xref=xref).action_invoice_open()
        invoice = self.resource_browse(xref=xref)
        self.assertEqual(
            invoice.state,
            "open",
            msg="action_invoice_open() FAILED: no state changed!"
        )
        # Without this module, amount tax is 15.73
        # self.assertEqual(invoice.amount_tax, 15.74)
        # self.assertEqual(invoice.amount_untaxed, 71.53)
        # self.assertEqual(invoice.amount_total, 87.27)

    def _test_1_sale(self):
        xref = "z0bug.invoice_Z0_9"
        self.resource_browse(xref=xref).action_invoice_open()
        invoice = self.resource_browse(xref=xref)
        self.assertEqual(
            invoice.state,
            "open",
            msg="action_invoice_open() FAILED: no state changed!"
        )
        # self.assertEqual(invoice.amount_tax, 15.74)
        # self.assertEqual(invoice.amount_untaxed, 71.53)
        # self.assertEqual(invoice.amount_total, 87.27)

    def test_round(self):
        _logger.info("🎺 Testing Account Invoice Tax Round")
        self._test_1_purchase()
        self._test_1_sale()


