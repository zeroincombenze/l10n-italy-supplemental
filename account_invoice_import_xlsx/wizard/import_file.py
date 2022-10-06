# -*- coding: utf-8 -*-
# © 2021-2022 SHS-AV srl (www.shs-av.com)

from past.builtins import basestring
import base64
from io import BytesIO
from openpyxl import load_workbook
from unidecode import unidecode
from odoo import models, fields, api, _
# from odoo.exceptions import UserError

TNL = {
    'Denominazione Cliente': 'partner_id',
    'Partita Iva': 'vat',
    'Codice Fiscale': 'fiscalcode',
    'Codice': 'default_code',
    'Nome': 'name',
    'Quantita': 'quantity',
    'Imponibile': 'price_subtotal',
    'Iva': 'price_tax',
    'Numero': 'move_name',
    'Data': 'date_invoice',
}


class WizardImportInvoiceFileXlsx(models.Model):
    _name = "wizard.import.invoice.file.xlsx"
    _description = "Import invoice lines from xlsx"

    def _default_journal(self):
        return self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]

    data_file = fields.Binary(
        string='Excel Data File',
        # required=True,
    )
    filename = fields.Char()

    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        required=True,
        default=_default_journal,
        domain=[('type', '=', ['sale', 'purchase'])]
    )
    date_invoice = fields.Date(
        string='Invoice Date')
    dry_run = fields.Boolean(
        string='Dry-run',
        default=False)
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

    def get_dim_text(self, name):
        stext = ''
        for ch in name:
            if ch.isalpha():
                if unidecode(ch) != ch:
                    stext += '_'
                else:
                    stext += ch
            elif not stext.endswith('%'):
                stext += '%'
        return stext

    def get_iso_date(self, date):
        if isinstance(date, basestring):
            sep = False
            for sep in ('/', '-', '.'):
                if sep in date:
                    fields = date.split(sep)
                    break
            if sep:
                if len(fields[0]) != 4:
                    pass
                date = '%04s-%02s-%02s' % (int(fields[2]),
                                           int(fields[1]),
                                           int(fields[0]))
        return date

    def get_float_eval(self, value):
        if isinstance(value, basestring):
            return eval(value.replace('.', '').replace(',', '.'))
        return value

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

    def get_partner(self, disable_err=None, search_by=None, html_txt=None):

        def write_html(html, html_txt, mesg):
            if html_txt:
                html += html_txt('', 'tr')
                html += html_txt('%s' % self.numrow, 'td')
                html += html_txt('', 'td')
                html += html_txt(self.partner_vals.get('name', ''), 'td')
                html += html_txt(
                    self.partner_vals.get(self.partner_vals.get('vat', '')),
                    'td')
                html += html_txt(mesg, 'td')
                html += html_txt('', '/tr')
            return html

        html = ''
        partner_model = self.env['res.partner']
        search_by = search_by or self.partner_search_by or 'vat'

        domain = [x for x in self.partner_domain]
        domain.append(('type', '=', 'contact'))
        stext = ''
        if self.partner_vals.get('name'):
            for ch in self.partner_vals['name']:
                if ch.isalpha():
                    if unidecode(ch) != ch:
                        stext += '_'
                    else:
                        stext += ch
                elif not stext.endswith('%'):
                    stext += '%'
        if search_by == 'vat,fiscalcode':
            domain.append(('vat', '=', self.partner_vals['vat']))
            domain.append(('fiscalcode', '=', self.partner_vals['fiscalcode']))
        elif search_by != 'name' and stext:
            domain.append((search_by, '=', self.partner_vals[search_by]))
        if stext:
            domain.append(('name', 'ilike', stext))
        partners = partner_model.search(domain)
        if not partners and search_by != 'name' and stext:
            partners = partner_model.search(domain[:-1])
        if partners:
            if len(partners) > 1:
                html = write_html(html, html_txt, _('Found multiple records.'))
            partner = partners[0]
        else:
            if not disable_err:
                html = write_html(html, html_txt, _('No partner found.'))
            partner = False
        return partner, html

    def get_product(self, disable_err=None, search_by=None, html_txt=None):

        def write_html(html, html_txt):
            if html_txt:
                html += html_txt('', 'tr')
                html += html_txt('%s' % self.numrow, 'td')
                html += html_txt(
                    self.product_vals.get('default_code', ''), 'td')
                html += html_txt(self.product_vals.get('name', ''), 'td')
                html += html_txt('', 'td')
                html += html_txt(_('Found multiple records.'), 'td')
                html += html_txt('', '/tr')
            return html

        html = ''
        product_model = self.env['product.product']

        stext = self.get_dim_text(self.line_vals.get('name'))
        search_by = search_by or self.product_search_by or 'default_code'
        domain = [x for x in self.product_domain]
        domain.append((search_by, '=', self.product_vals[search_by]))
        if stext:
            domain.append(('name', 'ilike', stext))
        products = product_model.search(domain)
        if not products and stext:
            products = product_model.search(domain[:-1])
        if products:
            if len(products) > 1:
                html = write_html(html, html_txt)
            product = products[0]
        else:
            if not disable_err:
                html = write_html(html, html_txt)
            product = False
        return product, html

    def unpack_data(self, row):
        self.invoice_domain = []
        self.invoice_search_by = []
        self.invoice_vals = {
            'date_invoice': self.date_invoice,
            'journal_id': self.journal_id.id,
        }
        self.line_vals = {
            'name': 'Prodotto generico',
            'uom_id': self.env.ref('product.product_uom_unit').id,
            'price_unit': 0.0,
        }
        self.partner_domain = []
        self.partner_search_by = []
        self.partner_vals = {}
        self.product_domain = []
        self.product_search_by = []
        self.product_vals = {}

        self.sequence = None
        line_subtotal = 0.0

        for field in row.keys():
            name = TNL.get(field, field)
            if name == 'sequence':
                self.sequence = row[field]
            elif not row[field]:
                continue
            elif name == 'vat':
                if row[field].isdigit():
                    self.partner_vals[name] = 'IT%s' % row[field]
                else:
                    self.partner_vals[name] = row[field]
                self.partner_search_by.insert(0, 'vat')
                if 'fiscalcode' in self.partner_search_by:
                    self.partner_search_by.insert(0, 'vat,fiscalcode')
            elif name == 'fiscalcode':
                self.partner_vals[name] = row[field]
                self.partner_search_by.append('fiscalcode')
                if 'vat' in self.partner_search_by:
                    self.partner_search_by.insert(0, 'vat,fiscalcode')
            elif name == 'partner_id':
                if isinstance(row[field], basestring):
                    self.partner_search_by.append('name')
                    self.partner_vals['name'] = row[field]
                elif isinstance(row[field], int):
                    self.invoice_vals['partner_id'] = row[field]
                    self.partner_search_by = []
            elif name == 'customer':
                if row[field]:
                    self.partner_domain.append(('customer', '=', True))
                    self.sale_purchase = 'sale'
            elif name == 'supplier':
                if row[field]:
                    self.partner_domain.append(('supplier', '=', True))
                    self.sale_purchase = 'purchase'
            elif name in ('move_name', ):
                self.invoice_vals[name] = row[field]
            elif name in ('date_invoice', ):
                self.invoice_vals[name] = self.get_iso_date(row[field])
            elif name == 'default_code':
                self.product_search_by.insert(0, name)
                self.product_vals[name] = row[field]
            elif name == 'quantity':
                self.line_vals[name] = self.get_float_eval(row[field]) or 0.0
            elif name == 'name':
                self.line_vals[name] = row[field] or ''
            elif (name == 'price_subtotal' and
                  not self.line_vals.get('quantity') and
                  not self.line_vals.get('price_unit')):
                self.line_vals['price_unit'] = self.get_float_eval(
                    row[field]) or 0.0
                self.line_vals['quantity'] = 1
                line_subtotal = self.get_float_eval(
                    self.line_vals['price_unit'])
            elif name == 'price_tax' and line_subtotal:
                rate = round(
                    self.get_float_eval(row[field]) * 100 / line_subtotal, 0)
                for tax_rate in (22, 10, 5, 4, 0):
                    if tax_rate >= rate:
                        break
                if self.sale_purchase == 'sale':
                    code = '%sv' % tax_rate
                elif self.sale_purchase == 'purchase':
                    code = '%sa' % tax_rate
                self.line_vals['invoice_line_tax_ids'] = [
                    (6, 0, [self.taxes[code]])]

    def unpack_partner(self):
        html = ''
        if self.sequence == 0 or self.sequence is None:
            if (not self.invoice_vals.get('partner_id') and
                    self.partner_search_by):
                for ii, by in enumerate(self.partner_search_by):
                    cont = (ii + 1) < len(self.partner_search_by)
                    partner, html = self.get_partner(
                        search_by=by, html_txt=self.html_txt,
                        disable_err=cont)
                    if partner:
                        self.invoice_vals['partner_id'] = partner.id
                        break
        return html

    def unpack_product(self):
        product = False
        html = ''
        if self.sequence or self.sequence is None:
            if (not self.line_vals.get('product_id') and
                    self.product_search_by):
                for ii, by in enumerate(self.product_search_by):
                    cont = (ii + 1) < len(self.product_search_by)
                    product, html = self.get_product(
                        search_by=by, html_txt=self.html_txt,
                        disable_err=cont)
                    if product:
                        self.line_vals['product_id'] = product.id
                        break
        return product, html

    def header_exits(self):
        return self.partner_search_by and 'partner_id' in self.invoice_vals

    def line_exits(self):
        return ('name' in self.line_vals and
                self.line_vals['name'] and
                self.line_vals['quantity'] and
                self.line_vals['price_unit'])

    def prepare_line_data(self, invoice):
        inv_line_model = self.env['account.invoice.line']
        self.line_vals['invoice_id'] = invoice.id
        self.line_vals['account_id'] = invoice.journal_id.default_debit_account_id.id
        # if self.product:
        #     self.line_vals["default_code"] = self.product.default_code
        #     account = inv_line_model.get_invoice_line_account(
        #         invoice.type, self.product, invoice.fiscal_position_id,
        #         invoice.company_id)
        #     self.line_vals['account_id'] = account.id

    def create_invoice(self, vals, html_txt=None):
        html = ''
        inv_model = self.env['account.invoice']
        if self.dry_run:
            if html_txt:
                html = html_txt('', 'tr')
                html += html_txt('%s' % self.numrow, 'td')
                html += html_txt('', 'td')
                html += html_txt(vals.get('move_name', ''), 'td')
                html += html_txt('', 'td')
                html += html_txt(_('Invoice will be created.'), 'td')
                html += html_txt('', '/tr')
            return True, html
        return inv_model.create(vals), html

    def create_invoice_line(self, vals, html_txt=None):
        html = ''
        line_model = self.env['account.invoice.line']
        if self.dry_run:
            if html_txt:
                html = html_txt('', 'tr')
                html += html_txt('%s' % self.numrow, 'td')
                html += html_txt('', 'td')
                html += html_txt(vals.get('name', ''), 'td')
                html += html_txt('', 'td')
                html += html_txt(_('Line will be created.'), 'td')
                html += html_txt('', '/tr')
            return html
        line = line_model.create(vals)
        name = vals["name"]
        line._onchange_product_id()
        line._compute_price()
        line._set_taxes()
        if hasattr(line, 'update_from_pricelist'):
            line.update_from_pricelist()
        line.write({"name": name})
        return html

    def store_tax_ids(self):
        # Search for taxes IDs
        self.taxes = {}
        for rate in (0, 4, 5, 10, 22):
            for tax in self.env['account.tax'].search(
                    [('amount', '=', rate),
                     ('company_id', '=', self.company.id)]
            ):
                if tax.type_tax_use == 'sale':
                    code = '%sv' % rate
                    if code not in self.taxes:
                        self.taxes[code] = tax.id
                elif tax.type_tax_use == 'purchase':
                    code = '%sa' % rate
                    if code not in self.taxes:
                        self.taxes[code] = tax.id

    def import_file_xlsx(self):
        tracelog = self.html_txt(_('Import invoices'), 'h3')
        tracelog += self.html_txt('', 'table')
        tracelog += self.html_txt('', 'tr')
        tracelog += self.html_txt(_('Row'), 'td')
        tracelog += self.html_txt(_('Code'), 'td')
        tracelog += self.html_txt(_('Name'), 'td')
        tracelog += self.html_txt(_('Vat'), 'td')
        tracelog += self.html_txt(_('Note'), 'td')
        tracelog += self.html_txt('', '/tr')

        # wizard common data
        self.numrow = 0
        if self.env.context.get('active_ids', False):
            self.company = False
        else:
            self.company = self.env.user.company_id
            self.store_tax_ids()
        self.sale_purchase = self.journal_id.type

        inv_model = self.env['account.invoice']
        datas = self.get_data()
        if self.env.context.get('active_ids', False):
            for invoice in inv_model.browse(
                    self.env.context['active_ids']):
                if invoice.company_id != self.company:
                    self.company = invoice.company_id
                    self.store_tax_ids()
                for row in datas:
                    self.numrow += 1
                    self.unpack_data(row)
                    self.product, html = self.unpack_product()
                    tracelog += html
                    self.prepare_line_data(invoice)
                    html = self.create_invoice_line(
                        self.line_vals, html_txt=self.html_txt)
                    tracelog += html
                invoice.compute_taxes()
        else:
            invoice = False
            for row in datas:
                self.numrow += 1
                self.unpack_data(row)
                html = self.unpack_partner()
                tracelog += html
                if self.header_exits():
                    if invoice and invoice is not True:
                        invoice.compute_taxes()
                    invoice, html = self.create_invoice(
                        self.invoice_vals, html_txt=self.html_txt)
                    tracelog += html
                if invoice and invoice is not True:
                    self.line_vals['invoice_id'] = invoice.id
                    if not self.line_vals.get('account_id'):
                        self.line_vals['account_id'] = (
                            invoice.journal_id.default_debit_account_id.id)
                self.product, html = self.unpack_product()
                tracelog += html
                if invoice and self.line_exits():
                    self.prepare_line_data(invoice)
                    html = self.create_invoice_line(
                        self.line_vals, html_txt=self.html_txt)
                    tracelog += html
            if invoice and invoice is not True:
                invoice.compute_taxes()
        tracelog += self.html_txt('', '/table')
        self.tracelog = tracelog
        if not self.env.context.get('active_ids', False):
            return {
                'name': 'Import result',
                'type': 'ir.actions.act_window',
                'res_model': 'wizard.import.invoice.file.xlsx',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'new',
                'view_id': self.env.ref(
                    'account_invoice_import_xlsx.wizard_import_invoice_result'
                ).id,
                'domain': [('id', '=', self.id)],
            }

    def close_window(self):
        return {'type': 'ir.actions.act_window_close'}
