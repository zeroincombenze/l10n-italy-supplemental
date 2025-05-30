# -*- coding: utf-8 -*-
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)


# Record data for models to test
TEST_ACCOUNT_INVOICE = {
    "z0bug.invoice_Z0_1": {
        "type": "in_invoice",
        "account_id": "l10n_generic_coa.1_conf_a_recv",
        "date_invoice": "####-<#-99",
        "partner_id": "base.res_partner_1",
    },
}

TEST_ACCOUNT_INVOICE_LINE = {
    "z0bug.invoice_Z0_1_1": {
        "product_id": "base.product_product_1",
        "invoice_id": "z0bug.invoice_Z0_1",
        "price_unit": 0.84,
        "account_id": "l10n_generic_coa.1_conf_a_sale",
        "name": "Prodotto Alpha",
        "invoice_line_tax_ids": "l10n_generic_coa.1_sale_tax_template",
        "quantity": 100,
    },
    "z0bug.invoice_Z0_1_2": {
        "product_id": "base.product_product_2",
        "invoice_id": "z0bug.invoice_Z0_1",
        "price_unit": 1.69,
        "account_id": "l10n_generic_coa.conf_a_sale",
        "name": "Prodotto Beta",
        "invoice_line_tax_ids": "l10n_generic_coa.1_sale_tax_template",
        "quantity": 10,
    },
}

TEST_SETUP_LIST = [
    "account.invoice",
    "account.invoice.line",
]


class TestInvoice(SingleTransactionCase):

    def setUp(self):
        super(TestInvoice, self).setUp()
        self.debug_level = 0
        # self.odoo_commit_test = True
        self.setup_company(
            self.default_company(),
            xref="z0bug.mycompany",
            partner_xref="z0bug.partner_mycompany",
            recv_xref="z0bug.coa_recv",
            pay_xref="z0bug.coa_pay",
            values={
                "name": "Test Company",
                "vat": "IT05111810015",
                "country_id": "base.it",
            },
        )
        self.setup_env()                            # Create test environment
        self.env["account.journal"].search([("update_posted", "!=", True)]).write(
            {"update_posted": True}
        )

    def tearDown(self):
        super(TestInvoice, self).tearDown()

    def test_account_invoice(self):
        model = "account.invoice"
        for xref in TEST_ACCOUNT_INVOICE.keys():
            self.log_lvl_1(u"🎺 Testing %s[%s]" % (model, xref))
            invoice = self.resource_browse(xref=xref)
            self.resource_edit(resource=invoice, actions="action_invoice_open")
            self.assertEqual(
                invoice.state, "open", "action_invoice_open() FAILED: no state changed!"
            )
            invoice.action_invoice_cancel()
            invoice.action_invoice_draft()
