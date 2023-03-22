# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License APL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from past.builtins import basestring, long
import os
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)

TEST_ACCOUNT_ACCOUNT = {
    # Output (paid) VAT account
    "z0bug.coa_tax_ova": {
        "code": "101300",
        "reconcile": False,
        "user_type_id": "account.data_account_type_current_assets",
        "name": "IVA n/credito",
    },
    # The bank account is linked to demo data: usually is 101401
    "z0bug.coa_bnk1": {
        # "code": "101401",
        "name": "Banca",
        "reconcile": False,
        "user_type_id": "account.data_account_type_liquidity",
    },
    # Input (received) VAT account
    "z0bug.coa_tax_iva": {
        "code": "111200",
        "reconcile": False,
        "user_type_id": "account.data_account_type_current_liabilities",
        "name": "IVA n/debito",
    },
    "z0bug.coa_sale": {
        "code": "200000",
        "name": "Merci c/vendita",
        "user_type_id": "account.data_account_type_revenue",
        "reconcile": False,
    },
    "z0bug.coa_sale2": {
        "code": "200010",
        "name": "Ricavi da servizi",
        "user_type_id": "account.data_account_type_revenue",
        "reconcile": False,
    },
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

TEST_ACCOUNT_INVOICE = {
    "z0bug.invoice_Z0_1": {
        "date_invoice": "####-<#-99",
        "journal_id": "external.INV",
        "origin": "P1/2023/0001",
        "partner_id": "z0bug.res_partner_1",
        "reference": "P1/2023/0001",
        "type": "out_invoice",
        "payment_term_id": "z0bug.payment_term_1",
    },
    "z0bug.invoice_Z0_2": {
        "date_invoice": "####-<#-99",
        "journal_id": "external.INV",
        "origin": "P1/2023/0002",
        "partner_id": "z0bug.res_partner_2",
        "reference": "P1/2023/0002",
        "type": "out_invoice",
        "payment_term_id": "z0bug.payment_term_1",
        "currency_id": "base.EUR",
    },
}

TEST_ACCOUNT_INVOICE_LINE = {
    "z0bug.invoice_Z0_1_1": {
        "invoice_id": "z0bug.invoice_Z0_1",
        "account_id": "z0bug.coa_sale",
        "invoice_line_tax_ids": "external.22v",
        "name": "Prodotto Alpha",
        "price_unit": 0.84,
        "product_id": "z0bug.product_product_1",
        "quantity": 100,
        "sequence": 1,
    },
    "z0bug.invoice_Z0_1_2": {
        "invoice_id": "z0bug.invoice_Z0_1",
        "account_id": "z0bug.coa_sale2",
        "invoice_line_tax_ids": "external.22v",
        "name": "Special Worldwide service",
        "price_unit": 1.88,
        "product_id": "z0bug.product_product_23",
        "quantity": 1,
        "sequence": 2,
    },
    "z0bug.invoice_Z0_2_1": {
        "invoice_id": "z0bug.invoice_Z0_2",
        "account_id": "z0bug.coa_sale",
        "invoice_line_tax_ids": "external.22v",
        "name": "Prodotto Beta",
        "price_unit": 3.38,
        "product_id": "z0bug.product_product_2",
        "quantity": 100,
        "sequence": 1,
    },
}

TEST_ACCOUNT_PAYMENT_TERM = {
    "z0bug.payment_term_1": {
        "name": "Bonifico 30 GG",
    },
}

TEST_ACCOUNT_PAYMENT_TERM_LINE = {
    "z0bug.payment_term_1_1": {
        "payment_id": "z0bug.payment_term_1",
        "sequence": 1,
        "days": 30,
        "value": "balance",
    },
}

TEST_ACCOUNT_TAX = {
    "external.22v": {
        "description": "22v",
        "name": "IVA 22% su vendite",
        "amount_type": "percent",
        "account_id": "z0bug.coa_tax_iva",
        "refund_account_id": "z0bug.coa_tax_iva",
        "amount": 22,
        "type_tax_use": "sale",
        "price_include": False,
    },
}

TEST_PRODUCT_TEMPLATE = {
    # Consumable product
    "z0bug.product_template_1": {
        "default_code": "AA",
        "name": "Prodotto Alpha",
        "lst_price": 0.84,
        "standard_price": 0.42,
        "type": "consu",
        "uom_id": "product.product_uom_unit",
        "uom_po_id": "product.product_uom_unit",
        "property_account_income_id": "z0bug.coa_sale",
    },
    "z0bug.product_template_2": {
        "default_code": "BB",
        "name": "Prodotto Beta",
        "lst_price": 3.38,
        "standard_price": 1.69,
        "type": "consu",
        "uom_id": "product.product_uom_unit",
        "uom_po_id": "product.product_uom_unit",
        "property_account_income_id": "z0bug.coa_sale",
    },
    # Product on stock
    "z0bug.product_template_18": {
        "default_code": "RR",
        "name": "Prodotto Rho",
        "lst_price": 1.19,
        "standard_price": 0.59,
        "type": "product",
        "uom_id": "product.product_uom_unit",
        "uom_po_id": "product.product_uom_unit",
        "property_account_income_id": "z0bug.coa_sale",
    },
    # Service
    "z0bug.product_template_23": {
        "default_code": "WW",
        "name": "Special Worldwide service",
        "lst_price": 1.88,
        "standard_price": 0,
        "type": "service",
        "uom_id": "product.product_uom_unit",
        "uom_po_id": "product.product_uom_unit",
        "property_account_income_id": "z0bug.coa_sale2",
    },
}

TEST_RES_PARTNER = {
    "z0bug.partner_mycompany": {
        "name": "Test Company",
        "street": "Via dei Matti, 0",
        "zip": "20080",
        "city": "Ozzero",
        "state_id": "base.state_it_mi",
        "customer": False,
        "supplier": False,
        "is_company": True,
        "email": "info@testcompany.org",
        "phone": "+39 025551234",
        "website": "https://www.testcompany.org",
    },
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
    },
    "z0bug.res_partner_2": {
        "name": "Latte Beta Due s.n.c.",
        "street": "Via Dueville, 2",
        "country_id": "base.it",
        "zip": "10060",
        "city": "S. Secondo Parmense",
        "state_id": "base.state_it_pr",
        "customer": True,
        "supplier": False,
        "is_company": True,
    },
}

TEST_SETUP_LIST = [
    "account.account",
    "account.tax",
    "account.journal",
    "product.template",
    "account.payment.term",
    "account.payment.term.line",
    "res.partner",
    "account.invoice",
    "account.invoice.line",
]


class TestPaymentOrder(SingleTransactionCase):

    def str2bool(self, t, default):
        """Convert text to bool"""
        if isinstance(t, bool):
            return t
        elif isinstance(t, (int, long)):
            return t != 0
        elif isinstance(t, float):
            return t != 0.0
        elif not isinstance(t, basestring):
            return default
        elif t.lower() in ["true", "t", "1", "y", "yes", "on", "enabled"]:
            return True
        elif t.lower() in ["false", "f", "0", "n", "no", "off", "disabled"]:
            return False
        else:
            return default

    def set_config_param(self, xref):
        param = self.env.ref(xref)
        user_ids = [x.id for x in self.env["res.users"].search([])]
        param.users = [6, 0, user_ids]

    def setUp(self):
        super().setUp()
        self.debug_level = 3
        self.date_rate_0 = self.compute_date("####-<#-99")
        data = {"TEST_SETUP_LIST": TEST_SETUP_LIST}
        for resource in TEST_SETUP_LIST:
            item = "TEST_%s" % resource.upper().replace(".", "_")
            data[item] = globals()[item]
        self.declare_all_data(data)
        self.setup_company(
            self.default_company(),
            xref="z0bug.mycompany",
            partner_xref="z0bug.partner_mycompany",
            recv_xref="z0bug.coa_recv",
            pay_xref="z0bug.coa_pay",
            bnk1_xref="z0bug.coa_bnk1",
            values={
                "name": "Test Company",
                "vat": "IT05111810015",
                "country_id": "base.it",
            },
        )
        self.set_config_param("base.group_multi_currency")
        model = "res.currency"
        self.resource_write(model, "base.EUR", {"active": True})
        self.setup_env()  # Create test environment
        xref = "base.EUR_%s" % self.date_rate_0
        self.declare_resource_data(
            "res.currency.rate",
            {
                xref: {
                    "currency_id": "base.EUR",
                    "name": self.date_rate_0,
                    "rate": 0.9,
                },

            }
        )

    def tearDown(self):
        super().tearDown()
        if os.environ.get("ODOO_COMMIT_TEST", ""):
            # Save test environment, so it is available to use
            self.env.cr.commit()  # pylint: disable=invalid-commit
            _logger.info("✨ Test data committed")

    def test_payment(self):
        _logger.info(
            "🎺 Starting test_payment()"
        )
        template = []
        record = self.env["account.move"]
        for xref in TEST_ACCOUNT_INVOICE.keys():
            invoice = self.resource_bind(xref)
            self.resource_edit(resource=invoice, actions="action_invoice_open")
            self.assertEqual(invoice.state, "open")
            vals = {
                "name": invoice.number,
                "journal_id": invoice.journal_id,
                "date": invoice.date,
                "currency_id": invoice.currency_id,
                "line_ids": []
            }
            line_vals = {
                "account_id": invoice.account_id,
                "debit": invoice.amount_total,
                "credit": 0.0,
            }
            vals["line_ids"].append(line_vals)
            record |= invoice.move_id
        self.validate_records(template, record)
        pass


