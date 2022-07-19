# -*- coding: utf-8 -*-
# © 2021-2022 SHS-AV srl (www.shs-av.com)

from datetime import datetime
import base64
from io import BytesIO
from openpyxl import load_workbook
from odoo import models, fields, api, _
from odoo import exceptions as UserError

TNL = {
    'Data contabile': 'date',
    'Dare': 'amount',
    'Avere': 'amount',
    'Divisa': 'currency_id',
    'Causale': 'note',
    'Valuta': '',
    'Descrizione': 'name',
}


class WizardImportAccountBankStatement(models.Model):
    _name = "wizard.import.account.bank.statement"
    _description = "Import account bank statement from Excel"

    data_file = fields.Binary(
        string='Excel Data File',
        required=True,
    )
    filename = fields.Char()

    def get_data(self):
        contents = []
        wb = load_workbook(BytesIO(base64.b64decode(self.data_file)))
        sheet = wb.active
        colnames = []
        for column in sheet.columns:
            colnames.append(column[0].value)
        hdr = True
        for line in sheet.rows:
            if hdr:
                hdr = False
                continue
            row = {}
            for column, cell in enumerate(line):
                row[colnames[column]] = cell.value
            contents.append(row)
        return contents

    def prepare_data(self, row):
        vals = {
            'company_id': self.env.user.company_id.id,
            'statement_id': self.env.context['active_id']
        }
        for field in row.keys():
            name = TNL.get(field)
            if not name:
                continue
            if name not in self.env['account.bank.statement.line']:
                raise UserError(_("Field %s not mapped" % name))
            if name == 'currency_id':
                vals[name] = self.env['res.currency'].search(
                    [('name', '=', row[field])]).id
            elif name == 'amount':
                if row[field]:
                    vals[name] = row[field]
            else:
                vals[name] = row[field]
        return vals

    @api.multi
    def import_statement_xls(self):
        self.ensure_one()
        if self.env['account.bank.statement'].browse(
                self.env.context['active_id']).state != "open":
            raise UserError(_("Cannot import on confirmed statement"))
        model_dtl = 'account.bank.statement.line'
        datas = self.get_data()
        for row in datas:
            vals = self.prepare_data(row)
            self.env[model_dtl].create(vals)
