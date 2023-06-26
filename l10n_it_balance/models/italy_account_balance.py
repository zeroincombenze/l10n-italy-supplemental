# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later
# (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import datetime
# import logging
import base64
import xlwt
import io
from odoo import api, fields, models
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
from . import spreadsheet_config as scg


LABELS_NATURE = {
    'A': 'Attivo',
    'P': 'Passivo',
    'R': 'Ricavi',
    'C': 'Costi',
    'O': 'C/Ordine',
}
LEVEL_BALANCE_LINE = 4
LEVEL_BALANCE_PARTNER = 5


class ItalyAccountBalance(models.Model):
    _name = 'italy.account.balance'
    _description = 'Bilancio fiscale italiano'

    def _set_balance_type(self):
        # _logger.info(self.env.context.get('balance_type'))
        if self.env.context.get('balance_type'):
            return self.env.context.get('balance_type')
        return 'trial'

    @api.model
    def get_actual_val(self, vals, name, layer=None, ttype=None):
        """Get real value from vals or from record
        @layer: 'onchange', 'create', 'write', 'validate', 'post'
        @ttype: 'company', 'company_id', 'many2one', 'id', 'date', 'datetime'
        """
        if name in vals:
            if ttype == 'date' and vals[name] and isinstance(vals[name], str):
                return datetime.datetime.strptime(
                    vals[name], '%Y-%m-%d').date()
            elif (isinstance(vals[name], int) and
                  hasattr(self, name) and
                  ttype in ('company', 'company_id', 'many2one', 'id')):
                return getattr(self, name).browse(vals[name])
            return vals[name]
        elif layer != 'create' and self and len(self) == 1:
            if ttype == 'company_id':
                if self[name]:
                    return self[name].id
                return self.env.user.company_id.id
            elif ttype == 'id':
                if self[name]:
                    return self[name].id
                return False
            else:
                return self[name]
        elif ttype == 'company_id':
            return self.env.user.company_id.id
        return False

    @api.model
    def show_error(self, vals, message, title, layer=None):
        if layer != 'onchange':
            raise UserError(message)
        warning_mess = {
            'title': title,
            'message': message
        }
        return {
            'warning': warning_mess,
            'values': vals,
        }

    @api.model
    def ret_by_layer(self, vals, layer=None):
        if layer != 'onchange':
            return vals
        return {
            'values': vals,
        }

    name = fields.Char(required=True, translate=False)
    fiscalyear_id = fields.Many2one('account.fiscal.year',
                                    required=True,
                                    string="Esercizio contabile")
    date_range_id = fields.Many2one(
        comodel_name='date.range',
        string='Date range'
    )
    date_from = fields.Date(
        string='Start date',
        required=True)
    date_to = fields.Date(
        string='End date',
        required=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",
        default=lambda self: self.env.user.company_id.id,
        required=True)
    balance_line_ids = fields.One2many(
        'italy.account.balance.line', 'balance_id', 'Balance',
        readonly=True
    )
    balance_line2_ids = fields.One2many(
        'italy.account.balance.line2', 'balance_id', 'Balance',
        readonly=True
    )
    balance_line_asset_ids = fields.One2many(
        'italy.account.balance.line.asset', 'balance_id', 'Asset',
        readonly=True
    )
    balance_line_liability_ids = fields.One2many(
        'italy.account.balance.line.liability', 'balance_id', 'Asset',
        readonly=True
    )
    balance_line_income_ids = fields.One2many(
        'italy.account.balance.line.income', 'balance_id', 'Asset',
        readonly=True
    )
    balance_line_expense_ids = fields.One2many(
        'italy.account.balance.line.expense', 'balance_id', 'Asset',
        readonly=True
    )
    balance_line_memorandum_ids = fields.One2many(
        'italy.account.balance.line.memorandum', 'balance_id', 'Asset',
        readonly=True
    )
    balance_line_accrual_ids = fields.One2many(
        'italy.account.balance.line.accrual', 'balance_id', 'Accruals',
        readonly=True
    )
    balance_line_customers_ids = fields.One2many(
        'italy.account.balance.line.customer.detail', 'balance_id', 'Asset',
        readonly=True
    )
    balance_line_suppliers_ids = fields.One2many(
        'italy.account.balance.line.supplier.detail', 'balance_id', 'Asset',
        readonly=True
    )
    balance_type = fields.Selection(
        [
            ("trial", "Trail balance"),
            ("ordinary", "Ordinary balance"),
            ("opposite", "Opposite side balance"),
        ],
        string='Balance type',
        # readonly=True,
        help="Balance type...",
        default=_set_balance_type
    )
    nature_of_accounts = fields.Selection(
        [
            ("none_excluded", "None excluded"),
            ("balance_sheets_only", "Balance sheets only"),
            ("economic_accounts_only", "Income Statement"),
            ("memorandum_accounts", "Memorandum accounts"),
        ],
        string='Nature of the accounts',
        # required=True,
        default="none_excluded",
        help="Accounts selection...",
    )
    select_details = fields.Selection(
        [
            ("all_excluded", "Tutti esclusi"),
            ("customers_suppliers",
             "Clienti e fornitori"),
            ("only_customers", "Solo clienti"),
            ("only_suppliers", "Solo fornitori"),
        ],
        string='Conti di debito e credito',
        # required=True,
        default="all_excluded",
        help="Seleziona opzioni ...",
    )
    date_balance_option = fields.Selection(
        [
            ('registration_date', 'Registration date'),
            ('competence_date', 'Competence date'),
            ('vat_date', 'VAT date'),
        ],
        string='Selezione competenza',
        required=True,
        default="registration_date",
        help="Date options...",
    )
    fiscalyear_state = fields.Selection(related='fiscalyear_id.state',
                                        readonly=True)
    no_opening_balances = fields.Boolean(string='Excluded opening balances')
    # hide_account_at_0 = fields.Selection(
    #     [('only_posted', 'Only posted accounts'),
    #      ('no_zero', 'Hide zero balance accounts'),
    #      ('all', 'All accounts')],
    #     string='Hide accounts at 0',
    #     default='no_zero')
    no_accounting_closure = fields.Boolean(
        string='Excluded accounting closure')
    no_adjustment_records = fields.Boolean(
        string='Excluded adjustment records')
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('draft', 'Only Draft Entries'),
                                    ('all', 'All Entries')],
                                   string='Target Moves',
                                   required=True,
                                   default='posted')
    order_by = fields.Selection([('APCRO', 'Patrimoniale,Costi,Ricavi,Ordine'),
                                 ('APRCO', 'Patrimoniale,Ricavi,Costi,Ordine'),
                                 ('APOCR', 'Patrimoniale,Ordine,Costi,Ricavi'),
                                 ('APORC', 'Patrimoniale,Ordine,Ricavi,Costi'),
                                 ('code', 'Codice'),
                                 ],
                                string='Printing order',
                                default='APRCO'
                                )
    hierarchy_level = fields.Selection(
        [
            ("0", "Tutti"),
            ("1", "Solo primo livello"),
            ("2", "Solo primo e secondo livello"),
            ("3", "Solo secondo e terzo livello"),
            ("4", "Solo ultimo livello"),
        ],
        string='Livello di bilancio',
        default="0",
        help="Selezione livello..."
    )
    evaluate_accrual = fields.Boolean(
        string='Calcolo competenze',
        translate=False,
        default=False)
    move_ids = fields.Many2many(
        string='Move entries', comodel_name='account.move',
        store=True)

    rounding = fields.Selection(
        [
            ("no_round", "Non applicato"),
            ("sub_round", "Arrotondamento matematico dei sottoconti"),
            ("summary_round", "Arrotondamento matematico dei capoconti"),
            ("master_round", "Arrotondamento matematico dei mastri"),
            ("smart_round", "Arrotondamento intelligente"),
        ],
        string='Arrotondamento',
        default="no_round",
        help="Selezione arrotondamento..."
    )
    receivable_account_only = fields.Boolean('Receivable account only',
                                             default=False)
    payable_account_only = fields.Boolean('Payable account only',
                                          default=False)
    no_grand_total = fields.Boolean('No grand total', default=True)
    no_nature_total = fields.Boolean('No nature total', default=False)
    no_selected_moves = fields.Boolean('No selected moves', default=False)
    inversion = fields.Selection(
        [
            ("no_inversion", "Non invertire"),
            ("account_inversion", "Inverti in base al "
                                  "corrispondente del conto"),
            ("force_inversion", "Inverti sempre"),
        ],
        string='Inversione Natura Conti con segno negativo',
        default='no_inversion')
    last_update = fields.Datetime(string='Ultimo aggiornamento', readonly=True)
    view_partner_details = fields.Selection(
        [
            ("in_balance", "Nel bilancio"),
            ("separate_list", "Scheda separata"),
        ],
        string='Dettagli conti',
        default="in_balance",
        help="Selezione visualizzazione..."
    )

    @api.model
    def check_n_set(self, vals, layer=None):
        fiscalyear = self.get_actual_val(vals, 'fiscalyear_id',
                                         ttype='many2one', layer=layer)
        if layer != 'onchange' and not fiscalyear:
            return self.show_error(vals,
                                   'Manca esercizio fiscale',
                                   'Date!', layer=layer)
        date_from = self.get_actual_val(vals, 'date_from',
                                        ttype='date', layer=layer)
        if not date_from:
            vals['date_from'] = date_from = fiscalyear.date_from
            if self:
                self.date_from = date_from
        date_to = self.get_actual_val(vals, 'date_to',
                                      ttype='date', layer=layer)
        if not date_to:
            vals['date_to'] = date_to = fiscalyear.date_to
            if self:
                self.date_to = date_to

        balance_type = self.get_actual_val(vals, 'balance_type',
                                           ttype='char', layer=layer)
        if layer not in ('write', 'create'):
            if balance_type:
                if balance_type == 'trial':
                    if self and self.order_by != 'code':
                        self.order_by = 'code'

        if (fiscalyear.date_from <= date_from <= date_to <=
                fiscalyear.date_to):
            return self.ret_by_layer(vals, layer=layer)

        if layer == 'onchange':
            self.date_from = max(date_from,
                                 self.fiscalyear_id.date_from)
            self.date_to = min(date_to,
                               self.fiscalyear_id.date_to)
            return self.show_error(vals,
                                   'Date fuori limiti esercizio contabile',
                                   'Date!', layer=layer)
        if 'date_from' in vals:
            vals['date_from'] = max(str(date_from),
                                    vals['date_from'])
        if 'date_to' in vals:
            vals['date_to'] = max(str(date_to),
                                  vals['date_to'])
        return vals

    @api.onchange('date_range_id')
    def _date_range_id(self):
        if self.date_range_id:
            self.date_from = self.date_range_id.date_start
            self.date_to = self.date_range_id.date_end
        return self.check_n_set({}, layer='onchange')

    @api.onchange('fiscalyear_id')
    def _onchange_fiscalyear_id(self):
        if self.fiscalyear_id:
            self.date_from = self.fiscalyear_id.date_from
            self.date_to = self.fiscalyear_id.date_to
        return self.check_n_set({}, layer='onchange')

    @api.onchange('date_from', 'date_to')
    def _onchange_date(self):
        return self.check_n_set({}, layer='onchange')

    @api.onchange('order_by')
    def _onchange_order_by(self):
        if self.order_by == 'code':
            self.hierarchy_level = '3'
            self.no_nature_total = True

    @api.onchange('no_opening_balances')
    def _onchange_no_opening_balances(self):
        if not self.no_opening_balances and self.fiscalyear_id:
            self.date_from = self.fiscalyear_id.date_from

    @api.multi
    def generate_trial_xls(self):
        filename = 'bilancio_di_verifica.xls'
        domain = [('balance_id', '=', self.id)]
        line_model = self.env['italy.account.balance.line']

        wb = xlwt.Workbook()
        ws = wb.add_sheet(self.display_name)

        default_money = scg.xlwt_get_col_width(len('Saldo iniziale'))

        row_index = 0
        col_index = 0
        # header
        ws.write(row_index, col_index, 'Natura', scg.STYLE_HEADER)
        col_index += 1
        ws.write(row_index, col_index, 'Conto', scg.STYLE_HEADER)
        col_index += 1
        if self.select_details in ('customers_suppliers', 'only_customers',
                                   'only_suppliers'):
            ws.write(row_index, col_index, 'Partner', scg.STYLE_HEADER)
            ws.col(col_index).width = scg.xlwt_get_col_width(20)
            col_index += 1

        ws.write(row_index, col_index, 'Descrizione', scg.STYLE_HEADER)
        ws.col(col_index).width = scg.xlwt_get_col_width(50)
        col_index += 1
        ws.write(row_index, col_index, 'Saldo iniziale', scg.STYLE_HEADER)
        ws.col(col_index).width = default_money
        col_index += 1
        ws.write(row_index, col_index, 'Totale dare', scg.STYLE_HEADER)
        ws.col(col_index).width = default_money
        col_index += 1
        ws.write(row_index, col_index, 'Totale avere', scg.STYLE_HEADER)
        ws.col(col_index).width = default_money
        col_index += 1
        ws.write(row_index, col_index, 'Saldo', scg.STYLE_HEADER)
        ws.col(col_index).width = default_money
        row_index += 1

        for line in line_model.search(domain, order='code ASC, seq2 ASC'):
            col_index = 0
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4

            ws.write(row_index, col_index, LABELS_NATURE[line.nature])
            col_index += 1
            ws.write(row_index, col_index, line.code, cstyle)
            col_index += 1

            if self.select_details in ('customers_suppliers', 'only_customers',
                                       'only_suppliers'):
                ws.write(row_index, col_index, line.partner_id.vat or '',
                         cstyle)
                col_index += 1

            ws.write(row_index, col_index, line.name, cstyle)
            col_index += 1
            ws.write(row_index, col_index, line.amount_start, cstyle)
            col_index += 1
            ws.write(row_index, col_index, line.amount_debit, cstyle)
            col_index += 1
            ws.write(row_index, col_index, line.amount_credit, cstyle)
            col_index += 1
            ws.write(row_index, col_index, line.amount_balance, cstyle)
            row_index += 1

        fp = io.BytesIO()
        wb.save(fp)
        data = {'file_export': base64.encodebytes(fp.getvalue()),
                'name': filename}
        wizard_id = self.env['wizard.balance.export.xls'].create(data)
        fp.close()
        if wizard_id and wizard_id[0]:
            act_ur = {
                'type': 'ir.actions.act_url',
                'url':  'web/content/?model=wizard.balance.export.xls&'
                        'field=file_export&download=true&id=%s&'
                        'filename=bilancio_di_verifica.xls' % wizard_id[0].id,
                'target': 'new',
            }
            return act_ur
        else:
            return False

    @api.multi
    def generate_ordinary_xls(self):
        filename = 'bilancio_ordinario.xls'
        domain = [('balance_id', '=', self.id)]
        line_model = self.env['italy.account.balance.line2']

        wb = xlwt.Workbook()
        ws = wb.add_sheet(self.display_name)
        row_index = 0
        col_index = 0

        # header
        ws.write(row_index, col_index, 'Natura', scg.STYLE_HEADER)
        col_index += 1
        ws.write(row_index, col_index, 'Conto', scg.STYLE_HEADER)
        col_index += 1
        if self.select_details in ('customers_suppliers', 'only_customers',
                                   'only_suppliers'):
            ws.write(row_index, col_index, 'Partner', scg.STYLE_HEADER)
            ws.col(col_index).width = scg.xlwt_get_col_width(20)
            col_index += 1
        ws.write(row_index, col_index, 'Descrizione', scg.STYLE_HEADER)

        ws.col(col_index).width = scg.xlwt_get_col_width(50)

        col_index += 1

        ws.write(row_index, col_index, 'Saldo', scg.STYLE_HEADER)

        ws.col(col_index).width = scg.xlwt_get_col_width(20)

        row_index += 1

        for line in line_model.search(domain, order='seq1 ASC, seq2 ASC'):
            col_index = 0
            cstyle = scg.MAIN_STYLE
            if line.level_balance == 0:
                cstyle = scg.STYLE_LEVEL_ZERO
            elif line.level_balance == 1:
                cstyle = scg.STYLE_LEVEL_1
            elif line.level_balance == 2:
                cstyle = scg.STYLE_LEVEL_2
            elif line.level_balance == 4:
                cstyle = scg.STYLE_LEVEL_4

            ws.write(row_index, col_index, LABELS_NATURE[line.nature], cstyle)
            col_index += 1
            ws.write(row_index, col_index, line.code, cstyle)
            col_index += 1
            if self.select_details in ('customers_suppliers', 'only_customers',
                                       'only_suppliers'):
                ws.write(row_index, col_index, line.partner_id.vat or '',
                         cstyle)
                col_index += 1
            ws.write(row_index, col_index, line.name, cstyle)
            col_index += 1
            ws.write(row_index, col_index, line.amount_balance, cstyle)
            row_index += 1

        fp = io.BytesIO()
        wb.save(fp)
        data = {'file_export': base64.encodebytes(fp.getvalue()),
                'name': filename}
        wizard_id = self.env['wizard.balance.export.xls'].create(data)
        fp.close()
        if wizard_id and wizard_id[0]:
            act_ur = {
                'type': 'ir.actions.act_url',
                'url':  'web/content/?model=wizard.balance.export.xls&'
                        'field=file_export&download=true&id=%s&'
                        'filename=bilancio_ordinario.xls' % wizard_id[0].id,
                'target': 'new',
            }

            return act_ur
        else:
            return False

    @api.model
    def create(self, vals):
        vals = self.check_n_set(vals, layer='create')
        return super().create(vals)

    @api.multi
    def write(self, vals):
        vals = self.check_n_set(vals, layer='write')
        if 'last_update' not in vals:
            vals.update({'last_update': False})
        super().write(vals)

    @api.multi
    def generate_balance(self):
        # active_id = self._context.get('active_id')
        return {'type': 'ir.actions.act_window_close'}


class ItalyAccountBalanceLine(models.Model):
    _name = 'italy.account.balance.line'
    _description = 'Righe bilancio fiscale italiano'
    _order = "seq1, seq2, code"

    def _compute_display_code(self):
        for rec in self:
            rec.display_code = rec.code if rec.code and rec.code.isdigit() else ' '

    parent_code = fields.Char('Codice', readonly=True, translate=False)
    code = fields.Char('Codice', readonly=True, translate=False)
    display_code = fields.Char(compute='_compute_display_code')
    name = fields.Char('Descrizione', readonly=True, translate=False)
    seq1 = fields.Integer('Sequenza 1', readonly=True,)
    seq2 = fields.Integer('Sequenza 2', readonly=True,)
    nature = fields.Selection(
        [('A', 'Attivo'),
         ('P', 'Passivo'),
         ('R', 'Ricavi'),
         ('C', 'Costi'),
         ('O', 'C/Ordine')],
        'Natura', readonly=True,
    )
    balance_id = fields.Many2one(
        'italy.account.balance', 'Balance')
    amount_start = fields.Float(
        'Saldo iniziale', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_debit = fields.Float(
        'Totale dare', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_credit = fields.Float(
        'Totale avere', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_balance = fields.Float(
        'Saldo finale', readonly=True,
        digits=dp.get_precision('Account')
    )
    account_id = fields.Many2one(
        'account.account', 'Account', readonly=True)
    parent_id = fields.Many2one(
        'account.group',
        string='Parent account', readonly=True)
    level_balance = fields.Integer('Livello di bilancio', readony=True,
                                   default=LEVEL_BALANCE_LINE)
    pos_balance = fields.Selection(
        [('E', 'Most Elevated'),
         ('H', 'High'),
         ('I', 'Intermediate'),
         ('L', 'Low'),
         ('S', 'Sub'),
         ('T', 'Gran Total')],
        'Posizione in bilancio',
        readony=True, default='L')
    to_delete = fields.Boolean('Row to delete', readony=True, default=False)
    partner_id = fields.Many2one(
        'res.partner', 'Partner')
    partner_vat = fields.Char(related='partner_id.vat', type="char",
                              string="Partita IVA", readonly=True)


class ItalyAccountBalanceLine2(models.Model):
    _name = 'italy.account.balance.line2'
    _description = 'Righe bilancio fiscale italiano'
    _order = "seq1, seq2, code"

    def _compute_display_code(self):
        for rec in self:
            rec.display_code = rec.code if rec.code and rec.code.isdigit() else ' '

    parent_code = fields.Char('Codice', readonly=True, translate=False)
    code = fields.Char('Codice', readonly=True, translate=False)
    display_code = fields.Char(compute='_compute_display_code')
    name = fields.Char('Descrizione', readonly=True, translate=False)
    seq1 = fields.Integer('Sequenza 1', readonly=True,)
    seq2 = fields.Integer('Sequenza 2', readonly=True,)
    nature = fields.Selection(
        [('A', 'Attivo'),
         ('P', 'Passivo'),
         ('R', 'Ricavi'),
         ('C', 'Costi'),
         ('O', 'C/Ordine')],
        'Natura', readonly=True,
    )
    balance_id = fields.Many2one(
        'italy.account.balance', 'Balance')
    amount_start = fields.Float(
        'Saldo iniziale', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_balance = fields.Float(
        'Saldo finale', readonly=True,
        digits=dp.get_precision('Account')
    )
    account_id = fields.Many2one(
        'account.account', 'Account', readonly=True)
    parent_id = fields.Many2one(
        'account.group',
        string='Parent account', readonly=True)
    level_balance = fields.Integer('Livello di bilancio', readony=True,
                                   default=LEVEL_BALANCE_LINE)
    pos_balance = fields.Selection(
        [('E', 'Most Elevated'),
         ('H', 'High'),
         ('I', 'Intermediate'),
         ('L', 'Low'),
         ('S', 'Sub'),
         ('T', 'Gran Total')],
        'Posizione in bilancio',
        readony=True, default='L')
    to_delete = fields.Boolean('Row to delete', readony=True, default=False)
    partner_id = fields.Many2one(
        'res.partner', 'Partner')
    partner_vat = fields.Char(related='partner_id.vat', type="char",
                              string="Partita IVA", readonly=True)


class ItalyAccountBalanceLineAsset(models.Model):
    _name = 'italy.account.balance.line.asset'
    _description = 'Righe bilancio fiscale italiano (attività)'
    _order = "seq1, seq2, code"

    def _compute_display_code(self):
        for rec in self:
            rec.display_code = rec.code if rec.code and rec.code.isdigit() else ' '

    nature = fields.Selection(
        [('A', 'Attivo'),
         ('P', 'Passivo'),
         ('R', 'Ricavi'),
         ('C', 'Costi'),
         ('O', 'C/Ordine')],
        'Natura', readonly=True,
    )
    parent_code = fields.Char('Codice', readonly=True, translate=False)
    code = fields.Char('Codice', readonly=True, translate=False)
    display_code = fields.Char(compute='_compute_display_code')
    name = fields.Char('Descrizione', readonly=True, translate=False)
    seq1 = fields.Integer('Sequenza 1', readonly=True,)
    seq2 = fields.Integer('Sequenza 2', readonly=True,)
    balance_id = fields.Many2one(
        'italy.account.balance', 'Balance')
    amount_start = fields.Float(
        'Saldo iniziale', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_debit = fields.Float(
        'Totale dare', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_credit = fields.Float(
        'Totale avere', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_balance = fields.Float(
        'Saldo finale', readonly=True,
        digits=dp.get_precision('Account')
    )
    account_id = fields.Many2one(
        'account.account', 'Account', readonly=True)
    parent_id = fields.Many2one(
        'account.group',
        string='Parent account', readonly=True)
    level_balance = fields.Integer('Livello di bilancio', readony=True,
                                   default=LEVEL_BALANCE_LINE)
    pos_balance = fields.Selection(
        [('E', 'Most Elevated'),
         ('H', 'High'),
         ('I', 'Intermediate'),
         ('L', 'Low'),
         ('S', 'Sub'),
         ('T', 'Gran Total')],
        'Posizione in bilancio',
        readony=True, default='L')
    to_delete = fields.Boolean('Row to delete', readony=True, default=False)
    partner_id = fields.Many2one(
        'res.partner', 'Partner')
    partner_vat = fields.Char(related='partner_id.vat', type="char",
                              string="Partita IVA", readonly=True)


class ItalyAccountBalanceLineLiability(models.Model):
    _name = 'italy.account.balance.line.liability'
    _description = 'Righe bilancio fiscale italiano (passività)'
    _order = "seq1, seq2, code"

    def _compute_display_code(self):
        for rec in self:
            rec.display_code = rec.code if rec.code and rec.code.isdigit() else ' '

    nature = fields.Selection(
        [('A', 'Attivo'),
         ('P', 'Passivo'),
         ('R', 'Ricavi'),
         ('C', 'Costi'),
         ('O', 'C/Ordine')],
        'Natura', readonly=True,
    )
    parent_code = fields.Char('Codice', readonly=True, translate=False)
    code = fields.Char('Codice', readonly=True, translate=False)
    display_code = fields.Char(compute='_compute_display_code')
    name = fields.Char('Descrizione', readonly=True, translate=False)
    seq1 = fields.Integer('Sequenza 1', readonly=True,)
    seq2 = fields.Integer('Sequenza 2', readonly=True,)
    balance_id = fields.Many2one(
        'italy.account.balance', 'Balance')
    amount_start = fields.Float(
        'Saldo iniziale', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_debit = fields.Float(
        'Totale dare', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_credit = fields.Float(
        'Totale avere', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_balance = fields.Float(
        'Saldo finale', readonly=True,
        digits=dp.get_precision('Account')
    )
    account_id = fields.Many2one(
        'account.account', 'Account', readonly=True)
    parent_id = fields.Many2one(
        'account.group',
        string='Parent account', readonly=True)
    level_balance = fields.Integer('Livello di bilancio', readony=True,
                                   default=LEVEL_BALANCE_LINE)
    pos_balance = fields.Selection(
        [('E', 'Most Elevated'),
         ('H', 'High'),
         ('I', 'Intermediate'),
         ('L', 'Low'),
         ('S', 'Sub'),
         ('T', 'Gran Total')],
        'Posizione in bilancio',
        readony=True, default='L')
    to_delete = fields.Boolean('Row to delete', readony=True, default=False)
    partner_id = fields.Many2one(
        'res.partner', 'Partner')
    partner_vat = fields.Char(related='partner_id.vat', type="char",
                              string="Partita IVA", readonly=True)


class ItalyAccountBalanceLineIncome(models.Model):
    _name = 'italy.account.balance.line.income'
    _description = 'Righe bilancio fiscale italiano (ricavi)'
    _order = "seq1, seq2, code"

    def _compute_display_code(self):
        for rec in self:
            rec.display_code = rec.code if rec.code and rec.code.isdigit() else ' '

    nature = fields.Selection(
        [('A', 'Attivo'),
         ('P', 'Passivo'),
         ('R', 'Ricavi'),
         ('C', 'Costi'),
         ('O', 'C/Ordine')],
        'Natura', readonly=True,
    )
    parent_code = fields.Char('Codice', readonly=True, translate=False)
    code = fields.Char('Codice', readonly=True, translate=False)
    display_code = fields.Char(compute='_compute_display_code')
    name = fields.Char('Descrizione', readonly=True, translate=False)
    seq1 = fields.Integer('Sequenza 1', readonly=True,)
    seq2 = fields.Integer('Sequenza 2', readonly=True,)
    balance_id = fields.Many2one(
        'italy.account.balance', 'Balance')
    amount_start = fields.Float(
        'Saldo iniziale', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_debit = fields.Float(
        'Totale dare', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_credit = fields.Float(
        'Totale avere', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_balance = fields.Float(
        'Saldo finale', readonly=True,
        digits=dp.get_precision('Account')
    )
    account_id = fields.Many2one(
        'account.account', 'Account', readonly=True)
    parent_id = fields.Many2one(
        'account.group',
        string='Parent account', readonly=True)
    level_balance = fields.Integer('Livello di bilancio', readony=True,
                                   default=LEVEL_BALANCE_LINE)
    pos_balance = fields.Selection(
        [('E', 'Most Elevated'),
         ('H', 'High'),
         ('I', 'Intermediate'),
         ('L', 'Low'),
         ('S', 'Sub'),
         ('T', 'Gran Total')],
        'Posizione in bilancio',
        readony=True, default='L')
    to_delete = fields.Boolean('Row to delete', readony=True, default=False)
    partner_id = fields.Many2one(
        'res.partner', 'Partner')
    partner_vat = fields.Char(related='partner_id.vat', type="char",
                              string="Partita IVA", readonly=True)


class ItalyAccountBalanceLineExpense(models.Model):
    _name = 'italy.account.balance.line.expense'
    _description = 'Righe bilancio fiscale italiano (costi)'
    _order = "seq1, seq2, code"

    def _compute_display_code(self):
        for rec in self:
            rec.display_code = rec.code if rec.code and rec.code.isdigit() else ' '

    nature = fields.Selection(
        [('A', 'Attivo'),
         ('P', 'Passivo'),
         ('R', 'Ricavi'),
         ('C', 'Costi'),
         ('O', 'C/Ordine')],
        'Natura', readonly=True,
    )
    parent_code = fields.Char('Codice', readonly=True, translate=False)
    code = fields.Char('Codice', readonly=True, translate=False)
    display_code = fields.Char(compute='_compute_display_code')
    name = fields.Char('Descrizione', readonly=True, translate=False)
    seq1 = fields.Integer('Sequenza 1', readonly=True,)
    seq2 = fields.Integer('Sequenza 2', readonly=True,)
    balance_id = fields.Many2one(
        'italy.account.balance', 'Balance')
    amount_start = fields.Float(
        'Saldo iniziale', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_debit = fields.Float(
        'Totale dare', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_credit = fields.Float(
        'Totale avere', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_balance = fields.Float(
        'Saldo finale', readonly=True,
        digits=dp.get_precision('Account')
    )
    account_id = fields.Many2one(
        'account.account', 'Account', readonly=True)
    parent_id = fields.Many2one(
        'account.group',
        string='Parent account', readonly=True)
    level_balance = fields.Integer('Livello di bilancio', readony=True,
                                   default=LEVEL_BALANCE_LINE)
    pos_balance = fields.Selection(
        [('E', 'Most Elevated'),
         ('H', 'High'),
         ('I', 'Intermediate'),
         ('L', 'Low'),
         ('S', 'Sub'),
         ('T', 'Gran Total')],
        'Posizione in bilancio',
        readony=True, default='L')
    to_delete = fields.Boolean('Row to delete', readony=True, default=False)
    partner_id = fields.Many2one(
        'res.partner', 'Partner')
    partner_vat = fields.Char(related='partner_id.vat', type="char",
                              string="Partita IVA", readonly=True)


class ItalyAccountBalanceLineMemorandum(models.Model):
    _name = 'italy.account.balance.line.memorandum'
    _description = 'Righe bilancio fiscale italiano (conti d\'ordine)'
    _order = "seq1, seq2, code"

    def _compute_display_code(self):
        for rec in self:
            rec.display_code = rec.code if rec.code and rec.code.isdigit() else ' '

    nature = fields.Selection(
        [('A', 'Attivo'),
         ('P', 'Passivo'),
         ('R', 'Ricavi'),
         ('C', 'Costi'),
         ('O', 'C/Ordine')],
        'Natura', readonly=True,
    )
    parent_code = fields.Char('Codice', readonly=True, translate=False)
    code = fields.Char('Codice', readonly=True, translate=False)
    display_code = fields.Char(compute='_compute_display_code')
    name = fields.Char('Descrizione', readonly=True, translate=False)
    seq1 = fields.Integer('Sequenza 1', readonly=True,)
    seq2 = fields.Integer('Sequenza 2', readonly=True,)
    balance_id = fields.Many2one(
        'italy.account.balance', 'Balance')
    amount_start = fields.Float(
        'Saldo iniziale', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_debit = fields.Float(
        'Totale dare', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_credit = fields.Float(
        'Totale avere', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_balance = fields.Float(
        'Saldo finale', readonly=True,
        digits=dp.get_precision('Account')
    )
    account_id = fields.Many2one(
        'account.account', 'Account', readonly=True)
    parent_id = fields.Many2one(
        'account.group',
        string='Parent account', readonly=True)
    level_balance = fields.Integer('Livello di bilancio', readony=True,
                                   default=LEVEL_BALANCE_LINE)
    pos_balance = fields.Selection(
        [('E', 'Most Elevated'),
         ('H', 'High'),
         ('I', 'Intermediate'),
         ('L', 'Low'),
         ('S', 'Sub'),
         ('T', 'Gran Total')],
        'Posizione in bilancio',
        readony=True, default='L')
    to_delete = fields.Boolean('Row to delete', readony=True, default=False)
    partner_id = fields.Many2one(
        'res.partner', 'Partner')


class ItalyAccountBalanceLineAccrual(models.Model):
    _name = 'italy.account.balance.line.accrual'
    _description = 'Ratei e risconti'

    balance_id = fields.Many2one(
        'italy.account.balance', 'Balance')
    type = fields.Selection(
        [
            ("cutoff_active", "Rateo attivo"),
            ("cutoff_passive", "Rateo passivo"),
            ("prepayment_active", "Risconto attivo"),
            ("prepayment_passive", "Risconto passivo"),
            ("cutoff_active+prepayment_passive",
             "Rateo attivo+Risconto passivo"),
            ("cutoff_passive+prepayment_active",
             "Rateo passivo+Risconto attivo"),
            ("invtobericeived_active", "Fatture da ricevere attive"),
            ("invtobericeived_passive", "Fatture da ricevere passive"),
        ],
        string='Tipo',
        readonly=True,
        help="Tipo di record",
        default='cutoff_active'
    )
    move_number = fields.Char(string='Numero registrazione',
                              readonly=True, translate=False)
    move_date = fields.Date(string='Data registrazione',
                            readonly=True, translate=False)
    move_count = fields.Char(string='Conto registrazione',
                             readonly=True, translate=False)
    invoiced_amount = fields.Float(
        'Importo da fattura', readonly=True,
        digits=dp.get_precision('Account')
    )
    expired_year_amount = fields.Float(
        'Importo consolidato', readonly=True,
        digits=dp.get_precision('Account')
    )
    previous_year_amount = fields.Float(
        'Importo periodo precedente', readonly=True,
        digits=dp.get_precision('Account')
    )
    current_year_amount = fields.Float(
        'Importo periodo corrente', readonly=True,
        digits=dp.get_precision('Account')
    )
    next_year_amount = fields.Float(
        'Importo periodo successivo', readonly=True,
        digits=dp.get_precision('Account')
    )
    start_date_competence = fields.Date(
        string='Data inizio competenza',
        translate=False,
        readonly=True)
    end_date_competence = fields.Date(
        string='Data fine competenza',
        translate=False,
        readonly=True)
    to_delete = fields.Boolean('Row to delete', readony=True, default=False)


class ItalyAccountBalanceLineCustomersDetails(models.Model):
    _name = 'italy.account.balance.line.customer.detail'
    _description = 'Righe bilancio fiscale italiano (clienti)'
    _order = "seq1, seq2, code"

    def _compute_display_code(self):
        for rec in self:
            rec.display_code = rec.code

    nature = fields.Selection(
        [('A', 'Attivo'),
         ('P', 'Passivo'),
         ('R', 'Ricavi'),
         ('C', 'Costi'),
         ('O', 'C/Ordine')],
        'Natura', readonly=True, translate=False
    )
    code = fields.Char('Codice', readonly=True, translate=False)
    display_code = fields.Char(compute='_compute_display_code')
    name = fields.Char('Descrizione', readonly=True, translate=False)
    seq1 = fields.Integer('Sequenza 1', readonly=True,)
    seq2 = fields.Integer('Sequenza 2', readonly=True,)
    balance_id = fields.Many2one(
        'italy.account.balance', 'Balance')
    partner_id = fields.Many2one(
        'res.partner', 'Partner')
    amount_start = fields.Float(
        'Saldo iniziale', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_debit = fields.Float(
        'Totale dare', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_credit = fields.Float(
        'Totale avere', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_balance = fields.Float(
        'Saldo finale', readonly=True,
        digits=dp.get_precision('Account')
    )
    account_id = fields.Many2one(
        'account.account', 'Account', readonly=True)
    level_balance = fields.Integer('Livello di bilancio', readony=True,
                                   default=LEVEL_BALANCE_PARTNER)
    pos_balance = fields.Selection(
        [('E', 'Most Elevated'),
         ('H', 'High'),
         ('I', 'Intermediate'),
         ('L', 'Low'),
         ('S', 'Sub'),
         ('T', 'Gran Total')],
        'Posizione in bilancio',
        readony=True, default='L')
    to_delete = fields.Boolean('Row to delete', readony=True, default=False)


class ItalyAccountBalanceLineSuppliersDetails(models.Model):
    _name = 'italy.account.balance.line.supplier.detail'
    _description = 'Righe bilancio fiscale italiano (fornitori)'
    _order = "seq1, seq2, code"

    def _compute_display_code(self):
        for rec in self:
            rec.display_code = rec.code

    nature = fields.Selection(
        [('A', 'Attivo'),
         ('P', 'Passivo'),
         ('R', 'Ricavi'),
         ('C', 'Costi'),
         ('O', 'C/Ordine')],
        'Natura', readonly=True, translate=False
    )
    code = fields.Char('Codice', readonly=True, translate=False)
    display_code = fields.Char(compute='_compute_display_code')
    name = fields.Char('Descrizione', readonly=True, translate=False)
    seq1 = fields.Integer('Sequenza 1', readonly=True,)
    seq2 = fields.Integer('Sequenza 2', readonly=True,)
    balance_id = fields.Many2one(
        'italy.account.balance', 'Balance')
    partner_id = fields.Many2one(
        'res.partner', 'Partner')
    amount_start = fields.Float(
        'Saldo iniziale', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_debit = fields.Float(
        'Totale dare', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_credit = fields.Float(
        'Totale avere', readonly=True,
        digits=dp.get_precision('Account')
    )
    amount_balance = fields.Float(
        'Saldo finale', readonly=True,
        digits=dp.get_precision('Account')
    )
    account_id = fields.Many2one(
        'account.account', 'Account', readonly=True)
    level_balance = fields.Integer('Livello di bilancio', readony=True,
                                   default=LEVEL_BALANCE_PARTNER)
    pos_balance = fields.Selection(
        [('E', 'Most Elevated'),
         ('H', 'High'),
         ('I', 'Intermediate'),
         ('L', 'Low'),
         ('S', 'Sub'),
         ('T', 'Gran Total')],
        'Posizione in bilancio',
        readony=True, default='L')
    to_delete = fields.Boolean('Row to delete', readony=True, default=False)
