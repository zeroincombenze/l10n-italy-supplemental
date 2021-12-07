# © 2021-2022 SHS-AV srl (www.shs-av.com)

import base64
from io import BytesIO
from openpyxl import load_workbook
from odoo import models, fields, api, _
# from odoo import exceptions

TNL = {
    'Codice': 'default_code',
    'Nome': 'name',
    'Quantità': 'product_qty',
}


class WizardImportAccountOpening(models.Model):
    _name = "wizard.import.inventory"
    _description = "Import inventory from xlsx"

    data_file = fields.Binary(
        string='Excel Data File',
        required=True,
    )
    filename = fields.Char()
    name = fields.Char(
        string='Name',
        required=True)
    location_id = fields.Many2one(
        'stock.location',
        string='Location',
        required=True)
    tracelog = fields.Html('Result History')

    @api.multi
    def html_txt(self, text, tag):
        if tag:
            if tag in ('table', '/table', 'tr', '/tr'):
                if not text and tag == 'table':
                    text = 'border="2px" cellpadding="2px" style="padding: 5px"'
                if text:
                    html = '<%s %s>' % (tag, text)
                elif tag.startswith('/'):
                    html = '<%s>\n' % tag
                else:
                    html = '<%s>' % tag
            else:
                html = '<%s>%s</%s>' % (tag, text, tag)
        else:
            html = text
        return html

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

    def prepare_data(self, row, company_id, numrec, html_txt=None):
        html = ''
        product_domain = []
        vals = {}
        by_vat = by_code = False
        for field in row.keys():
            name = TNL.get(field)
            if name == 'default_code':
                if row[field]:
                    product_domain.append(('default_code', '=', row[field]))
                    by_code = field
            elif name == 'product_qty':
                vals[name] = row[field] or 0.0
            # elif name == 'name':
            #     vals[name] = row[field] or ''
        if by_code:
            recs = self.env['product.product'].search(product_domain)
            if len(recs) != 1:
                if html_txt:
                    html += html_txt('', 'tr')
                    html += html_txt('%s' % numrec, 'td')
                    html += html_txt(row.get(by_code, ''), 'td')
                    html += html_txt(vals.get('name', ''), 'td')
                    html += html_txt('', 'td')
                    if len(recs) > 1:
                        html += html_txt(_('Found multiple records.'), 'td')
                    else:
                        html += html_txt(_('No record found!'), 'td')
                    html += html_txt('', '/tr')
                vals = {}
            else:
                vals['product_id'] = recs[0].id
                vals['product_uom_id'] = recs[0].uom_id.id
        else:
            if html_txt:
                html += html_txt('', 'tr')
                html += html_txt('%s' % numrec, 'td')
                html += html_txt('', 'td')
                html += html_txt(vals.get('name', ''), 'td')
                html += html_txt('', 'td')
                html += html_txt(_('Record without data'), 'td')
                html += html_txt('', '/tr')
            vals = {}
        return vals, html

    @api.multi
    def import_xls(self):
        model = 'stock.inventory'
        company_id = self.env.user.company_id.id
        model_dtl = 'stock.inventory.line'
        inventory = self.env[model].create({
            'company_id': company_id,
            'name': self.name,
            'location_id': self.location_id.id,
        })
        tracelog = self.html_txt(_('Inventory entries'), 'h3')
        numrec = 0
        tracelog += self.html_txt('', 'table')
        tracelog += self.html_txt('', 'tr')
        tracelog += self.html_txt(_('Row'), 'td')
        tracelog += self.html_txt(_('Code'), 'td')
        tracelog += self.html_txt(_('Name'), 'td')
        tracelog += self.html_txt(_('Qty'), 'td')
        tracelog += self.html_txt(_('Note'), 'td')
        tracelog += self.html_txt('', '/tr')
        datas = self.get_data()
        for row in datas:
            numrec += 1
            vals, html = self.prepare_data(row, company_id, numrec,
                                           html_txt=self.html_txt)
            tracelog += html
            if not vals:
                continue
            vals['inventory_id'] = inventory.id
            vals['location_id'] = self.location_id.id
            try:
                self.env[model_dtl].create(vals)
            except BaseException as e:
                html = self.html_txt('', 'tr')
                html += self.html_txt('%s' % numrec, 'td')
                html += self.html_txt('', 'td')
                html += self.html_txt(vals.get('name', ''), 'td')
                html += self.html_txt('', 'td')
                html += self.html_txt(e, 'td')
                html += self.html_txt('', '/tr')
                tracelog += html
                break
        tracelog += self.html_txt('', '/table')
        self.tracelog = tracelog
        return {
            'name': 'Import result',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.import.inventory',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'view_id': self.env.ref(
                'import_inventory.wizard_import_inventory_result'
            ).id,
            'domain': [('id', '=', self.id)],
        }

    def close_window(self):
        return {'type': 'ir.actions.act_window_close'}
