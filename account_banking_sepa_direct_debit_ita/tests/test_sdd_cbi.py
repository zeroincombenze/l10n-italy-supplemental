# Copyright 2026 Zeroincombenze srls <https://www.zeroincombenze.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64

from lxml import etree

from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.account_banking_sepa_direct_debit.tests.test_sdd import TestSDDBase

CBI_NS = {"c": "urn:CBI:xsd:CBISDDReqLogMsg.00.01.00"}


@tagged("post_install", "-at_install")
class TestSddCbi(TestSDDBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.method_core = cls.env.ref(
            "account_banking_sepa_direct_debit_ita.sdd_core_cbi"
        )
        cls.method_b2b = cls.env.ref(
            "account_banking_sepa_direct_debit_ita.sdd_b2b_cbi"
        )
        cls.bank_journal.write(
            {
                "inbound_payment_method_line_ids": [
                    (
                        0,
                        0,
                        {
                            "payment_method_id": method.id,
                            "payment_account_id": cls.account_expense_company_B.id,
                        },
                    )
                    for method in (cls.method_core, cls.method_b2b)
                ]
            }
        )
        cls.company_bank_it = cls.env["res.partner.bank"].create(
            {
                "acc_number": "IT60X0542811101000000123456",
                "bank_id": cls.bank.id,
                "partner_id": cls.main_company.partner_id.id,
                "company_id": cls.main_company.id,
            }
        )
        cls.bank_journal.bank_account_id = cls.company_bank_it
        cls.main_company.write(
            {
                "sepa_creditor_identifier": "IT66ZZZA1B2C3D4E5F6G7H8",
                "initiating_party_identifier": "ABCDE123",
            }
        )
        cls.payment_mode.payment_method_id = cls.method_core
        # The CBI library requires the BIC country to match the IBAN country
        cls.mandate2.partner_bank_id.bank_id = cls.env["res.bank"].create(
            {"name": "BNP Paribas Fortis", "bic": "GEBABEBBXXX"}
        )

    def test_bic_country_mismatch(self):
        self.mandate2.partner_bank_id.bank_id = self.bank
        order = self._make_order()
        with self.assertRaises(UserError):
            order.open2generated()

    def _make_order(self):
        invoice1 = self.create_invoice(self.partner_agrolait.id, self.mandate2, 42.0)
        invoice2 = self.create_invoice(self.partner_c2c.id, self.mandate12, 11.0)
        for invoice in invoice1 + invoice2:
            action = invoice.create_account_payment_line()
        order = self.payment_order_model.browse(action["res_id"])
        order.draft2open()
        self.assertEqual(order.state, "open")
        return order

    def _generate(self, order):
        action = order.open2generated()
        self.assertEqual(order.state, "generated")
        attachment = self.attachment_model.browse(action["res_id"])
        self.assertTrue(attachment.name.endswith(".xml"))
        return etree.fromstring(base64.b64decode(attachment.datas))

    def test_core(self):
        root = self._generate(self._make_order())
        self.assertEqual(etree.QName(root).localname, "CBISDDReqLogMsg")
        self.assertEqual(root.findtext("c:GrpHdr/c:NbOfTxs", namespaces=CBI_NS), "2")
        self.assertEqual(
            root.findtext("c:GrpHdr/c:CtrlSum", namespaces=CBI_NS), "53.00"
        )
        self.assertEqual(
            root.findtext(".//c:InitgPty//c:Othr/c:Id", namespaces=CBI_NS), "ABCDE123"
        )
        self.assertEqual(
            root.findtext(".//c:LclInstrm/c:Cd", namespaces=CBI_NS), "CORE"
        )
        self.assertEqual(
            root.findtext(".//c:CdtrAcct/c:Id/c:IBAN", namespaces=CBI_NS),
            "IT60X0542811101000000123456",
        )
        mandates = {el.text for el in root.iterfind(".//c:MndtId", namespaces=CBI_NS)}
        self.assertEqual(mandates, {"BMTEST2", "BMTEST12"})

    def test_b2b(self):
        self.payment_mode.payment_method_id = self.method_b2b
        (self.mandate2 + self.mandate12).write({"scheme": "B2B"})
        root = self._generate(self._make_order())
        self.assertEqual(root.findtext(".//c:LclInstrm/c:Cd", namespaces=CBI_NS), "B2B")

    def test_wrong_scheme(self):
        # B2B method with CORE mandates must be refused
        self.payment_mode.payment_method_id = self.method_b2b
        order = self._make_order()
        with self.assertRaises(UserError):
            order.open2generated()

    def test_invalid_cuc(self):
        self.main_company.initiating_party_identifier = "abc"
        order = self._make_order()
        with self.assertRaises(UserError):
            order.open2generated()

    def test_missing_bic(self):
        order = self._make_order()
        self.bank.bic = False
        with self.assertRaises(UserError):
            order.open2generated()

    def test_standard_sepa_untouched(self):
        # Standard OCA SEPA method still produces the pain.008 file
        self.payment_mode.payment_method_id = self.env.ref(
            "account_banking_sepa_direct_debit.sepa_direct_debit"
        )
        self.payment_mode.payment_method_id.pain_version = "pain.008.001.02"
        root = self._generate(self._make_order())
        self.assertEqual(etree.QName(root).localname, "Document")
