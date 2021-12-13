# -*- coding: utf-8 -*-
# © 2021-2022 SHS-AV srl (www.shs-av.com)

import base64
from io import BytesIO
from openpyxl import load_workbook
from odoo import models, fields, _
# from odoo import exceptions

TNL = {
    'Codice': 'default_code',
    'Nome': 'name',
    'Quantità': 'quantity',
}


class WizardImportInvoiceFileXlsx(models.Model):
    _name = "wizard.import.invoice.file.xlsx"
    _description = "Import invoice lines from xlsx"

    data_file = fields.Binary(
        string='Excel Data File',
        required=True,
    )
    filename = fields.Char()

    def get_data(self):
        contents = []
        wb = load_workbook(BytesIO(base64.b64decode(self.data_file)))
        for sheet in wb:
            break
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

    def prepare_data(self, invoice, row):
        product_domain = []
        vals = {
            'uom_id': self.env.ref('product.product_uom_unit').id,
            'price_unit': 0.0,
            'invoice_id': invoice.id,
            'account_id': invoice.journal_id.default_debit_account_id.id,
        }
        by_code = False
        for field in row.keys():
            name = TNL.get(field)
            if name == 'default_code':
                if row[field]:
                    product_domain.append(('default_code', '=', row[field]))
                    by_code = field
            elif name == 'quantity':
                vals[name] = row[field] or 0.0
            elif name == 'name':
                vals[name] = row[field] or ''
        if by_code:
            recs = self.env['product.product'].search(product_domain)
            if len(recs) == 1:
                product = recs[0]
                vals['product_id'] = recs[0].id
                vals['uom_id'] = recs[0].uom_id.id
                vals['account_id'] = self.env[
                    'account.invoice.line'].get_invoice_line_account(
                    invoice.type, product, invoice.fiscal_position_id,
                    invoice.company_id).id
        return vals

    def import_file_xlsx(self):
        inv_model = self.env['account.invoice']
        line_model = self.env['account.invoice.line']
        datas = self.get_data()
        for invoice in inv_model.browse(
                self.env.context.get('active_ids', False)):
            for row in datas:
                line = line_model.create(
                    self.prepare_data(invoice, row))
                line._onchange_product_id()
                line._compute_price()
                line._set_taxes()
                line.write({})
        return {
        }
