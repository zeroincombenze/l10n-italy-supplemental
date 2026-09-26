# -*- coding: utf-8 -*-
#
# Copyright 2019-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
"""Load a whole zip of sale e-invoices at once.

l10n_it_einvoice_import_zip does the same job for the purchase side and is
left to it: the sale counterpart lives here, in the module that owns the sale
import, so that neither module has to depend on the other.
"""
import base64
import io
import logging
import os
import re
import zipfile

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

# VAT_PROGRESSIVE.xml, the name SdI gives to an e-invoice file
FILENAME_RE = r"[A-Z]{2}[A-Za-z0-9]+_[A-Za-z0-9]{3,5}\.(xml|XML|xml\.p7m|XML\.P7M)$"
XMLNS_TOKEN = "//ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2"


class WizardEInvoiceImportZipSale(models.TransientModel):
    _name = "wizard.einvoice.import.zip.sale"
    _description = "Import sale e-invoices from zip"

    zip = fields.Binary("ZIP file", required=True)

    def get_zip_file(self):
        try:
            content = base64.b64decode(self.zip)
        except BaseException:
            raise UserError(_("Imported file is not a valid zip file"))
        if not zipfile.is_zipfile(io.BytesIO(content)):
            raise UserError(_("Imported file is not a zip file"))
        return zipfile.ZipFile(io.BytesIO(content))

    def get_attachment_values(self, xml_file, data):
        vals = {
            "name": xml_file,
            "datas_fname": xml_file,
            "type": "binary",
            "mimetype": "text/xml",
        }
        # A plain xml file carries the FatturaPA namespace and has to be
        # encoded; a signed or already encoded one does not
        if data.find(XMLNS_TOKEN) < 0:
            vals["datas"] = data
        else:
            vals["datas"] = base64.b64encode(data)
        return vals

    @api.multi
    def import_zip(self):
        self.ensure_one()
        att_model = self.env["fatturapa.attachment.out"]
        zf = self.get_zip_file()
        att_list = []
        for xml_fullfile in zf.namelist():
            xml_file = os.path.basename(xml_fullfile)
            if not re.match(FILENAME_RE, xml_file):
                continue
            # Already loaded: link to it rather than creating a duplicate,
            # the file name is unique by constraint
            attachments = att_model.search([("name", "=", xml_file)])
            if attachments:
                att_list += attachments.ids
                continue
            try:
                data = zf.read(xml_fullfile)
            except BaseException as e:
                _logger.warning(
                    "Cannot extract %s from zip file: %s" % (xml_fullfile, e)
                )
                continue
            try:
                att_list.append(
                    att_model.create(self.get_attachment_values(xml_file, data)).id
                )
            except BaseException as e:
                raise UserError(
                    _("Error %s extracting %s from zip file") % (e, xml_fullfile)
                )
        if not att_list:
            raise UserError(_("No e-invoice file found in the zip file"))
        return {
            "name": _("Imported E-invoice Files"),
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "fatturapa.attachment.out",
            "type": "ir.actions.act_window",
            "domain": [("id", "in", att_list)],
        }
