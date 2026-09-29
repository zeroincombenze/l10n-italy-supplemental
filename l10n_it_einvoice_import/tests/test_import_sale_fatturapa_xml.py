# -*- coding: utf-8 -*-
#
# Copyright 2018-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
"""Test sale e-invoice import.

The xml fixture is a plain TD01 issued by the company itself: it checks that
the roles of the header are read the other way round of a purchase file, and
that journal, account and taxes come from the sale side.
"""
import base64
import logging
import tempfile

from odoo.exceptions import UserError, ValidationError
from odoo.modules import get_module_resource
from odoo.tests.common import SingleTransactionCase

_logger = logging.getLogger(__name__)

COMPANY_VAT = "IT05111810015"
SALE_XML = "IT05111810015_00001.xml"
PURCHASE_XML = "IT01234567890_FPR03.xml"


class CommonMixin(object):
    """Helpers shared by the test classes below."""

    def create_sale_tax_22(self):
        AccountTax = self.env["account.tax"]
        taxes = AccountTax.search(
            [
                ("type_tax_use", "=", "sale"),
                ("amount", "=", 22.0),
                ("company_id", "=", self.env.user.company_id.id),
            ]
        )
        if taxes:
            return taxes[0]
        account_id = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_current_assets").id,
                    )
                ],
                limit=1,
            )
            .id
        )
        return AccountTax.create(
            {
                "company_id": self.env.user.company_id.id,
                "name": "22% sale e-invoice",
                "description": "22v",
                "type_tax_use": "sale",
                "amount_type": "percent",
                "amount": 22.0,
                "account_id": account_id,
                "refund_account_id": account_id,
                "sequence": 1,
            }
        )

    def getFile(self, filename, module_name="l10n_it_einvoice_import"):
        path = get_module_resource(module_name, "tests", "data", filename)
        with open(path) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return path, out.read()

    def create_attachment(
        self, file_name, module_name="l10n_it_einvoice_import", datas_fname=None
    ):
        return self.attach_model.create(
            {
                "name": datas_fname or file_name,
                "datas": self.getFile(file_name, module_name=module_name)[1],
                "datas_fname": datas_fname or file_name,
            }
        )

    def run_wizard(
        self, file_name, module_name="l10n_it_einvoice_import", datas_fname=None
    ):
        attachment = self.create_attachment(
            file_name, module_name=module_name, datas_fname=datas_fname
        )
        wizard = self.wizard_model.with_context(
            active_ids=[attachment.id], active_model="fatturapa.attachment.out"
        ).create({})
        return attachment, wizard.importFatturaPA()


class TestSaleFatturaPAXMLImport(SingleTransactionCase, CommonMixin):

    def setUp(self):
        super(TestSaleFatturaPAXMLImport, self).setUp()
        self.env.user.company_id.vat = COMPANY_VAT
        self.tax_22 = self.create_sale_tax_22()
        self.attach_model = self.env["fatturapa.attachment.out"]
        self.wizard_model = self.env["wizard.import.fatturapa.sale"]
        self.invoice_model = self.env["account.invoice"]
        self.sale_journal = self.env["account.journal"].search(
            [
                ("type", "=", "sale"),
                ("company_id", "=", self.env.user.company_id.id),
            ],
            limit=1,
        )

    def test_01_attachment_reads_xml(self):
        """Data of a file with no linked invoice come from the xml itself"""
        customer = self.env["res.partner"].create(
            {"name": "SOCIETA' ALPHA SRL", "vat": "IT02780790107",
             "is_company": True, "customer": True}
        )
        attachment = self.create_attachment(SALE_XML)
        self.assertEqual(attachment.invoices_count, 1)
        self.assertFalse(attachment.registered)
        # A file loaded from outside is flagged as soon as it is uploaded
        self.assertTrue(attachment.imported)
        self.assertEqual(attachment.invoices_total, 122.0)
        self.assertEqual(attachment.date_invoice0, "2026-01-15")
        self.assertEqual(attachment.invoices_number, "2026/0001")
        # The buyer is looked up, never created, while computing the fields
        self.assertEqual(attachment.invoice_partner_id, customer)

    def test_02_import_sale_invoice(self):
        """A sale xml file creates a customer invoice"""
        attachment, action = self.run_wizard(SALE_XML)
        invoice = self.invoice_model.browse(action["domain"][0][2][0])
        # Roles of the header: the company issued the invoice
        self.assertEqual(invoice.type, "out_invoice")
        self.assertEqual(invoice.company_id.vat, COMPANY_VAT)
        self.assertEqual(invoice.partner_id.vat, "IT02780790107")
        self.assertTrue(invoice.partner_id.customer)
        # Sale side accounting
        self.assertEqual(invoice.journal_id.type, "sale")
        self.assertEqual(
            invoice.account_id, invoice.partner_id.property_account_receivable_id
        )
        # Document data
        self.assertEqual(invoice.reference, "2026/0001")
        # The number sent to SdI is forced, not taken from the journal sequence
        self.assertEqual(invoice.move_name, "2026/0001")
        self.assertEqual(invoice.date_invoice, "2026-01-15")
        self.assertEqual(invoice.amount_untaxed, 100.0)
        self.assertEqual(invoice.amount_total, 122.0)
        self.assertEqual(invoice.e_invoice_amount_total, 122.0)
        self.assertEqual(invoice.fiscal_document_type_id.code, "TD01")
        self.assertEqual(invoice.comment.strip(), "Vendita di prova")
        # Line and its tax, taken from sale taxes
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        line = invoice.invoice_line_ids[0]
        self.assertEqual(line.name, "Prodotto di vendita")
        self.assertEqual(line.quantity, 2.0)
        self.assertEqual(line.price_unit, 50.0)
        self.assertEqual(len(line.invoice_line_tax_ids), 1)
        self.assertEqual(line.invoice_line_tax_ids[0].type_tax_use, "sale")
        # e-invoice detail lines
        self.assertEqual(len(invoice.e_invoice_line_ids), 1)
        self.assertEqual(invoice.e_invoice_line_ids[0].uom, "NR")
        # The file is now linked and flagged
        self.assertTrue(attachment.imported)
        self.assertEqual(attachment.out_invoice_ids, invoice)
        self.assertTrue(attachment.registered)

    def test_02b_forced_number_survives_validation(self):
        """The validated invoice keeps the number the xml file carries

        account.move.post() uses invoice.move_name when set, so the invoice
        must not be renumbered by the sale journal sequence: the number is
        already known to SdI and to the customer.
        """
        attachment, action = self.run_wizard(SALE_XML, datas_fname="number.xml")
        invoice = self.invoice_model.browse(action["domain"][0][2][0])
        self.assertEqual(invoice.move_name, "2026/0001")
        invoice.invoice_validate()
        invoice.action_move_create()
        self.assertEqual(invoice.number, "2026/0001")
        self.assertEqual(invoice.move_id.name, "2026/0001")

    def test_02c_invoice_in_chosen_journal(self):
        """The invoice is created in the sale journal chosen in the wizard"""
        journal = self.sale_journal.copy(
            {"name": "E-invoice import", "code": "EIMP"}
        )
        attachment = self.create_attachment(SALE_XML, datas_fname="journal.xml")
        wizard = self.wizard_model.with_context(
            active_ids=[attachment.id], active_model="fatturapa.attachment.out"
        ).create({"journal_id": journal.id})
        action = wizard.importFatturaPA()
        invoice = self.invoice_model.browse(action["domain"][0][2][0])
        self.assertEqual(invoice.journal_id, journal)

    def test_02d_journal_must_be_sale(self):
        """Wizard refuses a journal other than a sale one"""
        self.assertEqual(self.wizard_model.create({}).journal_id, self.sale_journal)
        purchase_journal = self.env["account.journal"].search(
            [
                ("type", "=", "purchase"),
                ("company_id", "=", self.env.user.company_id.id),
            ],
            limit=1,
        )
        with self.assertRaises(ValidationError):
            self.wizard_model.create({"journal_id": purchase_journal.id})

    def test_03_already_imported(self):
        """A file already linked to invoices is not imported twice"""
        attachment, action = self.run_wizard(SALE_XML)
        wizard = self.wizard_model.with_context(
            active_ids=[attachment.id], active_model="fatturapa.attachment.out"
        )
        with self.assertRaises(UserError):
            wizard.create({}).importFatturaPA()

    def test_04_foreign_seller_refused(self):
        """A file whose seller is not this company is refused"""
        attachment = self.create_attachment(
            PURCHASE_XML, module_name="l10n_it_einvoice_in"
        )
        wizard = self.wizard_model.with_context(
            active_ids=[attachment.id], active_model="fatturapa.attachment.out"
        ).create({})
        with self.assertRaises(UserError):
            wizard.importFatturaPA()

    def test_05_unreadable_file_does_not_break_compute(self):
        """An attachment whose file is gone must not break the computed fields

        A database restored without its filestore has attachments whose datas
        is empty: reading their fields, as the ORM does when it recomputes a
        whole table on install, used to raise XMLSyntaxError.
        """
        attachment = self.attach_model.create(
            {"name": "gone.xml", "datas": "", "datas_fname": "gone.xml"}
        )
        self.assertFalse(attachment.registered)
        self.assertEqual(attachment.invoices_count, 0)
        self.assertFalse(attachment.invoice_partner_id)
        # The whole table is read the way init_models does after install
        for att in self.attach_model.search([]):
            att.registered
            att.invoices_count
            att.invoice_partner_id

    def test_06_registered_is_searchable(self):
        """registered is not stored, so it needs a working search method"""
        attachment, action = self.run_wizard(SALE_XML, datas_fname="reg.xml")
        not_registered = self.attach_model.search([("registered", "=", False)])
        registered = self.attach_model.search([("registered", "=", True)])
        self.assertIn(attachment, registered)
        self.assertNotIn(attachment, not_registered)


class TestSaleEInvoiceSendState(SingleTransactionCase, CommonMixin):
    """Interaction with l10n_it_einvoice_send2sdi.

    That module is loaded after this one, so its "state" field only exists in
    the registry once every module is in: these tests must run post_install.
    """

    at_install = False
    post_install = True

    def setUp(self):
        super(TestSaleEInvoiceSendState, self).setUp()
        self.env.user.company_id.vat = COMPANY_VAT
        self.tax_22 = self.create_sale_tax_22()
        self.attach_model = self.env["fatturapa.attachment.out"]
        self.wizard_model = self.env["wizard.import.fatturapa.sale"]

    def test_07_uploaded_file_is_not_sent_again(self):
        """An uploaded file must never sit in the state the send cron picks up

        send_all_xml_invoices() of l10n_it_einvoice_send2sdi sends every
        attachment whose state is "ready". A sale xml file was already sent to
        SdI by whoever produced it, so it must not be in that state, not even
        in the hour between the upload and the import.
        """
        attachment = self.create_attachment(SALE_XML, datas_fname="notsent.xml")
        self.assertTrue(attachment.imported)
        if "state" not in attachment._fields:
            self.skipTest("l10n_it_einvoice_send2sdi is not installed")
        self.assertEqual(attachment.state, "sent")
        # and the wizard keeps it that way
        wizard = self.wizard_model.with_context(
            active_ids=[attachment.id], active_model="fatturapa.attachment.out"
        ).create({})
        wizard.importFatturaPA()
        self.assertEqual(attachment.state, "sent")

    def test_08_exported_file_stays_ready(self):
        """A file generated by the export wizard is still to be sent"""
        attachment = self.attach_model.with_context(einvoice_export=True).create(
            {
                "name": "exported.xml",
                "datas": self.getFile(SALE_XML)[1],
                "datas_fname": "exported.xml",
            }
        )
        self.assertFalse(attachment.imported)
        if "state" not in attachment._fields:
            self.skipTest("l10n_it_einvoice_send2sdi is not installed")
        self.assertEqual(attachment.state, "ready")
