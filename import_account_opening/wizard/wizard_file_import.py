# © 2021-2022 SHS-AV srl (www.shs-av.com)

import base64
from io import BytesIO
from openpyxl import load_workbook
from odoo import models, fields, api, _
# from odoo import exceptions

TNL = {
    'Codice': 'code',
    'Nome': 'name',
    'Cliente': 'customer',
    'Fornitore': 'supplier',
    'Partita IVA': 'vat',
    'Dare': 'debit',
    'Avere': 'credit',
}


class WizardImportAccountOpening(models.Model):
    _name = "wizard.import.account.opening"
    _description = "Import Account Opening from xlsx"

    data_file = fields.Binary(
        string='Excel Data File',
        required=True,
    )
    filename = fields.Char()
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        required=True)
    account_id = fields.Many2one(
        'account.account',
        string='Open account',
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
        partner_domain = []
        acc_domain = []
        vals = {}
        by_vat = by_code = False
        for field in row.keys():
            name = TNL.get(field)
            if name == 'vat':
                if row[field]:
                    partner_domain.append(('vat', '=', row[field]))
                    by_vat = field
            elif name == 'customer':
                if row[field]:
                    partner_domain.append(('customer', '=', True))
            elif name == 'supplier':
                if row[field]:
                    partner_domain.append(('supplier', '=', True))
            elif name == 'code':
                if row[field]:
                    acc_domain.append(('code', '=', row[field]))
                    by_code = field
            elif name in ('debit', 'credit'):
                vals[name] = row[field] or 0.0
            elif name == 'name':
                vals[name] = row[field] or ''
        if by_vat:
            partner_domain.append(('type', '=', 'contact'))
            recs = self.env['res.partner'].search(partner_domain)
            if recs:
                if len(recs) > 1:
                    if html_txt:
                        html += html_txt('', 'tr')
                        html += html_txt('%s' % numrec, 'td')
                        html += html_txt('', 'td')
                        html += html_txt(vals.get('name', ''), 'td')
                        html += html_txt(row.get(by_vat, ''), 'td')
                        html += html_txt(_('Found multiple records.'), 'td')
                        html += html_txt('', '/tr')
                    vals['partner_id'] = recs[0].id
                    if vals.get('supplier'):
                        vals['account_id'] = recs[
                            0].property_account_payable_id.id
                    else:
                        vals['account_id'] = recs[
                            0].property_account_receivable_id.id
                    by_code = False
            else:
                if html_txt:
                    html += html_txt('', 'tr')
                    html += html_txt('%s' % numrec, 'td')
                    html += html_txt('', 'td')
                    html += html_txt(vals.get('name', ''), 'td')
                    html += html_txt(row.get(by_vat, ''), 'td')
                    html += html_txt(_('No record found!'), 'td')
                    html += html_txt('', '/tr')
                vals = {}
        elif by_code:
            acc_domain.append(('company_id', '=', company_id))
            recs = self.env['account.account'].search(acc_domain)
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
                vals['account_id'] = recs[0].id
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
        model = 'account.move'
        company_id = self.env.user.company_id.id
        model_dtl = 'account.move.line'
        move = self.env[model].create({
            'company_id': company_id,
            'journal_id': self.journal_id.id,
            'move_type': 'other',
            'type': 'entry',
            'ref': 'apertura conti',
        })
        tracelog = self.html_txt(_('Import account entries'), 'h3')
        numrec = 0
        tracelog += self.html_txt('', 'table')
        tracelog += self.html_txt('', 'tr')
        tracelog += self.html_txt(_('Row'), 'td')
        tracelog += self.html_txt(_('Code'), 'td')
        tracelog += self.html_txt(_('Name'), 'td')
        tracelog += self.html_txt(_('Vat'), 'td')
        tracelog += self.html_txt(_('Note'), 'td')
        tracelog += self.html_txt('', '/tr')
        # self.tracelog = travislog
        move_list = [move.id]
        datas = self.get_data()
        total_debit = total_credit = 0.0
        for row in datas:
            numrec += 1
            vals, html = self.prepare_data(row, company_id, numrec,
                                           html_txt=self.html_txt)
            # self.tracelog += html
            tracelog += html
            if not vals:
                continue
            vals['move_id'] = move.id
            try:
                self.env[model_dtl].with_context(
                    check_move_validity=False).create(vals)
                total_debit += vals.get('debit') or 0.0
                total_credit += vals.get('credit') or 0.0
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
        vals = {
            'move_id': move.id,
            'account_id': self.account_id.id,
            'name': 'risultato di esercizio',
        }
        if total_credit > total_debit:
            vals['debit'] = total_credit - total_debit
        else:
            vals['credit'] = total_debit - total_credit
        self.env[model_dtl].create(vals)
        tracelog += self.html_txt('', '/table')
        self.tracelog = tracelog
        return {
            'name': 'Import result',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.import.account.opening',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {
                'active_id': self.id,
                'move_list': move_list
            },
            'view_id': self.env.ref(
                'import_account_opening.wizard_import_account_opening_result'
            ).id,
            'domain': [('id', '=', self.id)],
        }

    def close_window(self):
        return {'type': 'ir.actions.act_window_close'}
