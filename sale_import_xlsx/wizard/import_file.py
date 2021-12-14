# -*- coding: utf-8 -*-
# © 2021-2022 SHS-AV srl (www.shs-av.com)

import base64
from io import BytesIO
from openpyxl import load_workbook
from odoo import models, fields, _
from odoo import exceptions

TNL = {
    'Codice': 'default_code',
    'Nome': 'name',
    'Quantita': 'product_uom_qty',
}


class WizardImportSaleFileXlsx(models.Model):
    _name = "wizard.import.sale.file.xlsx"
    _description = "Import sale order lines from xlsx"

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

    def prepare_data(self, order, row):
        product_domain = []
        vals = {
            'product_uom': self.env.ref('product.product_uom_unit').id,
            'price_unit': 0.0,
            'order_id': order.id,
        }
        by_code = False
        for field in row.keys():
            name = TNL.get(field)
            if name == 'default_code':
                if row[field]:
                    product_domain.append(('default_code', '=', row[field]))
                    by_code = field
            elif name == 'product_uom_qty':
                vals[name] = row[field] and row[field].strip() or 0.0
            elif name == 'name':
                vals[name] = row[field] or ''
        if by_code:
            recs = self.env['product.product'].search(product_domain)
            if len(recs) == 1:
                product = recs[0]
                vals['product_id'] = recs[0].id
                vals['product_uom'] = recs[0].uom_id.id
        return vals

    def import_file_xlsx(self):
        order_model = self.env['sale.order']
        line_model = self.env['sale.order.line']
        datas = self.get_data()
        for order in order_model.browse(
                self.env.context.get('active_ids', False)):
            row_ctr = 1
            for row in datas:
                row_ctr += 1
                vals = self.prepare_data(order, row)
                if not vals or not vals.get('product_uom_qty'):
                    continue
                if not vals.get('product_id'):
                    raise exceptions.Warning(
                        _('Invalid or missed code in line %d (%s)') % (
                            row_ctr, vals.get('name')))
                try:
                    line = line_model.create(vals)
                except BaseException as e:
                    raise exceptions.Warning(
                        _('Error %s in line %d') % (e, row_ctr))
                line.product_id_change()
                line._compute_amount()
                line._compute_tax_id()
                line.write({})
        return {
        }