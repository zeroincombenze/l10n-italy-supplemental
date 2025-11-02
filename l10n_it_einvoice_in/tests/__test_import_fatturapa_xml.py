# -*- coding: utf-8 -*-
"""Test e-invoice import
Test various xml files with many properties.
See file ./tests/data/README.txt for furthermore information about specific
checkpoint of every xml file.
"""
from odoo.exceptions import UserError

from .fatturapa_common import FatturapaCommon


class TestDuplicatedAttachment(FatturapaCommon):

    def setUp(self):
        super(TestDuplicatedAttachment, self).setUp()
        # Set VAT number of e-invoices
        self.env.user.company_id.vat = "IT05111810015"
        self.tax_22a = self.create_tax_22a()
        self.tax_a10a = self.create_tax_a10a()
        self.tax_a27a = self.create_tax_a27a()
        self.tax_a17c2a = self.create_tax_a17c2a()
        self.invoice_model = self.env["account.invoice"]

    def test_00001_xml_import(self):
        # This test breaks the current transaction and every test executed after this
        # would fail.
        # So this test ir executed isolated from the other tests.
        self.run_wizard("🎺 test001", "IT12345670892_00001.xml")
        with self.assertRaises(UserError):
            self.run_wizard("🎺 test_duplicated", "IT12345670892_00001.xml")


class TestFatturaPAXMLValidation(FatturapaCommon):

    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()
        # Set VAT number of e-invoices
        self.env.user.company_id.vat = "IT05111810015"
        self.tax_22a = self.create_tax_22a()
        self.tax_a10a = self.create_tax_a10a()
        self.tax_a27a = self.create_tax_a27a()
        self.tax_a17c2a = self.create_tax_a17c2a()
        self.wt85 = self.create_wt_85()
        self.wt115 = self.create_wt_115()
        self.invoice_model = self.env["account.invoice"]

    def __test_02_xml_link(self):
        """
        E-invoice lines are created.
        Vendor Reference and Invoice Date are fetched from the XML.
        """
        supplier = self.env["res.partner"].search(
            [("vat", "=", "IT02780790107")], limit=1
        )
        invoice_values = {
            "partner_id": supplier.id,
            "type": "in_invoice",
        }
        orig_invoice = self.invoice_model.create(invoice_values)
        wiz_values = {
            "line_ids": [(0, 0, {"invoice_id": orig_invoice.id})],
        }
        self.run_wizard(
            "test_link_02",
            "IT02780790107_11004.xml",
            mode="link",
            wiz_values=wiz_values,
        )
        self.assertTrue(orig_invoice.e_invoice_line_ids)
        self.assertFalse(orig_invoice.invoice_line_ids)
        self.assertTrue(orig_invoice.e_invoice_validation_error)
        self.assertTrue(orig_invoice.reference)
        self.assertTrue(orig_invoice.date_invoice)

    def __test_03_xml_link(self):
        """
        E-invoice lines are created.
        Vendor Reference and Invoice Date are kept.
        """
        supplier = self.env["res.partner"].search(
            [("vat", "=", "IT02780790107")], limit=1
        )
        invoice_values = {
            "partner_id": supplier.id,
            "type": "in_invoice",
            "reference": "original_ref",
            "date_invoice": "2020-01-01",
        }
        orig_invoice = self.invoice_model.create(invoice_values)
        wiz_values = {
            "line_ids": [(0, 0, {"invoice_id": orig_invoice.id})],
        }
        self.run_wizard(
            "test_link_03",
            "IT01234567890_FPR04.xml",
            mode="link",
            wiz_values=wiz_values,
        )
        self.assertTrue(orig_invoice.e_invoice_line_ids)
        self.assertFalse(orig_invoice.invoice_line_ids)
        self.assertTrue(orig_invoice.e_invoice_validation_error)
        self.assertEqual(
            invoice_values["reference"],
            orig_invoice.reference,
        )
        self.assertEqual(
            invoice_values["date_invoice"],
            orig_invoice.date_invoice,
        )

    def __test_003_xml_import(self):
        res = self.run_wizard("🎺 test003", "IT05979361218_003.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, "FT/2015/0008")
        self.assertEqual(invoice.sender, "TZ")
        # self.assertEqual(invoice.intermediary.name, "ROSSI MARIO")
        # self.assertEqual(invoice.intermediary.firstname, "MARIO")
        # self.assertEqual(invoice.intermediary.lastname, "ROSSI")
        self.assertEqual(
            invoice.e_invoice_line_ids[0].discount_rise_price_ids[0].name, "SC"
        )
        self.assertEqual(
            invoice.e_invoice_line_ids[0].discount_rise_price_ids[0].percentage, 10
        )
        self.assertEqual(invoice.amount_untaxed, 9)
        self.assertEqual(invoice.amount_tax, 0)
        self.assertEqual(invoice.amount_total, 9)

    def __test_06_import_except(self):
        # File not exist Exception
        self.assertRaises(Exception, self.run_wizard, "test6_Exception", "")
        # fake Signed file is passed , generate orm_exception
        self.assertRaises(
            UserError,
            self.run_wizard,
            "test6_orm_exception",
            "IT05979361218_fake.xml.p7m",
        )

    def __test_004_xml_import(self):
        # 2 lines with quantity != 1 and discounts
        res = self.run_wizard("🎺 test004", "IT05979361218_004.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, "FT/2015/0009")
        self.assertAlmostEqual(invoice.amount_untaxed, 1173.60)
        self.assertEqual(invoice.amount_tax, 258.19)
        self.assertEqual(invoice.amount_total, 1431.79)
        # self.assertAlmostEqual(
        #     invoice.e_invoice_amount_untaxed,
        #     invoice.amount_untaxed,
        #     places=invoice.currency_id.decimal_places,
        # )
        # self.assertAlmostEqual(
        #     invoice.e_invoice_amount_tax,
        #     invoice.amount_tax,
        #     places=invoice.currency_id.decimal_places,
        # )
        self.assertEqual(invoice.e_invoice_validation_error, False)
        self.assertEqual(invoice.invoice_line_ids[0].admin_ref, "D122353")

    def __test_08_xml_import(self):
        # using ImportoTotaleDocumento
        res = self.run_wizard("test8", "IT05979361218_005.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, "FT/2015/0010")
        self.assertAlmostEqual(invoice.amount_total, 1288.61)
        self.assertFalse(invoice.inconsistencies)

    def __test_09_xml_import(self):
        # using DatiGeneraliDocumento.ScontoMaggiorazione without
        # ImportoTotaleDocumento
        # add test file name case sensitive
        res = self.run_wizard("test9", "IT05979361218_006.XML")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, "FT/2015/0011")
        self.assertAlmostEqual(invoice.amount_total, 1288.61)
        self.assertEqual(
            invoice.inconsistencies,
            "Computed amount untaxed 1030.42 is different from summary data 1173.6",
        )

    def __test_10_xml_import(self):
        # Fix Date format
        res = self.run_wizard("test6", "IT05979361218_007.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, "FT/2015/0009")
        self.assertEqual(invoice.date_invoice, "2015-03-16")
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].payment_due_date,
            "2015-06-03",
        )
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].fatturapa_pm_id.code,
            "MP18",
        )

    def __test_11_xml_import(self):
        # DatiOrdineAcquisto with RiferimentoNumeroLinea referring to
        # not existing invoice line
        res = self.run_wizard("test11", "IT02780790107_11006.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(len(invoice.invoice_line_ids[0].related_documents), 0)
        self.assertEqual(invoice.invoice_line_ids[0].sequence, 1)
        self.assertEqual(invoice.related_documents[0].type, "order")
        self.assertEqual(invoice.related_documents[0].lineRef, 60)

    def __test_12_xml_import(self):
        res = self.run_wizard("test12", "IT05979361218_008.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, "FT/2015/0012")
        self.assertEqual(invoice.sender, "TZ")
        self.assertEqual(invoice.intermediary.name, "ROSSI MARIO")
        self.assertEqual(invoice.intermediary.firstname, "MARIO")
        self.assertEqual(invoice.intermediary.lastname, "ROSSI")

    def __test_13_xml_import(self):
        # inconsistencies must not be duplicated
        res = self.run_wizard_multi(
            [
                "IT02780790107_11005.xml",
                "IT02780790107_11006.xml",
            ]
        )
        invoice1_id = res.get("domain")[0][2][0]
        invoice2_id = res.get("domain")[0][2][1]
        invoice1 = self.invoice_model.browse(invoice1_id)
        invoice2 = self.invoice_model.browse(invoice2_id)
        self.assertEqual(
            invoice1.inconsistencies,
            "Company Name field contains 'Societa' Alpha SRL'. "
            "Your System contains 'SOCIETA' ALPHA SRL'\n\n",
        )
        self.assertEqual(
            invoice2.inconsistencies,
            "Company Name field contains 'Societa' Alpha SRL'. "
            "Your System contains 'SOCIETA' ALPHA SRL'\n\n",
        )

    def __test_14_xml_import(self):
        # check: no tax code found , write inconsisteance and anyway
        # create draft
        res = self.run_wizard("test14", "IT02780790107_11007.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, "136")
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(invoice.amount_untaxed, 25.00)
        self.assertEqual(invoice.amount_tax, 0.0)
        self.assertEqual(
            invoice.inconsistencies,
            "Company Name field contains 'Societa' Alpha SRL'. "
            "Your System contains 'SOCIETA' ALPHA SRL'\n\n"
            "XML contains tax with percentage '15.55' "
            "but it does not exist in your system\n"
            "XML contains tax with percentage '15.55' "
            "but it does not exist in your system",
        )

    def __test_15_xml_import(self):
        self.wt = self.create_wt()
        res = self.run_wizard("test15", "IT05979361218_009.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEquals(invoice.withholding_tax_amount, 1)
        self.assertAlmostEquals(invoice.amount_total, 6.1)
        self.assertAlmostEquals(invoice.amount_net_pay, 5.1)

    def __test_16_xml_import(self):
        # file B2B downloaded from
        # http://www.fatturapa.gov.it/export/fatturazione/it/a-3.htm
        res = self.run_wizard("test16a", "IT01234567890_FPR03.xml")
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        for invoice in invoices:
            self.assertEqual(invoice.inconsistencies, "")
            self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
            self.assertTrue(invoice.reference in ("456", "123"))
            if invoice.reference == "123":
                self.assertTrue(len(invoice.invoice_line_ids) == 2)
                for line in invoice.invoice_line_ids:
                    self.assertFalse(line.product_id)
            if invoice.reference == "456":
                self.assertTrue(len(invoice.invoice_line_ids) == 1)
                for line in invoice.invoice_line_ids:
                    self.assertFalse(line.product_id)

        partner = invoice.partner_id
        partner.e_invoice_default_product_id = self.imac.product_variant_ids[0].id
        # I create a supplier code to be matched in XML
        self.env["product.supplierinfo"].create(
            {
                "name": partner.id,
                "product_tmpl_id": self.headphones.id,
                "product_code": "ART123",
            }
        )
        res = self.run_wizard("test16b", "IT01234567890_FPR03.xml")
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        for invoice in invoices:
            self.assertTrue(invoice.reference in ("456", "123"))
            if invoice.reference == "123":
                self.assertEqual(
                    invoice.invoice_line_ids[0].product_id.id,
                    self.headphones.product_variant_ids[0].id,
                )
            else:
                for line in invoice.invoice_line_ids:
                    self.assertEqual(
                        line.product_id.id, self.imac.product_variant_ids[0].id
                    )

        # change Livello di dettaglio Fatture elettroniche to Minimo
        partner.e_invoice_detail_level = "0"
        res = self.run_wizard("test16c", "IT01234567890_FPR03.xml")
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertTrue(len(invoices) == 2)
        for invoice in invoices:
            self.assertTrue(len(invoice.invoice_line_ids) == 0)

    def __test_17_xml_import(self):
        res = self.run_wizard("test17", "IT05979361218_010.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.related_documents[0].type, "invoice")

    def __test_19_xml_import(self):
        # Testing CAdES signature, base64 encoded
        res = self.run_wizard(
            "test19",
            "IT01234567890_FPR03.base64.xml.p7m",
            "IT01234567890_FPR03.xml.p7m",
        )
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        for invoice in invoices:
            self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
            self.assertEqual(invoice.partner_id.e_invoice_detail_level, "0")
            self.assertTrue(invoice.reference in ("456", "123"))
            if invoice.reference == "123":
                self.assertEqual(
                    invoice.inconsistencies,
                    "Computed amount untaxed 0.0 is different from summary data 25.0",
                )
            if invoice.reference == "456":
                self.assertEqual(
                    invoice.inconsistencies,
                    "Computed amount untaxed 0.0 is different from summary "
                    "data 2000.0",
                )

    def __test_20_xml_import(self):
        # Testing xml without xml declaration (sent by Amazon)
        res = self.run_wizard("test20", "IT05979361218_no_decl.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")

    def __test_21_xml_import(self):
        supplier = self.env["res.partner"].search([("vat", "=", "IT02780790107")])[0]
        # in order to make the system create the invoice lines
        supplier.e_invoice_detail_level = "2"
        res = self.run_wizard("test21", "IT01234567890_FPR04.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.inconsistencies, "")
        self.assertEqual(invoice.invoice_line_ids[2].price_unit, 0.0)
        self.assertEqual(invoice.invoice_line_ids[2].discount, 0.0)

    def __test_11x04_xml_import(self):
        res = self.run_wizard("🎺 test11x04", "IT02780790107_11x04.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)

        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")

        # self.assertIn("removed timezone information", invoice.inconsistencies)

        # DatiGeneraliDocumento/Causale
        self.assertIn("", invoice.comment)

        # DatiGeneraliDocumento/Data
        self.assertEqual(invoice.date_invoice, "2022-12-18")

        # DatiTrasporto/IndirizzoResa/NumeroCivico
        # self.assertEqual(
        #     invoice.delivery_address, "strada dei test,  \n12042 - Bra\nCN IT"
        # )

        # DatiTrasporto/DataOraConsegna
        self.assertEqual("2022-10-22 14:46:12", invoice.delivery_datetime)

        # DatiBeniServizi/DettaglioLinee/Descrizione
        self.assertEqual(invoice.invoice_line_ids[0].name, "N/D")

        # DatiPagamento/DettaglioPagamento/DataDecorrenzaPenale
        payment_data = self.env["fatturapa.payment.data"].search(
            [("invoice_id", "=", invoice.id)]
        )
        self.assertEqual(payment_data[0].payment_methods[0].penalty_date, "2023-05-01")

    def __test_23_xml_import(self):
        # Testing CAdES signature, base64 encoded with newlines
        res = self.run_wizard(
            "test23",
            "IT01234567890_FPR04.base64.xml.p7m",
            "IT01234567890_FPR04.xml.p7m",
        )
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)

    def __test_25_xml_import(self):
        res = self.run_wizard("test25", "IT05979361218_013.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEqual(invoice.e_invoice_amount_untaxed, 34.67)
        self.assertEqual(invoice.e_invoice_amount_tax, 0.0)
        self.assertEqual(invoice.e_invoice_amount_total, 34.32)
        self.assertAlmostEqual(invoice.efatt_rounding, - 0.35)
        invoice.action_invoice_open()
        move_line = False
        for line in invoice.move_id.line_ids:
            if (
                line.account_id.id
                == self.env.user.company_id.arrotondamenti_attivi_account_id.id
            ):
                move_line = True
        self.assertTrue(move_line)

    def __test_26_xml_import(self):
        res = self.run_wizard("test26", "IT05979361218_014.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 0)
        self.assertEqual(invoice.invoice_line_ids[1].quantity, 1)

    def __test_31_xml_import(self):
        res = self.run_wizard("test31", "IT01234567890_FPR05.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.invoice_line_ids[1].discount, 100)
        self.assertEqual(invoice.invoice_line_ids[1].price_subtotal, 0)
        self.assertEqual(invoice.amount_total, 12.2)

    def __test_32_xml_import(self):
        res = self.run_wizard("test02", "IT05979361218_012.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.partner_id.vat, "IT05979361218")

    def __test_39_xml_import_withholding(self):
        self.wt = self.create_wt_4q()
        self.wtq = self.create_wt_23_20q()
        res = self.run_wizard("test39", "IT01234567890_FPR11.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(len(invoice.ftpa_withholding_ids), 2)
        self.assertAlmostEquals(invoice.amount_total, 1220.0)
        self.assertAlmostEquals(invoice.withholding_tax_amount, 86.0)
        self.assertAlmostEquals(invoice.amount_net_pay, 1134.0)

    def __test_46_xml_import(self):
        wiz_values = {"e_invoice_detail_level": "0"}
        res = self.run_wizard("test46", "IT05979361218_016.xml", wiz_values=wiz_values)
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEqual(invoice.e_invoice_amount_untaxed, 34.32)
        self.assertEqual(invoice.e_invoice_amount_tax, 0.0)
        self.assertEqual(invoice.e_invoice_amount_total, 34.32)
