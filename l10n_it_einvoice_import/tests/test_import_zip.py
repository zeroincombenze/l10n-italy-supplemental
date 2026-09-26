# -*- coding: utf-8 -*-
#
# Copyright 2019-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
"""Loading sale e-invoices from a zip file."""
import base64
import io
import zipfile

from odoo.exceptions import UserError
from odoo.modules import get_module_resource
from odoo.tests.common import SingleTransactionCase

SALE_XML = "IT05111810015_00001.xml"


class TestImportZipSale(SingleTransactionCase):

    def setUp(self):
        super(TestImportZipSale, self).setUp()
        self.env.user.company_id.vat = "IT05111810015"
        self.wizard_model = self.env["wizard.einvoice.import.zip.sale"]
        self.attach_model = self.env["fatturapa.attachment.out"]

    def build_zip(self, names):
        buf = io.BytesIO()
        zf = zipfile.ZipFile(buf, "w")
        for arcname in names:
            path = get_module_resource(
                "l10n_it_einvoice_import", "tests", "data", SALE_XML
            )
            zf.write(path, arcname)
        zf.close()
        return base64.b64encode(buf.getvalue())

    def run_wizard(self, names):
        wizard = self.wizard_model.create({"zip": self.build_zip(names)})
        action = wizard.import_zip()
        return action, self.attach_model.browse(action["domain"][0][2])

    def test_01_zip_creates_sale_attachments(self):
        action, attachments = self.run_wizard([SALE_XML])
        self.assertEqual(action["res_model"], "fatturapa.attachment.out")
        self.assertEqual(len(attachments), 1)
        attachment = attachments[0]
        self.assertEqual(attachment.name, SALE_XML)
        self.assertEqual(attachment.invoices_count, 1)
        self.assertEqual(attachment.invoices_total, 122.0)
        # Already sent to SdI by whoever produced it
        self.assertTrue(attachment.imported)

    def test_02_already_loaded_file_is_not_duplicated(self):
        """Loading the same zip twice links the existing file"""
        _action, first = self.run_wizard([SALE_XML])
        _action, second = self.run_wizard([SALE_XML])
        self.assertEqual(first, second)
        self.assertEqual(
            len(self.attach_model.search([("name", "=", SALE_XML)])), 1
        )

    def test_03_files_in_subdirectories_are_read(self):
        """SdI archives nest the files in a directory"""
        _action, attachments = self.run_wizard(["a_folder/" + SALE_XML])
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].name, SALE_XML)

    def test_04_zip_without_einvoice_is_refused(self):
        with self.assertRaises(UserError):
            self.run_wizard(["not_an_einvoice.txt"])

    def test_05_non_zip_is_refused(self):
        wizard = self.wizard_model.create({"zip": base64.b64encode(b"not a zip")})
        with self.assertRaises(UserError):
            wizard.import_zip()
