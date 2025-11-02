# -*- coding: utf-8 -*-
"""Test e-invoice import
Test various xml files with many properties.
See file ./tests/data/README.txt for furthermore information about specific
checkpoint of every xml file.
"""
import logging
# from odoo.exceptions import UserError
from .fatturapa_common import FatturapaCommon

_logger = logging.getLogger(__name__)


class TestFatturaPAXMLValidation(FatturapaCommon):

    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()
        # Set VAT number of e-invoices
        self.env.user.company_id.vat = "IT05111810015"
        self.tax_22a = self.create_tax_22a()
        self.tax_10a = self.create_tax_10a()
        self.tax_a10a = self.create_tax_a10a()
        self.tax_a27a = self.create_tax_a27a()
        self.tax_a17c2a = self.create_tax_a17c2a()
        self.wt85 = self.create_wt_85()
        self.wt115 = self.create_wt_115()
        self.partner = self.create_partner_with_rea()
        self.invoice_model = self.env["account.invoice"]

    def invoice_from_xml(self, mesg, xml_fn):
        _logger.info(u"🎺 " + mesg + "(" + xml_fn + ")")
        return self.invoice_model.browse(
            self.run_wizard(mesg, xml_fn).get("domain")[0][2][0])

    def test_00_xml_import_001(self):
        # Mostly fields tests, Albo professionale, Cassa previdenziale. VAT with spaces
        invoice = self.invoice_from_xml("test_00_001", "IT05979361218_001.xml")
        self.assertEqual(invoice.partner_id.register_code, "TO1258B")
        self.assertEqual(invoice.partner_id.register_fiscalpos.code, "RF02")
        self.assertEqual(invoice.reference, "FT/2024/0006")
        self.assertEqual(invoice.amount_total, 57.0)
        self.assertEqual(invoice.gross_weight, 0.0)
        self.assertEqual(invoice.net_weight, 0.0)
        self.assertEqual(invoice.welfare_fund_ids[0].tax_kind_id.code, "N4")
        self.assertFalse(invoice.art73)
        welfare_found = False
        for line in invoice.invoice_line_ids:
            if line.product_id.id == self.service.id:
                self.assertEqual(line.price_unit, 3)
                welfare_found = True
        self.assertTrue(welfare_found)
        self.assertTrue(len(invoice.e_invoice_line_ids) == 1)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].name, "Prodotto di test al giorno"
        )
        self.assertEqual(invoice.e_invoice_line_ids[0].qty, 15)
        self.assertEqual(invoice.e_invoice_line_ids[0].uom, "Giorno(i)")
        self.assertEqual(invoice.e_invoice_line_ids[0].unit_price, 3.6)
        self.assertEqual(invoice.e_invoice_line_ids[0].total_price, 54.0)
        self.assertEqual(invoice.e_invoice_line_ids[0].tax_amount, 0.0)
        self.assertEqual(invoice.e_invoice_line_ids[0].tax_kind, "N4")
        self.assertTrue(len(invoice.e_invoice_line_ids[0].other_data_ids) == 2)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].other_data_ids[0].text_ref, "Riferimento"
        )
        self.assertEqual(invoice. e_invoice_amount_untaxed, 57.0)
        self.assertEqual(invoice. e_invoice_amount_tax, 0.0)
        self.assertEqual(invoice.e_invoice_amount_total, 57.0)
        invoice.invoice_validate()

    def test_01_xml_import_11004(self):
        # Supplier name like previous, rappresentante fiscale + fiscal code
        invoice = self.invoice_from_xml("test_01_11004", "IT02780790107_11004.xml")
        self.assertEqual(invoice.reference, "123")
        self.assertEqual(invoice.date_invoice, "2024-07-18")
        self.assertEqual(invoice.amount_untaxed, 34.00)
        self.assertEqual(invoice.amount_tax, 7.48)
        self.assertEqual(len(invoice.invoice_line_ids[0].invoice_line_tax_ids), 1)
        self.assertEqual(
            invoice.invoice_line_ids[0].invoice_line_tax_ids[0].name, "22% e-bill"
        )
        self.assertEqual(invoice.fatturapa_summary_ids[0].amount_untaxed, 34.00)
        self.assertEqual(invoice.fatturapa_summary_ids[0].amount_tax, 7.48)
        self.assertEqual(invoice.fatturapa_summary_ids[0].payability, "D")
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(invoice.partner_id.street, "VIALE ROMA 543")
        self.assertEqual(invoice.partner_id.state_id.code, "SS")
        self.assertEqual(invoice.partner_id.country_id.code, "IT")
        self.assertEqual(invoice.tax_representative_id.name, "Rappresentante fiscale")
        self.assertEqual(invoice.welfare_fund_ids[0].welfare_rate_tax, 0.04)
        order_related_doc = invoice.related_documents.filtered(
            lambda rd: rd.type == "order"
        )
        self.assertTrue(order_related_doc)
        self.assertEqual(order_related_doc.cig, "456def")
        self.assertEqual(order_related_doc.cup, "123abc")
        self.assertEqual(invoice.welfare_fund_ids[0].welfare_amount_tax, 9.0)
        self.assertFalse(invoice.welfare_fund_ids[0].welfare_taxable)
        self.assertEqual(invoice.unit_weight, "KGM")
        self.assertEqual(invoice.ftpa_incoterms, "DAP")
        self.assertEqual(invoice.fiscal_document_type_id.code, "TD01")
        self.assertTrue(invoice.art73)
        self.assertEqual(invoice. e_invoice_amount_untaxed, 34.0)
        self.assertEqual(invoice. e_invoice_amount_tax, 7.48)
        self.assertEqual(invoice.e_invoice_amount_total, 41.48)

    def test_02_xml_import_011(self):
        # Intermediary
        invoice = self.invoice_from_xml("test_02_011", "IT05979361218_011.xml")
        self.assertEqual(invoice.intermediary.vat, "IT02886610241")

    def test_80_xml_import(self):
        # E-invoice from RSM with wrong len vat number
        invoice = self.invoice_from_xml("test_80_00003", "SM00000004298_00003.xml")
        for line in invoice.invoice_line_ids:
            self.assertEqual(line.invoice_line_tax_ids[0].kind_id.code, "N6.9")

    def test_81_xml_import(self):
        # Invoice with wrong e-mail + REA code + Partner in DB
        invoice = self.invoice_from_xml("test_81_00014", "IT00488410010_00014.xml")
        self.assertEqual(invoice.partner_id, self.partner)
        self.assertEqual(invoice.partner_id.type, "contact")
        # self.assertEqual(
        #     len(self.env["res.partner"].search(
        #     [("parent_id", "=", self.partner.id)])),
        #     1)

    def test_82_xml_import(self):
        # Invoice with wrong e-mail
        self.run_wizard("test_82", "IT01641790702_00015.xml")

    def test_83_xml_import(self):
        # Invoice with wrong round
        invoice = self.invoice_from_xml("test_83", "IT02421500469_00244.xml")
        self.assertEqual(invoice.amount_untaxed, 39.08)
        self.assertEqual(invoice.amount_tax, 3.91)
        self.assertEqual(round(invoice.amount_total, 2), 42.99)
        self.assertEqual(invoice. e_invoice_amount_untaxed, 39.08)
        self.assertEqual(invoice. e_invoice_amount_tax, 3.91)
        self.assertEqual(round(invoice.e_invoice_amount_total, 2), 42.99)

    def test_84_xml_import(self):
        # Invoice with rounded amounts
        invoice = self.invoice_from_xml("test_84", "IT08973230967_9aA6M.xml")
        self.assertEqual(invoice.amount_untaxed, 36.2)
        self.assertEqual(invoice.amount_tax, 8.0)
        self.assertEqual(round(invoice.amount_total, 2), 44.2)
        self.assertEqual(invoice. e_invoice_amount_untaxed, 36.36)
        # self.assertEqual(round(invoice.e_invoice_xml_rounding, 2), 0.16)
        self.assertEqual(invoice. e_invoice_amount_tax, 8.0)
        self.assertEqual(round(invoice.e_invoice_amount_total, 2), 44.2)

    def test_901_xml_import_autogrill(self):
        # Tax rounded 1 cent
        invoice = self.invoice_from_xml("test_901_autogrill",
                                        "IT0526289001424201_AVH2R.xml")
        self.assertEqual(invoice.amount_untaxed, 23.55)
        self.assertEqual(invoice.amount_tax, 2.35)
        self.assertEqual(round(invoice.amount_total, 2), 25.9)
        self.assertEqual(invoice. e_invoice_amount_untaxed, 23.55)
        self.assertEqual(invoice. e_invoice_amount_tax, 2.35)
        self.assertEqual(round(invoice.e_invoice_amount_total, 2), 25.9)

    def test_902_xml_import_autogrill(self):
        # Tax rounded 3.3 EUR
        invoice = self.invoice_from_xml("test_902_autogrill",
                                        "IT0526289001424201_BQ1Ll.xml")
        self.assertEqual(round(invoice.amount_untaxed, 2), 58.05)
        self.assertEqual(invoice.amount_tax, 11.33)
        self.assertEqual(round(invoice.amount_total, 2), 69.38)
        self.assertEqual(invoice. e_invoice_amount_untaxed, 61.38)
        self.assertEqual(invoice. e_invoice_amount_tax, 11.33)
        self.assertEqual(round(invoice.e_invoice_amount_total, 2), 69.38)

    def test_903_xml_import_enasarco(self):
        # Invoice with WH tax
        invoice = self.invoice_from_xml("test_903_enasarco",
                                        "ITNREGCM80H30D612D_20003.xml")
        self.assertEqual(invoice.amount_untaxed, 10.0)
        self.assertEqual(invoice.amount_tax, 2.2)
        self.assertEqual(round(invoice.amount_total, 2), 12.2)
        self.assertEqual(round(invoice.amount_net_pay, 2), 11.35)
        self.assertTrue(len(invoice.invoice_line_ids) == 1)
