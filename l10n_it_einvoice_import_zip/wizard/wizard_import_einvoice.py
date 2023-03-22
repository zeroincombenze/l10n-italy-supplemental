# -*- coding: utf-8 -*-
#
# Copyright 2019-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
import os
import io
import base64
import zipfile
import re
# from datetime import datetime
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class WizardAccountInvoiceImportZip(models.TransientModel):
    _name = "wizard.einvoice.import.zip"
    _description = "Import E-bill from zip"

    zip = fields.Binary('ZIP file')
    type = fields.Selection(
        [('purchase', 'Purchase Invoices'),
         ('sale', 'Sale Invoices')],
        'Invoice type',
        default='purchase')

    @api.multi
    def import_zip(self):
        if not zipfile.is_zipfile(io.BytesIO(base64.b64decode(self.zip))):
            raise UserError('Imported file is not a zip file')
        zf = zipfile.ZipFile(io.BytesIO(base64.b64decode(self.zip)))
        att_list = []
        # ir_att_model = self.env['ir.attachment']
        if self.type == 'sale':
            model = 'fatturapa.attachment.out'
            att_model = self.env[model]
        else:
            model = 'fatturapa.attachment.in'
        att_model = self.env[model]
        rex = r'[A-Z]{2}[A-Za-z0-9]+_[A-Za-z0-9]{5}\.(xml|XML|xml.p7m|XML.P7m)'
        token_id = b'//ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2'
        for xml_fullfile in zf.namelist():
            xml_file = os.path.basename(xml_fullfile)
            if re.match(rex, xml_file):
                rec_ids = att_model.search([('name', '=', xml_file)])
                if rec_ids:
                    att_list += [x.id for x in rec_ids]
                    continue
                try:
                    data = zf.read(xml_fullfile)
                except BaseException as e:
                    continue
                vals = {
                    'name': xml_file,
                    'datas_fname': xml_file,
                    'type': 'binary',
                    'mimetype': 'text/xml',
                }
                encoded = True if token_id not in data else False
                if encoded:
                    vals['datas'] = data
                else:
                    # vals['datas'] = data.encodebytes()
                    vals['datas'] = base64.encodebytes(data)
                try:
                    att_id = att_model.create(vals)
                    att_list.append(att_id.id)
                except BaseException as e:
                    raise UserError(
                        'Error %s extracting %s from zip file' % (
                            e, xml_fullfile))
        return {
            'name': "Imported Attachment",
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': model,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', att_list)],
            'view_id': False,
        }
