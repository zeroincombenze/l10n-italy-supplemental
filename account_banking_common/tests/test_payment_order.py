# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import os
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)
TEST_ACCOUNT_ACCOUNT = {
    # The bank account is linked to demo dat: usually is 101401
    # "z0bug.coa_bnk1": {
    #     "code": "101401",
    #     "name": "Banca",
    #     "reconcile": True,
    #     "user_type_id": "account.data_account_type_liquidity",
    # },
    "z0bug.coa_tax_recv": {
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
    "z0bug.coa_bnk_fee": {
        "code": "212300",
        "reconcile": False,
        "user_type_id": "account.data_account_type_expenses",
        "name": "Costi bancari",
    },
}

TEST_ACCOUNT_FISCAL_POSITION = {
    "z0bug.fiscalpos_it": {
        "name": "Italia",
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
        # "bank_account_id": "z0bug.coa_bnk1",
        "sequence": 10,
        "default_debit_account_id": "z0bug.coa_bnk1",
        "default_credit_account_id": "z0bug.coa_bnk1",
        "default_bank_expenses_account": "z0bug.coa_bnk_fee",
    },
}

TEST_ACCOUNT_PAYMENT_METHOD = {
    "account_banking_riba.riba": {
        "name": "RiBa CBI",
        "code": "riba_cbi",
        "payment_type": "inbound",
    },
}

TEST_ACCOUNT_PAYMENT_MODE = {
    "z0bug.pmode_riba": {
        "name": "RiBA",
        "bank_account_link": "variable",
        "type": "sale",
        "payment_method_id": "account_banking_riba.riba",
        "payment_type": "inbound",
    },
}


TEST_ACCOUNT_PAYMENT_TERM = {
    'z0bug.payment_1': {
        'name': 'RiBA 30GG',
    },
    'z0bug.payment_2': {
        'name': 'RiBA 30/60 GG',
    },
}

TEST_ACCOUNT_PAYMENT_TERM_LINE = {
    'z0bug.payment_1_1': {
        'payment_id': 'z0bug.payment_1',
        'sequence': 1,
        'days': 30,
        'value': 'balance',
        'payment_method_credit': 'account_banking_riba.riba',
    },
    'z0bug.payment_2_1': {
        'payment_id': 'z0bug.payment_2',
        'sequence': 1,
        'days': 30,
        'value': 'percent',
        'value_amount': 50,
        'payment_method_credit': 'account_banking_riba.riba',
    },
    'z0bug.payment_2_2': {
        'payment_id': 'z0bug.payment_2',
        'sequence': 2,
        'days': 60,
        'value': 'balance',
        'payment_method_credit': 'account_banking_riba.riba',
    },
}

TEST_ACCOUNT_TAX = {
    "external.22v": {
        "description": "22v",
        "name": "IVA 22% su vendite",
        "amount_type": "percent",
        "account_id": "z0bug.coa_tax_recv",
        "refund_account_id": "z0bug.coa_tax_recv",
        "amount": 22,
        "type_tax_use": "sale",
        "price_include": False,
    },
}

TEST_PRODUCT_TEMPLATE = {
    "z0bug.product_template_1": {
        "property_account_income_id": "z0bug.coa_sale",
        "name": "Prodotto Alpha",
        "weight": 0.1,
        "type": "consu",
        "standard_price": 0.42,
        "uom_id": "uom.product_uom_unit",
        "lst_price": 0.84,
        "default_code": "AA",
        "uom_po_id": "uom.product_uom_unit",
        "taxes_id": "external.22v",
    },
    "z0bug.product_template_2": {
        "property_account_income_id": "z0bug.coa_sale",
        "name": "Prodotto Beta",
        "weight": 0.2,
        "type": "consu",
        "standard_price": 1.69,
        "uom_id": "uom.product_uom_unit",
        "lst_price": 3.38,
        "default_code": "BB",
        "uom_po_id": "uom.product_uom_unit",
        "taxes_id": "external.22v",
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
        "property_account_position_id": "z0bug.fiscalpos_it",
        "property_payment_term_id": "z0bug.payment_1",
        "property_supplier_payment_term_id": "z0bug.payment_1",
    },
    "z0bug.res_partner_2": {
        "name": "Latte Beta Due s.n.c.",
        "street": "Via Dueville, 2",
        "country_id": "base.it",
        "zip": "10060",
        "city": "S. Secondo Pinerolo",
        "state_id": "base.state_it_to",
        "customer": True,
        "supplier": False,
        "is_company": True,
        "email": "agrolait2@libero.it",
        "phone": "+39 0121555123",
        "vat": "IT02345670018",
        "website": "http://www.agrolait2.it/",
        "property_account_position_id": "z0bug.fiscalpos_it",
        "property_payment_term_id": "z0bug.payment_2",
    },
}

TEST_RES_PARTNER_BANK = {
    "z0bug.bank_company_1": {
        "partner_id": "base.main_partner",
        "sequence": 1,
        "acc_type": "iban",
        "codice_sia": "A7721",
        "acc_number": "IT15A0123412345100000123456",
    },
    "z0bug.bank_partner_1": {
        "partner_id": "z0bug.res_partner_1",
        "acc_type": "iban",
        "acc_number": "IT73C0102001011010101987654",
    },
    "z0bug.bank_partner_2": {
        "partner_id": "z0bug.res_partner_2",
        "acc_type": "iban",
        "acc_number": "IT82B0200802002200000000022",
    },
}

TEST_ACCOUNT_INVOICE_LINE = {
    "z0bug.invoice_Z0_1_01": {
        "invoice_id": "z0bug.invoice_Z0_1",
        "product_id": "z0bug.product_product_1",
        "name": "Prodotto Alpha",
        "quantity": 100,
        "account_id": "z0bug.coa_sale",
        "price_unit": 0.84,
        "invoice_line_tax_ids": "external.22v",
    },
    "z0bug.invoice_Z0_1_02": {
        "invoice_id": "z0bug.invoice_Z0_1",
        "product_id": "z0bug.product_product_2",
        "name": "Prodotto Beta",
        "quantity": 200,
        "account_id": "z0bug.coa_sale",
        "price_unit": 3.38,
        "invoice_line_tax_ids": "external.22v",
    },
    "z0bug.invoice_Z0_2_1": {
        "invoice_id": "z0bug.invoice_Z0_2",
        "product_id": "z0bug.product_product_1",
        "name": "Prodotto Alpha",
        "quantity": 100,
        "account_id": "z0bug.coa_sale",
        "price_unit": 0.42,
        "invoice_line_tax_ids": "external.22v",
    },
    "z0bug.invoice_Z0_2_2": {
        "invoice_id": "z0bug.invoice_Z0_2",
        "product_id": "z0bug.product_product_2",
        "name": "Prodotto Beta",
        "quantity": 100,
        "account_id": "z0bug.coa_sale",
        "price_unit": 1.69,
        "invoice_line_tax_ids": "external.22v",
    },
}

TEST_ACCOUNT_INVOICE = {
    "z0bug.invoice_Z0_1": {
        "partner_id": "z0bug.res_partner_1",
        "origin": "P1/2021/0001",
        "reference": "P1/2021/0001",
        "date_invoice": "####-<#-99",
        "type": "out_invoice",
        "journal_id": "external.INV",
        "fiscal_position_id": "z0bug.fiscalpos_it",
        # "partner_bank_id": "z0bug.bank_partner_1",
        "payment_term_id": "z0bug.payment_1",
        "company_bank_id": "z0bug.bank_company_1",
        "counterparty_bank_id": "z0bug.bank_partner_1",
    },
    "z0bug.invoice_Z0_2": {
        "partner_id": "z0bug.res_partner_2",
        "origin": "SO123",
        "reference": "SO123",
        "date_invoice": "####-<#-99",
        "type": "out_invoice",
        "journal_id": "external.INV",
        "fiscal_position_id": "z0bug.fiscalpos_it",
        # "partner_bank_id": "z0bug.bank_partner_1",
        "payment_term_id": "z0bug.payment_2",
        "company_bank_id": "z0bug.bank_company_1",
        "counterparty_bank_id": "z0bug.bank_partner_2",
    },
}

TEST_SETUP_LIST = [
    "account.account",
    "account.tax",
    "account.fiscal.position",
    "account.payment.method",
    "account.payment.mode",
    "account.payment.term",
    "account.payment.term.line",
    "product.template",
    "res.partner",
    "res.partner.bank",
    "account.journal",
    "account.invoice",
    "account.invoice.line",
]


class TestPaymentOrder(SingleTransactionCase):

    def setUp(self):
        super().setUp()
        data = {"TEST_SETUP_LIST": TEST_SETUP_LIST}
        for resource in TEST_SETUP_LIST:
            item = "TEST_%s" % resource.upper().replace(".", "_")
            data[item] = globals()[item]
        self.declare_all_data(data)
        self.setup_company(self.default_company(),
                           bnk1_xref="z0bug.coa_bnk1")
        self.setup_env()  # Create test environment

    def tearDown(self):
        super().tearDown()
        if os.environ.get("ODOO_COMMIT_TEST", ""):
            # Save test environment, so it is available to use
            self.env.cr.commit()  # pylint: disable=invalid-commit
            _logger.info("✨ Test data committed")

    def _validate_invoice(self):
        bnk_journal = self.resource_bind("external.BNK1")
        bnk_journal.inbound_payment_method_ids = (
            4, self.resource_bind("account_banking_riba.riba").id)
        pay_mode = self.resource_bind("z0bug.pmode_riba")
        self.resource_edit(
            resource=pay_mode,
            web_changes=[
                ("fixed_journal_id", "external.BNK1"),
                ("bank_account_link", "fixed"),
            ]
        )

        invoices = self.env["account.invoice"]
        for xref in TEST_ACCOUNT_INVOICE.keys():
            invoice = self.resource_bind(xref)
            invoice.compute_taxes()
            invoice.action_invoice_open()
            invoices |= invoice

        due_records = self.env["account.move.line"].search(
            [
                ("invoice_id", "in", [x.id for x in invoices]),
                ("account_id.user_type_id", "=", self.env.ref(
                    "account.data_account_type_receivable").id),
            ]
        )

        return invoices, due_records

    def test_payment_order(self):
        _logger.info(
            "🎺 Starting test_riba()"
        )
        invoice, due_records = self._validate_invoice()

