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
    'external.2601': {
        'code': '2601',
        'name': 'IVA n/debito',
        'user_type_id': 'account.data_account_type_current_liabilities',
        'reconcile': False,
    },
    'external.3112': {
        'code': '3112',
        'name': 'Ricavi da merci e servizi',
        'user_type_id': 'account.data_account_type_revenue',
        'reconcile': False,
    },
    'external.3101': {
        'code': '3101',
        'name': 'Merci c/vendita',
        'user_type_id': 'account.data_account_type_revenue',
        'reconcile': False,
    },
    "z0bug.coa_152210": {}
}
TEST_ACCOUNT_FISCAL_POSITION = {
    "z0bug.fiscalpos_it": {
        "name": "Italia",
    },
}
TEST_ACCOUNT_FISCAL_YEAR = {
    "z0bug.fy_2022": {
        "name": "2022",
        "date_from": "2022-01-01",
        "date_to": "2022-12-31",
    },
}
TEST_ACCOUNT_JOURNAL = {
    "external.INV": {
        "name": "Fatture di vendita",
        "code": "INV",
        "type": "sale",
        "update_posted": True,
    },
    "z0bug.bank11_journal": {
        "name": "B. Pop. Software (IT15*456)",
        "bank_account_id": "z0bug.bank_company_1",
        "code": "BNK11",
        "type": "bank",
        "sequence": 10,
        "default_debit_account_id": "z0bug.coa_180003",
        "default_credit_account_id": "z0bug.coa_180003",
        "update_posted": True,
        # "default_bank_expenses_account": "z0bug.coa_731140",
    },
    "z0bug.bank13_journal": {
        "name": "Portafoglio RiBA e SDD – B. Pop. Soft. (IT15*456)",
        "bank_account_id": "z0bug.bank_company_1a",
        "code": "BNK13",
        "type": "bank",
        "sequence": 20,
        "default_debit_account_id": "z0bug.coa_152210",
        "default_credit_account_id": "z0bug.coa_152210",
        "is_wallet": True,
        "main_bank_account_id": "z0bug.bank11_journal",
        "update_posted": True,
        # "default_bank_expenses_account": "z0bug.coa_731140",
        "sezionale": "z0bug.bank11_journal",
        "limite_effetti_sbf": 5000,
    }
}
TEST_ACCOUNT_PAYMENT_METHOD = {
    "account_banking_riba.riba": {
    },
}
TEST_ACCOUNT_PAYMENT_MODE = {
    "z0bug.pmode_riba": {
        "name": "RiBA SBF",
        "bank_account_link": "variable",
        "type": "sale",
        "payment_method_id": "account_banking_riba.riba",
        "payment_type": "inbound",
    },
}
TEST_ACCOUNT_PAYMENT_TERM = {
    'z0bug.payment_1': {
        'name': 'RiBA 30GG/FM',
        'fatturapa_pt_id': 'l10n_it_fiscal_payment_term.fatturapa_tp02',
        'fatturapa_pm_id': 'l10n_it_fiscal_payment_term.fatturapa_mp12',
    },
    'z0bug.payment_2': {
        'name': 'RiBA 30/60 GG/FM',
        'fatturapa_pt_id': 'l10n_it_fiscal_payment_term.fatturapa_tp01',
        'fatturapa_pm_id': 'l10n_it_fiscal_payment_term.fatturapa_mp12',
    },
}
TEST_ACCOUNT_PAYMENT_TERM_LINE = {
    'z0bug.payment_1_1': {
        'payment_id': 'z0bug.payment_1',
        'sequence': 1,
        'days': 28,
        'value': 'balance',
        'option': 'after_invoice_month',
        'payment_method_credit': 'account_banking_riba.riba',
    },
    'z0bug.payment_2_1': {
        'payment_id': 'z0bug.payment_2',
        'sequence': 1,
        'days': 28,
        'value': 'percent',
        'value_amount': 50,
        'option': 'after_invoice_month',
        'payment_method_credit': 'account_banking_riba.riba',
    },
    'z0bug.payment_2_2': {
        'payment_id': 'z0bug.payment_2',
        'sequence': 2,
        'days': 58,
        'value': 'balance',
        'option': 'after_invoice_month',
        'payment_method_credit': 'account_banking_riba.riba',
    },
}

TEST_ACCOUNT_TAX = {
    'external.22v': {
        'description': '22v',
        'name': 'IVA 22% su vendite',
        'amount': 22,
        'amount_type': 'percent',
        'type_tax_use': 'sale',
        'price_include': False,
        'account_id': 'external.2601',
        'refund_account_id': 'external.2601',
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
        "electronic_invoice_subjected": True,
        "codice_destinatario": "A1B2C3X",
        "lang": "it_IT",
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
        "electronic_invoice_subjected": True,
        "codice_destinatario": "ABCDEFG",
        "goods_description_id": "l10n_it_ddt.goods_description_SFU",
        "carriage_condition_id": "l10n_it_ddt.carriage_condition_PAF",
        "transportation_method_id": "l10n_it_ddt.transportation_method_COR",
        "lang": "it_IT",
    },
}
TEST_RES_PARTNER_BANK = {
    "z0bug.bank_company_1": {
        "acc_number": "IT15A0123412345100000123456",
        "partner_id": "base.main_partner",
        "acc_type": "iban",
        "bank_id": "z0bug.bank_bps",
    },
    "z0bug.bank_company_1a": {
        "acc_number": "Portafoglio RiBA",
        "partner_id": "base.main_partner",
        "acc_type": "bank",
        "bank_is_wallet": True,
        "bank_main_bank_account_id": "z0bug.bank_company_1",
    },
    "z0bug.bank_partner_1": {
        "acc_number": "IT73C0102001011010101987654",
        "partner_id": "z0bug.res_partner_1",
        "acc_type": "iban",
    },
    "z0bug.bank_partner_2": {
        "acc_number": "IT82B0200802002200000000022",
        "partner_id": "z0bug.res_partner_2",
        "acc_type": "iban",
        "bank_id": "z0bug.bank_unicr",
    },
}
TEST_ACCOUNT_INVOICE_LINE = {
    "z0bug.invoice_Z0_1_01": {
        "invoice_id": "z0bug.invoice_Z0_1",
        "product_id": "z0bug.product_product_1",
        "name": "Prodotto Alpha",
        "quantity": 100,
        "account_id": "external.3112",
        "price_unit": 0.84,
        "invoice_line_tax_ids": "external.22v",
    },
    "z0bug.invoice_Z0_1_02": {
        "invoice_id": "z0bug.invoice_Z0_1",
        "product_id": "z0bug.product_product_2",
        "name": "Prodotto Beta",
        "quantity": 200,
        "account_id": "external.3112",
        "price_unit": 3.38,
        "invoice_line_tax_ids": "external.22v",
    },
    "z0bug.invoice_Z0_2_1": {
        "invoice_id": "z0bug.invoice_Z0_2",
        "product_id": "z0bug.product_product_1",
        "name": "Prodotto Alpha",
        "quantity": 100,
        "account_id": "external.3101",
        "price_unit": 0.42,
        "invoice_line_tax_ids": "external.22v",
    },
    "z0bug.invoice_Z0_2_2": {
        "invoice_id": "z0bug.invoice_Z0_2",
        "product_id": "z0bug.product_product_2",
        "name": "Prodotto Beta",
        "quantity": 100,
        "account_id": "external.3101",
        "price_unit": 1.69,
        "invoice_line_tax_ids": "external.22v",
    },
}

TEST_ACCOUNT_INVOICE = {
    "z0bug.invoice_Z0_1": {
        "partner_id": "z0bug.res_partner_1",
        "origin": "P1/2021/0001",
        "reference": "P1/2021/0001",
        "date_invoice": "2022-10-31",
        "type": "out_invoice",
        "journal_id": "external.INV",
        "fiscal_position_id": "z0bug.fiscalpos_it",
        "partner_bank_id": "z0bug.bank_company_1",
        "payment_term_id": "z0bug.payment_1",
        "company_bank_id": "z0bug.bank_company_1",
        "counterparty_bank_id": "z0bug.bank_partner_1",
    },
    "z0bug.invoice_Z0_2": {
        "partner_id": "z0bug.res_partner_2",
        "origin": "SO123",
        "reference": "SO123",
        "date_invoice": "2022-10-31",
        "type": "out_invoice",
        "journal_id": "external.INV",
        "fiscal_position_id": "z0bug.fiscalpos_it",
        "partner_bank_id": "z0bug.bank_company_1",
        "payment_term_id": "z0bug.payment_2",
        "company_bank_id": "z0bug.bank_company_1",
        "counterparty_bank_id": "z0bug.bank_partner_2",
    },
}
TEST_SETUP_LIST = [
    "account.account",
    "account.fiscal.position",
    "account.fiscal.year",
    "account.payment.method",
    "account.payment.mode",
    "account.payment.term",
    "account.payment.term.line",
    "res.partner",
    "res.partner.bank",
    "account.tax",
    "account.journal",
    "account.invoice",
    "account.invoice.line",
]


class AccountInvoice(SingleTransactionCase):

    def setUp(self):
        super().setUp()
        data = {"TEST_SETUP_LIST": TEST_SETUP_LIST}
        for resource in TEST_SETUP_LIST:
            item = "TEST_%s" % resource.upper().replace(".", "_")
            data[item] = globals()[item]
        self.declare_all_data(data, merge="zerobug")
        xref_bank = "external.%s" % self.env["account.account"].search(
            [("user_type_id",
              "=",
              self.env.ref("account.data_account_type_liquidity").id)])[0].code
        portafoglio = "external.%s" % self.env["account.account"].search(
            [("user_type_id",
              "=",
              self.env.ref("account.data_account_type_current_assets").id)])[-1].code
        effetti = "external.%s" % self.env["account.account"].search(
            [("user_type_id",
              "=",
              self.env.ref("account.data_account_type_current_assets").id)])[0].code
        for field in ("default_debit_account_id", "default_credit_account_id"):
            self.add_translation(
                "account.journal",
                field,
                ["z0bug.coa_180003", xref_bank])
        for acc in ("z0bug.coa_180006", "z0bug.coa_180007", "z0bug.coa_180008"):
            self.add_translation(
                "account.journal",
                "portafoglio_sbf",
                [acc, portafoglio])
        self.add_translation(
            "account.journal",
            "effetti_allo_sconto",
            ["z0bug.coa_152220", effetti])
        self.setup_env(lang="it_IT")  # Create test environment

        self.company = self.default_company()
        self.company.vat = "IT05111810015"
        self.company.sia_code = "A7721"
        pay_mode = self.resource_bind("z0bug.pmode_riba")
        pay_mode.fixed_journal_id = self.resource_bind("z0bug.bank13_journal")
        pay_mode.bank_account_link = "fixed"
        # TODO> Check best way
        journal = self.resource_bind("z0bug.bank13_journal")
        journal.portafoglio_sbf = self.env["account.account"].search(
            [("user_type_id",
              "=",
              self.env.ref("account.data_account_type_current_assets").id)])[-1]

    def tearDown(self):
        super().tearDown()
        if os.environ.get("ODOO_COMMIT_TEST", ""):
            self.env.cr.commit()  # pylint: disable=invalid-commit
            _logger.info("✨ Test data committed")

    def test_payment_order(self):
        for xref in TEST_ACCOUNT_INVOICE.keys():
            invoice = self.resource_bind(xref)
            invoice.compute_taxes()
            invoice.action_invoice_open()
        partners = (
            self.resource_bind("z0bug.res_partner_1").id,
            self.resource_bind("z0bug.res_partner_2").id,
        )
        lines_model = self.env["account.move.line"]
        move_lines = lines_model.search(
            [
                ("user_type_id",
                 "=",
                 self.env.ref("account.data_account_type_receivable").id),
                ("journal_id.type", "=", "sale"),
                ("partner_id", "in", partners)
            ]
        )
        active_ids = [x.id for x in move_lines]
        ctx = {
            "active_model": "account.move.line",
            "active_ids": active_ids,
        }
        act_windows = lines_model.with_context(ctx).open_wizard_payment_order_generate()
        self.assertTrue(
            self.is_action(act_windows)
        )

        model = "account.payment.order"
        # model_child = "account.payment.line"
        act_windows = self.wizard(
            act_windows=act_windows,
            default={"payment_mode_id": self.env.ref("z0bug.pmode_riba").id},
            web_changes=[
                ("journal_id", self.resource_bind("z0bug.bank13_journal").id)
            ],
            # ctx=ctx,
            button_name="generate",
        )

        self.assertTrue(
            self.is_action(act_windows)
        )
        self.assertEqual(
            act_windows["res_model"],
            model
        )
        self.assertTrue(
            act_windows["res_id"] > 0
        )
        pay_order = self.env[act_windows["res_model"]].browse(act_windows["res_id"])
        pay_move_lines = [x.move_line_id.id for x in pay_order.payment_line_ids]
        self.assertEqual(
            set(pay_move_lines),
            set(active_ids)
        )

        pay_order.draft2open()
        self.assertEqual(
            pay_order.state,
            "open",
            "Payment order not opened!"
        )

        pay_order.open2generated()
        self.assertEqual(
            pay_order.state,
            "generated",
            "Payment order not generated!"
        )

        pay_order.generated2uploaded()
        self.assertEqual(
            pay_order.state,
            "uploaded",
            "Payment order not uploaded!"
        )
