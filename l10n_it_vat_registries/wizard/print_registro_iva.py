# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError


class WizardRegistroIva(models.TransientModel):
    _name = "wizard.registro.iva"
    _description = "Run VAT registry"

    date_range_id = fields.Many2one('date.range', string="Date range")
    from_date = fields.Date('From date', required=True)
    to_date = fields.Date('To date', required=True)
    filter_date = fields.Selection([
        ('date', 'Data contabile'),
        ('date_apply_vat', 'Data di competenza'),
        ],
        string='Data di ricerca', required=True, default='date')

    layout_type = fields.Selection([
        ('customer', 'Customer Invoices'),
        ('supplier', 'Supplier Invoices'),
        ('corrispettivi', 'Sums due'), ],
        'Layout', required=True, default='customer')
    tax_registry_id = fields.Many2one('account.tax.registry', 'VAT registry')
    journal_ids = fields.Many2many(
        'account.journal',
        'registro_iva_journals_rel',
        'journal_id',
        'registro_id',
        string='Journals',
        help='Select journals you want retrieve documents from')
    message = fields.Char(string='Message', size=64, readonly=True)
    only_totals = fields.Boolean(
        string='Prints only totals')
    fiscal_page_base = fields.Integer('Last printed page', required=True)
    year_footer = fields.Char(
        string='Year for Footer',
        help="Value printed near number of page in the footer")

    @api.onchange('tax_registry_id')
    def on_change_tax_registry_id(self):
        self.journal_ids = self.tax_registry_id.journal_ids
        self.layout_type = self.tax_registry_id.layout_type

    @api.onchange('date_range_id')
    def on_change_date_range_id(self):
        if self.date_range_id:
            self.from_date = self.date_range_id.date_start
            self.to_date = self.date_range_id.date_end

    @api.onchange('from_date')
    def get_year_footer(self):
        if self.from_date:
            self.year_footer = self.from_date.year

    def _get_move_ids(self, wizard):

        domain = [('journal_id', 'in', [j.id for j in self.journal_ids]),
                  ('state', '=', 'posted'),
                  ]

        filter_date = wizard.filter_date

        if filter_date == 'date_apply_vat':

            order_by = 'date_apply_vat, name'

            date_domain = []
            date_domain.append('|'),
            date_domain.append('&'),
            date_domain.append(('date_apply_vat', '<>', False)),
            date_domain.append(('date_apply_vat', '>=', self.from_date)),
            date_domain.append('&'),
            date_domain.append(('date_apply_vat', '=', False)),
            date_domain.append(('date', '>=', self.from_date)),
            date_domain.append('|'),
            date_domain.append('&'),
            date_domain.append(('date_apply_vat', '<>', False)),
            date_domain.append(('date_apply_vat', '<=', self.to_date)),
            date_domain.append('&'),
            date_domain.append(('date_apply_vat', '=', False)),
            date_domain.append(('date', '<=', self.to_date)),
        else:
            order_by = 'date, name'
            date_domain = [
                ('date', '>=', self.from_date),
                ('date', '<=', self.to_date),
                ]

        default_domain = domain + date_domain

        moves = self.env['account.move'].search(default_domain, order=order_by)
        return moves.ids

    @api.multi
    def print_registro(self):
        self.ensure_one()
        wizard = self
        if not wizard.journal_ids:
            raise UserError(_('No journals found in the current selection.\n'
                              'Please load them before to retry!'))
        move_ids = self._get_move_ids(wizard)

        datas_form = dict()
        datas_form['from_date'] = wizard.from_date
        datas_form['to_date'] = wizard.to_date
        datas_form['filter_date'] = wizard.filter_date
        datas_form['journal_ids'] = [j.id for j in wizard.journal_ids]
        datas_form['fiscal_page_base'] = wizard.fiscal_page_base
        datas_form['registry_type'] = wizard.layout_type
        datas_form['year_footer'] = wizard.year_footer

        lang_code = self.env.user.company_id.partner_id.lang
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        datas_form['date_format'] = date_format

        if wizard.tax_registry_id:
            datas_form['tax_registry_name'] = wizard.tax_registry_id.name
        else:
            datas_form['tax_registry_name'] = ''
        datas_form['only_totals'] = wizard.only_totals
        # report_name = 'l10n_it_vat_registries.report_registro_iva'
        report_name = 'l10n_it_vat_registries.action_report_registro_iva'
        datas = {
            'ids': move_ids,
            'model': 'account.move',
            'form': datas_form
        }
        return self.env.ref(report_name).report_action(self, data=datas)
