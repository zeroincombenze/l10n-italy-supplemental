# import os
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)

TEST_PRODUCT_TEMPLATE = {
    "z0bug.product_template_1": {
        "property_account_income_id": "l10n_generic_coa.conf_a_sale",
        "name": "Prodotto Alpha",
        "weight": 0.1,
        "type": "consu",
        "standard_price": 0.42,
        "uom_id": "product.product_uom_unit",
        "lst_price": 0.84,
        "default_code": "AA",
        "uom_po_id": "product.product_uom_unit",
        "taxes_id": "z0bug.tax_22v",
        "conai_category_id": "l10n_it_conai.ca",
    },
    "z0bug.product_template_2": {
        "property_account_income_id": "l10n_generic_coa.conf_a_sale",
        "name": "Prodotto Beta",
        "weight": 0.2,
        "type": "consu",
        "standard_price": 1.69,
        "uom_id": "product.product_uom_unit",
        "lst_price": 3.38,
        "default_code": "BB",
        "uom_po_id": "product.product_uom_unit",
        "taxes_id": "z0bug.tax_22v",
        "conai_category_id": "l10n_it_conai.al",
    },
}

TEST_ACCOUNT_INVOICE = {
    "z0bug.invoice_Z0_1": {
        "origin": "Test1",
        "reference": "SO123",
        "type": "out_invoice",
        "journal_id": "external.INV",
        "date_invoice": "####-<#-99",
        "partner_id": "z0bug.res_partner_2",
    },
}

TEST_ACCOUNT_INVOICE_LINE = {
    "z0bug.invoice_Z0_1_1": {
        "sequence": 1,
        "product_id": "z0bug.product_product_1",
        "invoice_id": "z0bug.invoice_Z0_1",
        "price_unit": 0.42,
        "quantity": 100,
        "product_uom": "product.product_uom_unit",
        "account_id": "l10n_generic_coa.conf_a_sale",
        "name": "Prodotto Alpha",
        "invoice_line_tax_ids": "z0bug.tax_22v",
    },
    "z0bug.invoice_Z0_1_2": {
        "sequence": 2,
        "product_id": "z0bug.product_product_2",
        "invoice_id": "z0bug.invoice_Z0_1",
        "price_unit": 1.69,
        "quantity": 20,
        "product_uom": "product.product_uom_unit",
        "account_id": "l10n_generic_coa.conf_a_sale",
        "name": "Prodotto Beta",
        "invoice_line_tax_ids": "z0bug.tax_22v",
    },
}

TEST_RES_PARTNER = {
    "z0bug.res_partner_2": {
        "street": "Via Dueville, 2",
        "city": "S. Secondo Pinerolo",
        "zip": "10060",
        "country_id": "base.it",
        "supplier": False,
        "email": "agrolait2@libero.it",
        "vat": "IT02345670018",
        "website": "http://www.agrolait2.it/",
        "phone": "+39 0121555123",
        "customer": True,
        "name": "Latte Beta Due s.n.c.",
        "is_company": True,
        "state_id": "base.state_it_to",
    },
}

TEST_SALE_ORDER = {
    "z0bug.sale_order_Z0_1": {
        "origin": "Test1",
        "client_order_ref": "230123",
        "date_order": "####-##-01",
        "partner_id": "z0bug.res_partner_2",
    },
}

TEST_SALE_ORDER_LINE = {
    "z0bug.sale_order_Z0_1_1": {
        "sequence": 1,
        "product_id": "z0bug.product_product_1",
        "order_id": "z0bug.sale_order_Z0_1",
        "price_unit": 0.42,
        "product_uom_qty": 100,
        "product_uom": "product.product_uom_unit",
        "tax_id": "z0bug.tax_22v",
        "name": "Prodotto Alpha",
    },
    "z0bug.sale_order_Z0_1_2": {
        "sequence": 2,
        "product_id": "z0bug.product_product_2",
        "order_id": "z0bug.sale_order_Z0_1",
        "price_unit": 1.69,
        "product_uom_qty": 20,
        "product_uom": "product.product_uom_unit",
        "tax_id": "z0bug.tax_22v",
        "name": "Prodotto Beta",
    },
}

TEST_SETUP_LIST = [
    "account.account",
    "account.tax",
    "product.template",
    "res.partner",
    "sale.order",
    "sale.order.line",
    "account.invoice",
    "account.invoice.line",
]


class TestConai(SingleTransactionCase):
    def setUp(self):
        super().setUp()
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
        self.setup_env()  # Create test environment

    def tearDown(self):
        super().tearDown()

    def _test_conai_order(self):
        _logger.info("🎺 Testing test_conai (order)")
        order = self.resource_browse("z0bug.sale_order_Z0_1")
        order.action_confirm()
        templates = []
        vals = {
            "product_id": self.default_company().conai_product_id.id,
            "conai_category_id": self.ref("l10n_it_conai.ca"),
            "product_qty": 10.0,
            "price_unit": 0.02,
            "price_subtotal": 0.2,
        }
        templates.append(vals)
        vals = {
            "product_id": self.default_company().conai_product_id.id,
            "conai_category_id": self.ref("l10n_it_conai.al"),
            "product_qty": 4.0,
            "price_unit": 0.02,
            "price_subtotal": 0.08,
        }
        templates.append(vals)
        records = self.env["sale.order.line"]
        for line in order.order_line:
            if line.product_id == self.default_company().conai_product_id:
                records += line
        self.validate_records(templates, records)

    def _test_conai_invoice(self):
        _logger.info("🎺 Testing test_conai (invoice)")
        invoice = self.resource_browse("z0bug.invoice_Z0_1")
        invoice.action_invoice_open()
        templates = []
        vals = {
            "product_id": self.default_company().conai_product_id.id,
            "conai_category_id": self.ref("l10n_it_conai.ca"),
            "quantity": 10.0,
            "price_unit": 0.02,
            "price_subtotal": 0.2,
        }
        templates.append(vals)
        vals = {
            "product_id": self.default_company().conai_product_id.id,
            "conai_category_id": self.ref("l10n_it_conai.al"),
            "quantity": 4.0,
            "price_unit": 0.02,
            "price_subtotal": 0.08,
        }
        templates.append(vals)
        records = self.env["account.invoice.line"]
        for line in invoice.invoice_line_ids:
            if line.product_id == self.default_company().conai_product_id:
                records += line
        self.validate_records(templates, records)

    def _test_create_ddt(self):
        _logger.info("🎺 Testing Create DdT")
        order = self.resource_browse("z0bug.sale_order_Z0_1")
        self.assertNotEqual(order.invoice_status, "invoiced")
        self.resource_edit(order, actions="action_create_ddt")
        ddt = self.resource_browse("z0bug.sale_order_Z0_1").ddt_ids[0]
        self.resource_edit(
            ddt,
            web_changes=[
                ("carriage_condition_id", "l10n_it_ddt.carriage_condition_PA"),
                ("goods_description_id", "l10n_it_ddt.goods_description_CAR"),
                ("transportation_reason_id", "l10n_it_ddt.transportation_reason_VEN"),
                ("transportation_method_id", "l10n_it_ddt.transportation_method_DES"),
            ],
            actions=["save", "set_done"],
        )
        self.assertEqual(ddt.state, "done")
        self.wizard(
            module="l10n_it_ddt",
            action_name="action_ddt_create_invoice",
            records=ddt,
            # web_changes=[],
            button_name="create_invoice",
        )
        self.assertEqual(
            self.resource_browse("z0bug.sale_order_Z0_1").invoice_status, "invoiced"
        )

    def test_conai(self):
        self._test_conai_order()
        self._test_conai_invoice()
        self._test_create_ddt()
