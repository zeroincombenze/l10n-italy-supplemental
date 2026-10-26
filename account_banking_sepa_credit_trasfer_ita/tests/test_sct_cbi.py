# Copyright 2026 Zeroincombenze srls <https://www.zeroincombenze.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64
import time

from lxml import etree

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

CBI_NS = {"c": "urn:CBI:xsd:CBIPaymentRequest.00.04.00"}
COMPANY_IBAN = "IT60X0542811101000000123456"


@tagged("post_install", "-at_install")
class TestSctCbi(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.groups_id += cls.env.ref(
            "account_payment_order.group_account_payment"
        )
        cls.main_company = cls.env.company
        cls.env.ref("base.EUR").active = True
        cls.main_company.initiating_party_identifier = "ABCDE123"
        cls.method = cls.env.ref("account_banking_sepa_credit_trasfer_ita.sct_cbi")
        cls.account_expense = cls.company_data["default_account_expense"]
        cls.partner_agrolait = cls.env["res.partner"].create(
            {"name": "Agrolait", "company_id": cls.main_company.id}
        )
        cls.partner_c2c = cls.env["res.partner"].create(
            {"name": "C2C", "company_id": cls.main_company.id}
        )
        cls.bank_it = cls.env["res.bank"].create(
            {"name": "Banca Popolare", "bic": "POSOIT22XXX"}
        )
        cls.company_bank = cls.env["res.partner.bank"].create(
            {
                "acc_number": COMPANY_IBAN,
                "bank_id": cls.bank_it.id,
                "partner_id": cls.main_company.partner_id.id,
                "company_id": cls.main_company.id,
            }
        )
        cls.bank_agrolait = cls.env["res.partner.bank"].create(
            {
                "acc_number": "FR66 1212 1212 1212 1212 1212 121",
                "partner_id": cls.partner_agrolait.id,
                "allow_out_payment": True,
            }
        )
        cls.bank_c2c = cls.env["res.partner.bank"].create(
            {
                "acc_number": "BE96 9988 7766 5544",
                "partner_id": cls.partner_c2c.id,
                "allow_out_payment": True,
            }
        )
        cls.bank_journal = cls.company_data["default_journal_bank"]
        cls.bank_journal.write(
            {
                "bank_account_id": cls.company_bank.id,
                "outbound_payment_method_line_ids": [
                    Command.create(
                        {
                            "payment_method_id": cls.method.id,
                            "payment_account_id": cls.env["account.chart.template"]
                            .ref("account_journal_payment_credit_account_id")
                            .id,
                        }
                    )
                ],
            }
        )
        cls.payment_mode = cls.env["account.payment.mode"].create(
            {
                "name": "SCT CBI",
                "company_id": cls.main_company.id,
                "payment_method_id": cls.method.id,
                "bank_account_link": "fixed",
                "fixed_journal_id": cls.bank_journal.id,
            }
        )

    def _create_invoice(self, partner, partner_bank, price_unit, ref):
        invoice = self.env["account.move"].create(
            {
                "partner_id": partner.id,
                "reference_type": "none",
                "ref": ref,
                "currency_id": self.env.ref("base.EUR").id,
                "invoice_date": time.strftime("%Y-%m-%d"),
                "move_type": "in_invoice",
                "payment_mode_id": self.payment_mode.id,
                "partner_bank_id": partner_bank.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Great service",
                            "account_id": self.account_expense.id,
                            "price_unit": price_unit,
                            "quantity": 1,
                        }
                    )
                ],
            }
        )
        invoice.action_post()
        return invoice

    def _make_order(self):
        inv1 = self._create_invoice(self.partner_agrolait, self.bank_agrolait, 42, "F1")
        inv2 = self._create_invoice(self.partner_c2c, self.bank_c2c, 11, "F2")
        for invoice in inv1 + inv2:
            action = invoice.create_account_payment_line()
        order = self.env["account.payment.order"].browse(action["res_id"])
        order.draft2open()
        self.assertEqual(order.state, "open")
        return order

    def test_sct_cbi(self):
        order = self._make_order()
        action = order.open2generated()
        self.assertEqual(order.state, "generated")
        attachment = self.env["ir.attachment"].browse(action["res_id"])
        self.assertTrue(attachment.name.endswith(".xml"))
        root = etree.fromstring(base64.b64decode(attachment.datas))
        self.assertEqual(etree.QName(root).localname, "CBIPaymentRequest")
        self.assertEqual(root.findtext("c:GrpHdr/c:NbOfTxs", namespaces=CBI_NS), "2")
        self.assertEqual(
            root.findtext("c:GrpHdr/c:CtrlSum", namespaces=CBI_NS), "53.00"
        )
        self.assertEqual(
            root.findtext(".//c:InitgPty//c:Othr/c:Id", namespaces=CBI_NS), "ABCDE123"
        )
        self.assertEqual(
            root.findtext(".//c:DbtrAcct/c:Id/c:IBAN", namespaces=CBI_NS),
            COMPANY_IBAN,
        )
        ibans = {
            el.text
            for el in root.iterfind(
                ".//c:CdtTrfTxInf/c:CdtrAcct/c:Id/c:IBAN", namespaces=CBI_NS
            )
        }
        self.assertEqual(ibans, {"FR6612121212121212121212121", "BE96998877665544"})

    def test_invalid_cuc(self):
        self.main_company.initiating_party_identifier = "abc"
        order = self._make_order()
        with self.assertRaises(UserError):
            order.open2generated()

    def test_missing_cuc(self):
        self.main_company.initiating_party_identifier = False
        order = self._make_order()
        with self.assertRaises(UserError):
            order.open2generated()

    def test_not_italian_iban(self):
        foreign = self.env["res.partner.bank"].create(
            {
                "acc_number": "ES52 0182 2782 5688 3882 1868",
                "partner_id": self.main_company.partner_id.id,
                "company_id": self.main_company.id,
            }
        )
        self.bank_journal.bank_account_id = foreign
        order = self._make_order()
        with self.assertRaises(UserError):
            order.open2generated()
