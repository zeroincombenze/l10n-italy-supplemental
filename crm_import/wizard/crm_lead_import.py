# -*- coding: utf-8 -*-
#
# Copyright 2017-2018, Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

import csv
import base64
from openerp import osv, fields, models, api
_logger = logging.getLogger(__name__)
try:
    from os0 import os0
except (ImportError, IOError) as err:
    _logger.debug(err)



class CrmLeadImport(models.Model):
    _name = 'crm.lead.import'
    _inherit = 'base_import.import'

    content_base64 = fields.Binary('Data File path',
                                   required=False,
                                   translate=False)
    filename = fields.Char('File Name', size=256)
    name = fields.Char('Name', size=256,
                       help='Marker for imported records')
    overwrite_existing = fields.Boolean('Overwrite existing',
                                        default=False)

    @api.one
    @api.constrains('filename')
    def _check_filename(self):
        if self.content_base64:
            if not self.filename:
                raise osv.except_osv_('Error!',
                                      'There is no file')
        else:
            tmp = self.filename.split('.')
            ext = tmp[len(tmp)-1]
            if ext != 'csv':
                raise osv.except_osv_('Error!',
                                      'The file must be a csv file')

    @api.model
    def _parse_all_files(self, data_file):
        """Parse one or multiple files from csv-file.

        :param data_file: Decoded raw content of the file
        :return:
        """
        crm_return_raw_list = []
        return crm_return_raw_list

    @api.model
    def _import_file(self, data_file, fields, options, dryrun=None):
        crm_lead_model = self.env['crm.lead']
        csv.register_dialect('odoo',
                             delimiter=options.get('separator', ','),
                             quotechar=options.get('quoting', '"'),
                             quoting=csv.QUOTE_MINIMAL)
        hdr_read = not options.get('headers', True)
        key_index = options.get('index', 0)
        key_name = fields[key_index]
        name_index = options.get('name_index', 1)
        ident = os0.u(options.get('name', ''))
        overwrite_existing = options.get('overwrite_existing', False)
        csv_obj = csv.DictReader(data_file.split('\n'),
                                 fieldnames=[],
                                 restkey='undef_name',
                                 dialect='odoo')
        rec_num = 0
        for row in csv_obj:
            if not hdr_read:
                hdr_read = True
                continue
            rec_num += 1
            vals = {}
            for index, val in enumerate(row['undef_name']):
                if len(val):
                    vals[fields[index]] = os0.u(val)
            if not vals[key_name]:
                raise 'Record # %d without key!' % rec_num
            if u'name' in vals:
                vals['name'] = u'%s - %s' % (ident, vals['name'])
            elif fields[name_index] in vals:
                vals['name'] = u'%s - %30.30s' % (
                    ident,
                    vals.get(fields[name_index], '').split('\n')[0])
            else:
                vals['name'] = ident
            ids = crm_lead_model.search([(key_name, '=', vals[key_name])])
            if ids:
                if overwrite_existing:
                    del vals[key_name]
                    crm_lead_model.browse(ids.id).write(vals)
            else:
                crm_lead_model.create(vals)
        return True

    @api.multi
    def import_file(self, data_file):
        self.ensure_one()
        data_file = base64.b64decode(self.content_base64)
        # self.with_context(
        #     active_id=self.id
        # )._import_file(data_file)
        self.res_model = 'crm.lead'
        self.file = data_file
        self.file_name = self.filename
        self.file_type = 'csv'
        fields = [
            'email_from',
            'description',
            'contact_name',
            'partner_name',
            'phone'
        ]
        options = {
            'quoting': '"',
            'separator': ';',
            'headers': True,
            'index': 0,
            'name_index': 1,
            'name': self.name,
            'overwrite_existing': self.overwrite_existing,
        }
        # self.do(fields, options, dryrun=True)
        return self._import_file(data_file, fields, options, dryrun=False)
