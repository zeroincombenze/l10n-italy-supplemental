# © 2021-2022 SHS-AV srl (www.shs-av.com)

import base64
from io import BytesIO
from openpyxl import load_workbook
from unidecode import unidecode
from odoo import models, fields, api, _

# from odoo import exceptions

TNL = {
    'Codice': 'ref',
    'Nome': 'name',
    'Cliente': 'customer',
    'Fornitore': 'supplier',
    'Partita IVA': 'vat',
    'Citta': 'city',
    'Indirizzo': 'street',
    'Telefono': 'phone',
    'E-mail': 'email',
    'Nazione': 'country_id',
    'CAP': 'zip',
    'Note': 'comment',
    'Codice fiscale': 'fiscalcode',
    'Sito web': 'website',
}


class WizardImportPartners(models.Model):
    _name = "wizard.import.partners"
    _description = "Import Partners from xlsx"

    data_file = fields.Binary(
        string='Excel Data File',
        required=True,
    )
    filename = fields.Char()
    dry_run = fields.Boolean(string='Dry-run', default=False)
    tracelog = fields.Html('Result History')

    @api.multi
    def html_txt(self, text, tag):
        if tag:
            if tag in ('table', '/table', 'tr', '/tr'):
                if not text and tag == 'table':
                    text = (
                        'border="2px" cellpadding="2px" style="padding: 5px"'
                    )
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

        def get_partner(partner_domain, partner_domain_vat, partner_domain_fc,
                        partner_domain_ref, vals, html, disable_err=None):
            partner_model = self.env['res.partner']
            partner_domain.append(('type', '=', 'contact'))
            stext = ''
            if vals.get('name'):
                for ch in vals['name']:
                    if ch.isalpha():
                        if unidecode(ch) != ch:
                            stext += '_'
                        else:
                            stext += ch
                    elif not stext.endswith('%'):
                        stext += '%'
            ref_recs = []
            recs = []
            if partner_domain_ref:
                domain = [x for x in partner_domain]
                domain += partner_domain_ref
                domain.append(('name', 'ilike', stext))
                ref_recs = partner_model.search(domain)
                if not ref_recs:
                    ref_recs = partner_model.search(domain[:-1])
            if partner_domain_vat and partner_domain_fc and len(ref_recs) != 1:
                domain = [x for x in partner_domain]
                domain += partner_domain_vat
                domain += partner_domain_fc
                domain.append(('name', 'ilike', stext))
                recs = partner_model.search(domain)
                if not recs:
                    recs = partner_model.search(domain[:-1])
                if ref_recs and len(ref_recs) < len(recs):
                    recs = ref_recs
            if not recs and partner_domain_vat:
                domain = [x for x in partner_domain]
                domain += partner_domain_vat
                domain.append(('name', 'ilike', stext))
                recs = partner_model.search(domain)
                if not recs:
                    recs = partner_model.search(domain[:-1])
                if ref_recs and len(ref_recs) < len(recs):
                    recs = ref_recs
            if not recs:
                domain = [x for x in partner_domain]
                domain += partner_domain_vat
                domain.append(('name', 'ilike', stext))
                recs = partner_model.search(domain)
                if not recs:
                    recs = partner_model.search(domain[:-1])
                if ref_recs and len(ref_recs) < len(recs):
                    recs = ref_recs
            if not recs:
                domain = [x for x in partner_domain]
                domain.append(('name', 'ilike', stext))
                recs = partner_model.search(domain)
                if ref_recs and len(ref_recs) < len(recs):
                    recs = ref_recs
            if recs:
                if len(recs) > 1:
                    if html_txt:
                        html += html_txt('', 'tr')
                        html += html_txt('%s' % numrec, 'td')
                        html += html_txt('', 'td')
                        html += html_txt(vals.get('name', ''), 'td')
                        html += html_txt(row.get('vat', ''), 'td')
                        html += html_txt(_('Found multiple records.'), 'td')
                        html += html_txt('', '/tr')
                vals['id'] = recs[0].id
            else:
                if html_txt:
                        html += html_txt('', 'tr')
                        html += html_txt('%s' % numrec, 'td')
                        html += html_txt('', 'td')
                        html += html_txt(vals.get('name', ''), 'td')
                        html += html_txt(row.get('vat', ''), 'td')
                        html += html_txt(_('New record added!'), 'td')
                        html += html_txt('', '/tr')
            vals['is_company'] = True
            vals['type'] = 'contact'
            return vals, html

        html = ''
        partner_domain_vat = []
        partner_domain_fc = []
        partner_domain_ref = []
        partner_domain = []
        vals = {}
        for field in row.keys():
            name = TNL.get(field, field)
            if name == 'vat':
                if row[field]:
                    partner_domain_vat.append(('vat', '=', row[field]))
            elif name == 'fiscalcode':
                if row[field]:
                    partner_domain_fc.append(('fiscalcode', '=', row[field]))
            elif name == 'customer':
                if row[field]:
                    partner_domain.append(('customer', '=', True))
            elif name == 'supplier':
                if row[field]:
                    partner_domain.append(('supplier', '=', True))
            elif name == 'ref':
                if row[field]:
                    partner_domain_ref.append(('ref', '=', row[field]))
            elif name in ('state_id', 'country_id', ):
                if (isinstance(row[field], str) and
                        len(row[field].split('.')) == 2 and
                        ' ' not in row[field]):
                    vals[name] = self.env.ref(row[field]).id,
                elif row[field]:
                    vals[name] = row[field]
            elif row[field] is not None:
                vals[name] = row[field]

        vals, html = get_partner(partner_domain, partner_domain_vat,
                                 partner_domain_fc, partner_domain_ref,
                                 vals, html)
        return vals, html

    @api.multi
    def import_xls(self):
        model = 'res.partner'
        company_id = self.env.user.company_id.id
        tracelog = self.html_txt(_('Import Partners'), 'h3')
        numrec = 0
        tracelog += self.html_txt('', 'table')
        tracelog += self.html_txt('', 'tr')
        tracelog += self.html_txt(_('Row'), 'td')
        tracelog += self.html_txt(_('Code'), 'td')
        tracelog += self.html_txt(_('Name'), 'td')
        tracelog += self.html_txt(_('Vat'), 'td')
        tracelog += self.html_txt(_('Note'), 'td')
        tracelog += self.html_txt('', '/tr')
        datas = self.get_data()
        for row in datas:
            numrec += 1
            vals, html = self.prepare_data(
                row, company_id, numrec, html_txt=self.html_txt
            )
            tracelog += html
            if self.dry_run:
                continue
            if vals.get('id'):
                try:
                    self.env[model].browse(vals['id']).write(vals)
                except BaseException as e:
                    self._cr.rollback()  # pylint: disable=invalid-commit
                    html = self.html_txt('', 'tr')
                    html += self.html_txt('%s' % numrec, 'td')
                    html += self.html_txt('', 'td')
                    html += self.html_txt(vals.get('name', ''), 'td')
                    html += self.html_txt('', 'td')
                    html += self.html_txt(e, 'td')
                    html += self.html_txt('', '/tr')
                    tracelog += html
                    break
            else:
                try:
                    self.env[model].create(vals)
                except BaseException as e:
                    self._cr.rollback()  # pylint: disable=invalid-commit
                    html = self.html_txt('', 'tr')
                    html += self.html_txt('%s' % numrec, 'td')
                    html += self.html_txt('', 'td')
                    html += self.html_txt(vals.get('name', ''), 'td')
                    html += self.html_txt('', 'td')
                    html += self.html_txt(e, 'td')
                    html += self.html_txt('', '/tr')
                    tracelog += html
                    break
            self._cr.commit()  # pylint: disable=invalid-commit
        tracelog += self.html_txt('', '/table')
        self.tracelog = tracelog
        return {
            'name': 'Import result',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.import.partners',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'view_id': self.env.ref(
                'import_partners.wizard_import_partners_result'
            ).id,
            'domain': [('id', '=', self.id)],
        }

    def close_window(self):
        return {'type': 'ir.actions.act_window_close'}
