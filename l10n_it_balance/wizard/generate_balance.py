# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from datetime import datetime, date
import logging

from odoo import models, fields, api
from odoo.exceptions import Warning
from odoo.http import request

_logger = logging.getLogger(__name__)

ID_2_NATURE = {
    'A': 'asset',
    'P': 'liability',
    'R': 'income',
    'C': 'expense',
    'O': 'memorandum',
}
NATURE_2_ID = {}
for x in ID_2_NATURE.keys():
    NATURE_2_ID[ID_2_NATURE[x]] = x
NATURE_NAMES = {
    'A': 'ATTIVITÀ',
    'P': 'PASSIVITÀ',
    'R': 'RICAVI',
    'C': 'COSTI',
    'O': 'CONTI D\'ORDINE',
}
OPPOSITE_NATURE = {
    'A': 'P',
    'P': 'A',
    'C': 'R',
    'R': 'C'
}
LINE_SEL = {
    'trial': '1',
    'ordinary': '2',
}
AMOUNT_NAMES = ('amount_start',
                'amount_debit',
                'amount_credit',
                'amount_balance')

NATURE_ECONOMIC_ACCOUNT_CODE = 'economic_accounts_only'
SEQ2_INCR = 100
SEQ2_LAST = 100000
SEQ2_GT = 999999
INDENTING_SPACE = u"\u00A0\u00A0"
LEVEL_BALANCE_LINE = 4
LEVEL_BALANCE_PARTNER = 5

NATURE = 0
SEQ2 = 0
CODE = 1
NAME = 2
PARENT_ID = 3
ACCOUNT_ID = 4
AMT_START = 5
AMT_DBT = 6
AMT_CRD = 7
AMT_BAL = 8
REF_ID = 9
PNAME = 10
ACC_TYPE = 11
PARTNER_ID = 12
DATE_FROM = 7
DATE_TO = 8
FY_ID = 12
LEV_BALANCE = 9

ACCRUAL_TYPES = {
    'name': {
        'cutoff_active': 'Rateo attivo',
        'cutoff_passive': 'Rateo passivo',
        'prepayment_active': 'Risconto attivo',
        'prepayment_passive': 'Risconto passivo',
    },
    'nature': {
        'cutoff_active': 'A',
        'prepayment_active': 'A',
        'cutoff_passive': 'P',
        'prepayment_passive': 'P',
    },
    'code': {
        'cutoff_active': 'CA',
        'prepayment_active': 'PA',
        'cutoff_passive': 'CP',
        'prepayment_passive': 'PP',
    }
}

ACCRUAL_MESSAGES = {
    'cutoff_active': {
        'empty': 'Conto Ratei attivi non impostato.',
        'wrong_type': 'Conto Ratei attivi di tipo non corretto.',
        'nature': 'A',
    },
    'cutoff_passive': {
        'empty': 'Conto Ratei passivi non impostato.',
        'wrong_type': 'Conto Ratei passivi di tipo non corretto.',
        'nature': 'P'
    },
    'prepayment_active': {
        'empty': 'Conto Risconti attivi non impostato.',
        'wrong_type': 'Conto Risconti di tipo non corretto.',
        'nature': 'A'
    },
    'prepayment_passive': {
        'empty': 'Conto Risconti passivi non impostato.',
        'wrong_type': 'Conto Risconti passivi di tipo non corretto.',
        'nature': 'P'
    },
    'invtobericeived_active': {
        'empty': 'Conto Fatture clienti da emettere non impostato.',
        'wrong_type': 'Conto Fatture clienti da emettere di tipo non corretto.',
        'nature': 'A'
    },
    'invtobericeived_passive': {
        'empty': 'Conto Fatture fornitori da ricevere non impostato.',
        'wrong_type': 'Conto Fatture fornitori da ricevere di tipo '
                      'non corretto.',
        'nature': 'P'
    },
    'refundtobericeived_active': {
        'empty': 'Conto NC fornitori da ricevere non impostato.',
        'wrong_type': 'Conto NC fornitori da ricevere di tipo non corretto.',
        'nature': 'A',
    },
    'refundtobericeived_passive': {
        'empty': 'Conto NC clienti da emettere non impostato.',
        'wrong_type': 'Conto NC clienti da emettere di tipo non corretto.',
        'nature': 'P',
    },

}


class WizardGenerateBalance(models.TransientModel):
    _name = 'wizard.generate.balance'
    _description = "Genera Bilancio"

    def _set_defval(self, nm):
        active_id = self.env.context.get('active_id')
        if not active_id:
            return False
        balance = self.env['italy.account.balance'].browse(active_id)
        if nm in ('date_from',
                  'date_to',
                  'target_move',
                  'order_by',
                  'date_balance_option',
                  'nature_of_accounts',
                  'balance_type',
                  'select_details',
                  'no_accounting_closure',
                  'no_adjustment_records',
                  'no_opening_balances',
                  'hide_account_at_0',
                  'hierarchy_level',
                  'evaluate_accrual',
                  'rounding',
                  'payable_account_only',
                  'receivable_account_only',
                  'no_grand_total',
                  'no_nature_total',
                  'no_selected_moves',
                  'inversion',
                  'last_update',
                  'view_partner_details'
                  ):
            return balance[nm]
        if nm in ('fiscalyear_id',
                  'company_id',
                  'date_range_id',):
            if balance[nm]:
                return balance[nm].id
        if nm in ('move_ids',):
            if balance[nm]:
                return [x.id for x in balance[nm]]
        return False

    def _set_fiscal_year(self):
        return self._set_defval('fiscalyear_id')

    def _set_date_from(self):
        return self._set_defval('date_from')

    def _set_date_to(self):
        return self._set_defval('date_to')

    def _set_company_id(self):
        return self._set_defval('company_id')

    def _set_target_move(self):
        return self._set_defval('target_move')

    def _set_order_by(self):
        return self._set_defval('order_by')

    def _set_date_balance_option(self):
        return self._set_defval('date_balance_option')

    def _set_nature_of_accounts(self):
        return self._set_defval('nature_of_accounts')

    def _set_balance_type(self):
        return self._set_defval('balance_type')

    def _set_date_range_id(self):
        return self._set_defval('date_range_id')

    def _set_select_details(self):
        return self._set_defval('select_details')

    def _set_no_accounting_closure(self):
        return self._set_defval('no_accounting_closure')

    def _set_no_adjustment_records(self):
        return self._set_defval('no_adjustment_records')

    def _set_no_opening_balances(self):
        return self._set_defval('no_opening_balances')

    def _set_hide_account_at_0(self):
        return self._set_defval('hide_account_at_0')

    def _set_hierarchy_level(self):
        return self._set_defval('hierarchy_level')

    def _set_evaluate_accrual(self):
        return self._set_defval('evaluate_accrual')

    def _set_move_ids(self):
        return self._set_defval('move_ids')

    def _set_rounding(self):
        return self._set_defval('rounding')

    def _set_receivable_account_only(self):
        return self._set_defval('receivable_account_only')

    def _set_payable_account_only(self):
        return self._set_defval('payable_account_only')

    def _set_no_grand_total(self):
        return self._set_defval('no_grand_total')

    def _set_no_nature_total(self):
        return self._set_defval('no_nature_total')

    def _set_no_selected_moves(self):
        return self._set_defval('no_selected_moves')

    def _set_inversion(self):
        return self._set_defval('inversion')

    def _set_last_update(self):
        return self._set_defval('last_update')

    def _set_view_partner_details(self):
        return self._set_defval('view_partner_details')

    @api.one
    def show_profile_warning(self):
        message = 'Profile contabile non rilevato'
        warning_mess = {
            'title': 'Profile contabile non rilevato',
            'message': message
        }
        return {'warning': warning_mess}

    name = fields.Char(readonly=True, translate=False)

    fiscalyear_id = fields.Many2one(
        comodel_name='account.fiscal.year', string="Esercizio contabile",
        default=_set_fiscal_year,
        readonly=True, required=True)

    date_from = fields.Date(string='Start date',
                            default=_set_date_from,
                            readonly=True, required=True)

    date_to = fields.Date(string='End date',
                          default=_set_date_to,
                          readonly=True, required=True)

    date_range_id = fields.Many2one(
        comodel_name='date.range',
        string='Date range',
        readonly=True,
        default=_set_date_range_id
    )

    company_id = fields.Many2one(
        comodel_name='res.company', string="Company",
        default=_set_company_id,
        readonly=True, required=True)

    balance_type = fields.Selection(
        [
            ("trial", "Trail balance"),
            ("ordinary", "Ordinary balance"),
            ("opposite", "Budget in opposite sections"),
        ],
        string='Balance type',
        readonly=True,
        help="Balance type...",
        default=_set_balance_type
    )

    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('draft', 'Only Draft Entries'),
                                    ('all', 'All Entries')],
                                   string='Target Moves',
                                   default=_set_target_move,
                                   readonly=True, required=True)

    order_by = fields.Selection([('APCRO', 'Patrimoniale,Costi,Ricavi,Ordine'),
                                 ('APRCO', 'Patrimoniale,Ricavi,Costi,Ordine'),
                                 ('APOCR', 'Patrimoniale,Ordine,Costi,Ricavi'),
                                 ('APORC', 'Patrimoniale,Ordine,Ricavi,Costi'),
                                 ('code', 'Codice'),
                                 ],
                                string='Printing order',
                                default=_set_order_by,
                                readonly=True, required=True)

    date_balance_option = fields.Selection(
        [
            ('registration_date', 'Registration date'),
            ('competence_date', 'Competence date'),
            ('vat_date', 'VAT date'),
        ],
        string='Selezione competenza',
        readonly=True,
        default=_set_date_balance_option,
    )

    nature_of_accounts = fields.Selection(
        [
            ("none_excluded", "None excluded"),
            ("balance_sheets_only", "Balance sheets only"),
            (NATURE_ECONOMIC_ACCOUNT_CODE, "Economic accounts only"),
            ("memorandum_accounts", "Memorandum accounts"),
        ],
        string='Nature of the accounts',
        readonly=True,
        default=_set_nature_of_accounts,
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
        readonly=True,
        default=_set_select_details)

    no_accounting_closure = fields.Boolean(
        string='Excluded accounting closure',
        default=_set_no_accounting_closure,
        readonly=True)

    no_adjustment_records = fields.Boolean(
        string='Excluded adjustment records',
        default=_set_no_adjustment_records,
        readonly=True)

    no_opening_balances = fields.Boolean(
        string='Excluded opening balances',
        default=_set_no_opening_balances,
        readonly=True)

    # hide_account_at_0 = fields.Selection(
    #     [('only_posted', 'Only posted accounts'),
    #      ('no_zero', 'Hide zero balance accounts'),
    #      ('all', 'All accounts')],
    #     string='Hide accounts at 0',
    #     default=_set_hide_account_at_0,
    #     readonly=True)

    hierarchy_level = fields.Selection(
        [
            ("0", "Tutti"),
            ("1", "Solo primo livello"),
            ("2", "Solo primo e secondo livello"),
            ("4", "Solo secondo e terzo livello"),
            ("3", "Solo ultimo livello"),
        ],
        string='Livello di bilancio',
        default=_set_hierarchy_level,
        readonly=True
    )

    evaluate_accrual = fields.Boolean(
        string='Calcola competenze',
        translate=False,
        default=_set_evaluate_accrual,
        readonly=True
    )

    move_ids = fields.Many2many(
        string='Move entires', comodel_name='account.move',
        default=_set_move_ids,
        readonly=True)

    rounding = fields.Selection(
        [
            ("no_round", "Non applicato"),
            ("sub_round", "Arrotondamento matematico dei sottoconti"),
            ("summary_round", "Arrotondamento matematico dei capoconti"),
            ("master_round", "Arrotondamento matematico dei mastri"),
            ("smart_round", "Arrotondamento intelligente"),
        ],
        string='Arrotondamento',
        default=_set_rounding,
        readonly=True
    )
    receivable_account_only = fields.Boolean('Receivable account only',
                                             readonly=True,
                                             default=_set_receivable_account_only)
    payable_account_only = fields.Boolean('Payable account only',
                                          readonly=True,
                                          default=_set_payable_account_only)
    no_grand_total = fields.Boolean('No grand total',
                                    default=_set_no_grand_total,
                                    readonly=True)
    no_nature_total = fields.Boolean('No nature total',
                                     readonly=True,
                                     default=_set_no_nature_total)
    no_selected_moves = fields.Boolean('No selected moves',
                                       default=_set_no_selected_moves,
                                       readonly=True)
    inversion = fields.Selection(
        [
            ("no_inversion", "Non invertire"),
            ("account_inversion", "Inverti in base al "
                                  "corrispondente del conto"),
            ("force_inversion", "Inverti sempre"),
        ],
        readonly=True,
        string='Inversione Natura Conti con segno negativo',
        default=_set_inversion)

    last_update = fields.Datetime(string='Ultimo aggiornamento',
                                  default=_set_last_update,
                                  readonly=True)
    view_partner_details = fields.Selection(
        [
            ("in_balance", "Nel bilancio"),
            ("separate_list", "Scheda separata"),
        ],
        string='Dettagli conti',
        default=_set_view_partner_details,
        readonly=True
    )

    def lpad_name_by_level(self, name, level_balance):
        return '%s%s' % (INDENTING_SPACE * int(level_balance),
                         name.strip())

    def vals_from_sqlrow(self, row, params,
                  nature=None, seq2=None, level_balance=None):

        def get_acc_lev_balance(account_id):
            level_balance = 1
            group = self.env['account.account'].browse(account_id).group_id
            while group:
                level_balance += 1
                group = group.parent_id
            return level_balance

        # Initialize dictionary vals from fetched row
        level_balance = level_balance or get_acc_lev_balance(row[ACCOUNT_ID])
        nature = nature or row[NATURE]
        self.seq2[nature] += SEQ2_INCR
        vals = {
            'nature': nature,
            'seq1': self.seq1[nature],
            'seq2': seq2 or self.seq2[nature],
            'balance_id': params['active_id'],
            'code': row[CODE],
            'name': self.lpad_name_by_level(row[NAME], level_balance),
            'to_delete': False,
            'parent_id': row[PARENT_ID],
            'account_id': row[ACCOUNT_ID],
            'level_balance': level_balance,
            'pos_balance': 'L',
        }
        if (level_balance == LEVEL_BALANCE_PARTNER and
                len(row) > 10 and row[PNAME]):
            vals['name'] = self.lpad_name_by_level(row[PNAME], level_balance)
            vals['pos_balance'] = 'S'
        return vals, nature

    def amounts_from_sqlrow(self, row, vals, reset_mode=None,
                            evaluate_mode=None, add_mode=None):
        if reset_mode:
            for nm in AMOUNT_NAMES:
                vals[nm] = 0.0
            vals['amount_balance'] = row[AMT_BAL]
        elif add_mode:
            for ii, nm in enumerate(AMOUNT_NAMES):
                vals[nm] += (row[ii + 5] or 0.0)
        else:
            for ii, nm in enumerate(AMOUNT_NAMES):
                vals[nm] = (row[ii + AMT_START] or 0.0)
        if evaluate_mode:
            vals['amount_balance'] = row[AMT_START] + row[
                AMT_DBT] - row[AMT_CRD]
        return vals

    def vals_from_rec(self, rec, nature, params, seq1=None):
        # Build vals dictionary from line rec
        vals = {
            'seq1': seq1 or self.seq1[nature],
            'balance_id': params['active_id'],
            'to_delete': False,
        }
        for nm in ('seq2',
                   'nature',
                   'code',
                   'name',
                   'amount_start',
                   'amount_debit',
                   'amount_credit',
                   'amount_balance',
                   'level_balance',
                   'pos_balance',
                   ):
            vals[nm] = rec[nm]
            if nm == 'name':
                vals[nm] = self.lpad_name_by_level(rec[nm],
                                                   rec['level_balance'])
        for nm in (
                'parent_code', 'group_id', 'account_id', 'partner_id',
                'parent_id'):
            if nm in rec:
                if (nm.endswith('_id') and
                        not isinstance(rec[nm], int)):
                    vals[nm] = rec[nm].id
                else:
                    vals[nm] = rec[nm]
        return vals

    def add_values_to_rec(self, rec, vals):
        if self.balance_type == 'trial':
            if self.no_opening_balances:
                vals['amount_start'] = 0.0
            else:
                vals['amount_start'] = rec.amount_start
            vals['amount_debit'] += rec.amount_debit
            vals['amount_credit'] += rec.amount_credit
            vals['amount_balance'] = (vals['amount_start'] +
                                      vals['amount_debit'] -
                                      vals['amount_credit'])
        else:
            vals['amount_balance'] += rec.amount_balance
        return vals

    @api.multi
    def has_debug_mode(self):
        # odoo 13
        if request.session.debug:
            _logger.info("debug |%s|" % request.session.debug)
            return request.session.debug
        _logger.info("debug |%s|" % request.debug)
        return request.debug

    def apply_balance_sign(self, params):
        if self.balance_type in ('ordinary', 'opposite'):
            for nature in ('P', 'R'):
                for line in self.line_model[nature].search(
                        [('balance_id', '=', params['active_id'])]):
                    line.write({'amount_balance': -line.amount_balance})

    def apply_opposite_description(self, vals):
        if vals.get('account_id'):
            account = self.env['account.account'].browse(
                vals['account_id'])
            if account.opposite_sign_code:
                vals['account_id'] = account.opposite_sign_code.id
                if account.opposite_sign_code.group_id:
                    vals['parent_id'] = account.opposite_sign_code.group_id.id
                vals['code'] = account.opposite_sign_code.code
                vals['name'] = self.lpad_name_by_level(
                    account.opposite_sign_code.name,
                    vals['level_balance'])
            elif account.opposite_sign_description:
                vals['name'] = self.lpad_name_by_level(
                    account.opposite_sign_description,
                    vals['level_balance'])
        return vals

    @api.model
    def build_sql_block(self, sql_what, params, sep=None, initial=None):
        query = ''
        for item in sorted(sql_what.keys()):
            if sql_what[item].startswith("$eval"):
                ii = sql_what[item].find('::')
                cond = sql_what[item][6:ii - 1]
                if not eval(cond, params):
                    continue
                cond = sql_what[item][ii + 2:] % params
            else:
                cond = sql_what[item] % params
            if not query:
                query = cond
            else:
                if sep:
                    query += sep
                query += cond
        if query and initial:
            query = initial + query
        return query

    def write_1_line(
            self, vals, sel=None, level_balance=None, partner_id=None,
            add_mode=None, evaluate_sign=None):

        def check_for_opposite_balance_sign(vals):
            # Check for opposite sign/nature management
            nature = vals['nature']
            if ((nature in ('A', 'C') and vals['amount_balance'] < 0.0) or
                    (nature in ('P', 'R') and vals['amount_balance'] > 0.0)):
                if vals['account_id']:
                    account = self.env['account.account'].browse(
                        vals['account_id'])
                    if self.inversion == 'force_inversion' or (
                            self.inversion == 'account_inversion' and
                            account.negative_balance in
                            ('invert_on_demand', 'invert') or
                            account.negative_balance == 'invert'
                    ):
                        nature = OPPOSITE_NATURE[nature]
                        vals['seq1'] = self.seq1[nature]
            return vals, nature

        if sel:
            line_model = self.line_model[sel]
        else:
            line_model = self.line_model[vals['nature']]
        domain = [('code', '=', vals['code']),
                  ('balance_id', '=', vals['balance_id'])]
        if level_balance:
            domain.append(('level_balance', '=', level_balance))
        if partner_id:
            domain.append(('partner_id', '=', partner_id))
        elif 'partner_id' in vals:
            domain.append(('partner_id', '=', vals['partner_id']))
        line = line_model.search(domain)
        if line:
            vals['to_delete'] = False
            if add_mode:
                vals = self.add_values_to_rec(line, vals)
            if evaluate_sign:
                vals, nature = check_for_opposite_balance_sign(vals)
                vals['nature'] = nature
            line.write(vals)
        else:
            if evaluate_sign:
                vals, nature = check_for_opposite_balance_sign(vals)
                vals['nature'] = nature
            line_model.create(vals)

    def write_lines_from_query(self, line_query, params):
        """Write balance lines.
        At this step we manage five different group of lines by nature.
        If balance type is trial we keep all the amounts. For the other
        balance types we keep just "Balance amount" amount_balance.
        """

        def init_vals_partner(row, seq, params):
            vals, nature = self.vals_from_sqlrow(row, params,
                seq2=seq, level_balance=LEVEL_BALANCE_PARTNER)
            vals = self.amounts_from_sqlrow(row, vals)
            vals['partner_id'] = row[PARTNER_ID]
            return vals

        def set_val_amounts(row, vals):
            amount_start = amount_credit = amount_debit = 0.0
            if self.balance_type == 'trial':
                amount_start = row[AMT_START]
                amount_debit = row[AMT_DBT]
                amount_credit = row[AMT_CRD]
            # BUG: sql query does not return balance amount
            amount_balance = row[AMT_START] + row[AMT_DBT] - row[AMT_CRD]
            vals['amount_start'] = amount_start
            vals['amount_debit'] = amount_debit
            vals['amount_credit'] = amount_credit
            vals['amount_balance'] = amount_balance
            self.prior_earning -= row[AMT_START]
            return vals

        def vals_rounding(self, vals):
            precision = 0
            for k in AMOUNT_NAMES:
                vals[k] = round(vals[k], precision)
            return vals

        def round_vals(vals):
            if self.rounding == 'sub_round':
                vals = self.vals_rounding(vals)
            zero_sum = not bool(sum((vals['amount_start'],
                                     vals['amount_debit'],
                                     vals['amount_credit'],
                                     vals['amount_balance'])))
            return vals, zero_sum

        customer_index = 12
        seq_by_code = {}
        self.env.cr.execute(line_query)
        for row in self.env.cr.fetchall():
            if 0 <= customer_index < len(row) and row[customer_index]:
                # check for customers/suppliers
                if row[ACC_TYPE] == 'receivable':
                    sel = 'CD'
                elif row[ACC_TYPE] == 'payable':
                    sel = 'SD'
                seq2 = self.seq2[row[SEQ2]]
                if row[CODE] in seq_by_code:
                    seq2 = seq_by_code[row[CODE]]
                vals = init_vals_partner(row, seq2 + 5, params)
                self.write_1_line(vals, sel=sel,
                    level_balance=LEVEL_BALANCE_PARTNER, evaluate_sign=True)
                if self.view_partner_details == 'in_balance':
                    vals, nature = self.vals_from_sqlrow(row, params,
                        nature=vals['nature'],
                        seq2=seq2 + 5,
                        level_balance=LEVEL_BALANCE_PARTNER)
                    vals = self.amounts_from_sqlrow(row, vals)
                    vals['partner_id'] = row[PARTNER_ID]
                    self.write_1_line(vals, sel=nature)
            else:
                # nature from account.nature
                vals, nature = self.vals_from_sqlrow(row, params)
                # store credit & debit account sequence
                if row[CODE] not in seq_by_code:
                    seq_by_code[row[CODE]] = vals['seq2']
                vals = set_val_amounts(row, vals)
                self.write_1_line(vals, sel=nature, evaluate_sign=True)

    def evaluate_parent_lines(self, params):
        """Evaluate upper level of balance
        Line sign is real sign if trial balance otherwise
        libability & income accounts have inverted sign
        account              real sign    trial balance   other balance
        asset / negative      +1 / -1         +1 / -1         1 / -1
        liability / negative  -1 / +1         -1 / +1         1 / -1
        income / negative     -1 / +1         -1 / +1         1 / -1
        expense / negative    +1 / -1         +1 / -1         1 / -1
        """

        def sum_nature(parents, nature, row):
            parents[nature] = self.amounts_from_sqlrow(
                row, parents[nature], add_mode=True)
            if nature == 'A':
                self.loss_profit_a -= row[AMT_BAL]
                self.lp_asset -= row[AMT_BAL]
            elif nature == 'P':
                if self.balance_type in ('ordinary', 'opposite'):
                    self.loss_profit_a += row[AMT_BAL]
                else:
                    self.loss_profit_a -= row[AMT_BAL]
            elif nature == 'R':
                if self.balance_type in ('ordinary', 'opposite'):
                    self.loss_profit += row[AMT_BAL]
                else:
                    self.loss_profit -= row[AMT_BAL]
            elif nature == 'C':
                self.loss_profit -= row[AMT_BAL]
                self.lp_expense -= row[AMT_BAL]
            for ii, nm in enumerate((
                    'grand_total_start',
                    'grand_total_debit',
                    'grand_total_credit',
                    'grand_total_balance')):
                setattr(self, nm,
                    getattr(self, nm) + (row[ii + AMT_START] or 0.0))
            return parents

        def sum_amounts(parents, parent_id, row,
                        nature=None, sub=None, level=None):
            level = level or (LEVEL_BALANCE_LINE - 1)
            group_model = self.env['account.group']
            if parent_id:
                level -= 1
                group = group_model.browse(parent_id)
                sub = sub or 0
                sub += 2
                if parent_id in parents:
                    parents[parent_id] = self.amounts_from_sqlrow(
                        row, parents[parent_id], add_mode=True)
                    parents[parent_id]['level_balance'] = level
                    parents[parent_id]['pos_balance'] = 'I'
                else:
                    parents[parent_id] = {
                        'code': group.code_prefix,
                        'name': group.name,
                        'nature': nature or group.nature,
                        'parent_id': group.parent_id.id,
                        # 'account_id': parent_id,
                        'account_id': row[ACCOUNT_ID],
                        'seq2': row[SEQ2] - sub,
                        'level_balance': level,
                        'pos_balance': 'I',
                    }
                    parents[parent_id] = self.amounts_from_sqlrow(
                        row, parents[parent_id])
                if not parents[parent_id]['parent_id']:
                    parents[parent_id]['level_balance'] = 1
                    parents[parent_id]['pos_balance'] = 'H'
                if parents[parent_id]['parent_id']:
                    return sum_amounts(
                        parents, parents[parent_id]['parent_id'], row,
                        nature=nature, sub=sub, level=level)
            return parents

        def build_query(params):
            query = self.build_sql_block(
                {
                    "0": "l.seq2",
                    "1": "l.code",
                    "2": "l.name",
                    "3": "a.group_id",
                    "4": "l.account_id",
                    "5": "COALESCE(l.amount_start, 0.0) AS amount_start",
                    "6": "l.amount_debit",
                    "7": "l.amount_credit",
                    "8": "l.amount_balance",
                    "9": "l.level_balance",
                },
                params,
                sep=',', initial='SELECT ')
            query += self.build_sql_block(
                {
                    '0': '%s l' % self.line_table[nature],
                },
                params,
                sep=',', initial=' FROM ')
            query += self.build_sql_block(
                {
                    '1': 'account_account a',
                },
                params,
                sep=',', initial=' LEFT JOIN ')
            query += self.build_sql_block(
                {
                    '0': 'l.account_id=a.id',
                },
                params,
                sep=' AND ', initial=' ON ')
            query += self.build_sql_block(
                {
                    '09': 'balance_id=%(active_id)s',
                    '10': 'level_balance <> %s' % LEVEL_BALANCE_PARTNER
                },
                params,
                sep=' AND ', initial=' WHERE ')
            query += self.build_sql_block(
                {
                    "0": "l.seq2",
                    "1": "l.code",
                },
                params,
                sep=',', initial=' ORDER BY ')
            return query

        def init_parents_with_nature(nature):
            return {
                nature: {
                    'amount_start': 0.0,
                    'amount_debit': 0.0,
                    'amount_credit': 0.0,
                    'amount_balance': 0.0,
                    'code': '%d' % self.seq1[nature],
                    'name': NATURE_NAMES[nature],
                    'nature': nature,
                    'parent_id': False,
                    'seq1': self.seq1[nature],
                    'seq2': 1,
                    'level_balance': 0,
                    'pos_balance': 'E',
                }
            }

        # Recurse to evaluate parent values
        for nature in self.order_by:
            parents = init_parents_with_nature(nature)
            query = build_query(params)
            self.env.cr.execute(query)
            for row in self.env.cr.fetchall():
                if row[PARENT_ID]:
                    parents = sum_amounts(
                        parents, row[PARENT_ID], row,
                        nature=nature, level=row[LEV_BALANCE])
                parents = sum_nature(parents, nature, row)

            if self.no_nature_total:
                for nature in ID_2_NATURE:
                    if nature in parents.keys():
                        del parents[nature]

            for parent_id in parents.keys():
                vals = self.vals_from_rec(
                    parents[parent_id], nature, params)
                if vals.get('account_id'):
                    account = self.env['account.account'].browse(
                        vals['account_id'])
                    if (account.nature != nature and
                            self.inversion == 'force_inversion' or (
                                    self.inversion == 'account_inversion' and
                                    account.negative_balance in
                                    ('invert_on_demand', 'invert'))
                    ):
                        vals = self.apply_opposite_description(vals)
                self.write_1_line(vals)

    def write_L_n_P(self, params, sel=None):
        """
        Line codes are the code of account/group record.
        Supplemental line like L&P or "Earning" etc must have a code as follow:
        '^': prior year loss/profit
        '-': current year loss/profit
        '#': asset/liability balance line
        '0': L&P
        '*': revenue/cost balance line
        ' ': footer grand total line
        '!': fiscal L&P
        """
        if self.prior_earning > 0:
            vals = {
                'nature': 'P',
                'seq1': 2,
                'seq2': SEQ2_LAST - 4,
                'code': '^',
                'name': '* PERDITA DA ESERCIZIO PRECEDENTE *',
                'balance_id': params['active_id'],
                'to_delete': False,
                'amount_start': 0.0,
                'amount_debit': 0.0,
                'amount_credit': 0.0,
                'level_balance': '0',
                'pos_balance': 'E',
            }
            if self.balance_type in ('ordinary', 'opposite'):
                vals['amount_balance'] = -self.prior_earning
            else:
                vals['amount_balance'] = self.prior_earning
                self.write_1_line(vals, sel=sel)
            self.write_1_line(vals, sel=sel)
            self.loss_profit_a -= self.prior_earning
        elif self.prior_earning < 0:
            vals = {
                'nature': 'P',
                'seq1': 2,
                'seq2': SEQ2_LAST - 4,
                'code': '^',
                'name': '* UTILE DA ESERCIZIO PRECEDENTE *',
                'balance_id': params['active_id'],
                'to_delete': False,
                'amount_start': 0.0,
                'amount_debit': 0.0,
                'amount_credit': 0.0,
                'level_balance': '0',
                'pos_balance': 'E',
            }
            if self.balance_type in ('ordinary', 'opposite'):
                vals['amount_balance'] = -self.prior_earning
            else:
                vals['amount_balance'] = self.prior_earning
            self.write_1_line(vals, sel=sel)
            self.loss_profit_a -= self.prior_earning
        if self.loss_profit_a > 0:
            vals = {
                'nature': 'P',
                'seq1': 2,
                'seq2': SEQ2_LAST - 3,
                'code': '-',
                'name': '* PERDITA LORDA DA RILEVARE *',
                'balance_id': params['active_id'],
                'to_delete': False,
                'amount_start': 0.0,
                'amount_debit': 0.0,
                'amount_credit': 0.0,
                'level_balance': '0',
                'pos_balance': 'E',
            }
            if self.balance_type in ('ordinary', 'opposite'):
                vals['amount_balance'] = -self.loss_profit_a
            else:
                vals['amount_balance'] = self.loss_profit_a
        elif self.loss_profit_a < 0:
            vals = {
                'nature': 'P',
                'seq1': 2,
                'seq2': SEQ2_LAST - 3,
                'code': '-',
                'name': '* UTILE LORDO PREIMPOSTE *',
                'balance_id': params['active_id'],
                'to_delete': False,
                'amount_start': 0.0,
                'amount_debit': 0.0,
                'amount_credit': 0.0,
                'level_balance': '0',
                'pos_balance': 'E',
            }
            if self.balance_type in ('ordinary', 'opposite'):
                vals['amount_balance'] = -self.loss_profit_a
            else:
                vals['amount_balance'] = self.loss_profit_a
        else:
            vals = {
                'nature': 'P',
                'seq1': 2,
                'seq2': SEQ2_LAST - 3,
                'code': '-',
                'name': 'BILANCIO A PAREGGIO',
                'balance_id': params['active_id'],
                'to_delete': False,
                'amount_start': 0.0,
                'amount_debit': 0.0,
                'amount_credit': 0.0,
                'amount_balance': 0.0,
                'level_balance': '0',
                'pos_balance': 'E',
            }
        self.write_1_line(vals, sel=sel)

        if self.loss_profit_a:
            vals = {
                'nature': 'P',
                'seq1': 2,
                'seq2': SEQ2_LAST - 1,
                'code': '#',
                'name': '* TOTALE A PAREGGIO *',
                'balance_id': params['active_id'],
                'to_delete': False,
                'amount_start': 0.0,
                'amount_debit': 0.0,
                'amount_credit': 0.0,
                'level_balance': '0',
                'pos_balance': 'E',
            }
            if self.loss_profit_a < 0:
                vals['amount_balance'] = -self.lp_asset
            else:
                vals['amount_balance'] = self.lp_asset
            self.write_1_line(vals, sel=sel)

        nature_LP = 'R' if self.seq1['R'] > self.seq1['C'] else 'C'
        if self.loss_profit < 0:
            vals = {
                'nature': nature_LP,
                'seq1': self.seq1[nature_LP],
                'seq2': SEQ2_LAST - 3,
                'code': '0',
                'name': '* PERDITA DI ESERCIZIO *',
                'balance_id': params['active_id'],
                'to_delete': False,
                'amount_start': 0.0,
                'amount_debit': 0.0,
                'amount_credit': 0.0,
                'level_balance': '0',
                'pos_balance': 'E',
            }
            if ((self.balance_type in ('ordinary', 'opposite') and
                 nature_LP == 'R') or
                    (self.balance_type not in ('ordinary', 'opposite') and
                     nature_LP == 'C')):
                vals['amount_balance'] = -self.loss_profit
            else:
                vals['amount_balance'] = self.loss_profit
        elif self.loss_profit > 0:
            vals = {
                'nature': nature_LP,
                'seq1': self.seq1[nature_LP],
                'seq2': SEQ2_LAST - 3,
                'code': '0',
                'name': '* PROFITTI ANTE IMPOSTE *',
                'balance_id': params['active_id'],
                'to_delete': False,
                'amount_start': 0.0,
                'amount_debit': 0.0,
                'amount_credit': 0.0,
                'level_balance': '0',
                'pos_balance': 'E',
            }
            if ((self.balance_type in ('ordinary', 'opposite') and
                 nature_LP == 'R') or
                    (self.balance_type not in ('ordinary', 'opposite') and
                     nature_LP == 'C')):
                vals['amount_balance'] = -self.loss_profit
            else:
                vals['amount_balance'] = self.loss_profit
        else:
            vals = {
                'nature': nature_LP,
                'seq1': self.seq1[nature_LP],
                'seq2': SEQ2_LAST - 3,
                'code': '0',
                'name': 'PROFITTI & PERDITE',
                'balance_id': params['active_id'],
                'to_delete': False,
                'amount_start': 0.0,
                'amount_debit': 0.0,
                'amount_credit': 0.0,
                'amount_balance': 0.0,
                'level_balance': '0',
                'pos_balance': 'E',
            }
        self.write_1_line(vals, sel=sel)

        if self.loss_profit:
            vals = {
                'nature': nature_LP,
                'seq1': self.seq1[nature_LP],
                'seq2': SEQ2_LAST - 1,
                'code': '*',
                'name': '* TOTALE A PAREGGIO *',
                'balance_id': params['active_id'],
                'to_delete': False,
                'amount_start': 0.0,
                'amount_debit': 0.0,
                'amount_credit': 0.0,
                'amount_balance': 0.0,
                'level_balance': '0',
                'pos_balance': 'E',
            }
            if ((self.balance_type in ('ordinary', 'opposite') and
                 nature_LP == 'R') or
                    (self.balance_type not in ('ordinary', 'opposite') and
                     nature_LP == 'C')):
                vals['amount_balance'] = self.lp_expense - self.loss_profit
            else:
                vals['amount_balance'] = -(self.lp_expense - self.loss_profit)
            self.write_1_line(vals, sel=sel)

    def write_gran_totals(self, params, sel=None):
        vals = {
            'seq1': 9,
            'seq2': SEQ2_GT,
            'code': ' ',
            'name': 'GRAN TOTALE',
            'balance_id': params['active_id'],
            'to_delete': False,
            'amount_start': self.grand_total_start,
            'amount_debit': self.grand_total_debit,
            'amount_credit': self.grand_total_credit,
            'amount_balance': self.grand_total_balance,
            'level_balance': '9',
            'pos_balance': 'T',
        }
        self.write_1_line(vals, sel=sel)

    def write_depreciations(self, params):
        return True

    def merge_lines(self, params):
        """Finally we merge the 5 group of balance lines into balance sheet"""
        nature_list = list(self.order_by)
        if self.select_details in ('customers_suppliers', 'only_customers',
                                   'only_suppliers'):
            nature_list += ['CD', 'SD']

        if self.balance_type == 'trial':
            balance_line_model = self.env['italy.account.balance.line']
        else:
            balance_line_model = self.env['italy.account.balance.line2']

        for cur_nature in nature_list:
            domain = [('balance_id', '=', params['active_id'])]
            if cur_nature in ['CD', 'SD']:
                domain.append(('level_balance', '=', LEVEL_BALANCE_PARTNER))
            else:
                domain.append(('level_balance', '!=', LEVEL_BALANCE_PARTNER))
            for cur_line in self.line_model[cur_nature].search(domain):
                cur_domain = [('code', '=', cur_line.code),
                     ('balance_id', '=', params['active_id'])]
                if cur_nature in ['CD', 'SD']:
                    cur_domain.extend([('level_balance', '=',
                                        LEVEL_BALANCE_PARTNER),
                                      ('partner_id', '=', cur_line.partner_id.id)])
                else:
                    cur_domain.append(('level_balance',
                                       '!=', LEVEL_BALANCE_PARTNER))

                if cur_nature in ['CD', 'SD'] and self.view_partner_details != \
                        'in_balance':
                    continue
                line = balance_line_model.search(cur_domain)
                if len(line) > 1:
                    line[1:].unlink()
                    line = line[0]

                if cur_nature in ['CD', 'SD']:
                    line_nature = self.env['account.account'].search([
                        ('code', '=', cur_line.code)]).nature or ''
                    vals = self.vals_from_rec(cur_line, line_nature, params,
                        seq1=cur_line['seq1'])
                else:
                    vals = self.vals_from_rec(cur_line, cur_nature, params,
                        seq1=cur_line['seq1'])
                if 'partner_id' not in vals and cur_line['partner_id']:
                    vals['partner_id'] = cur_line['partner_id'].id
                if line:
                    vals['to_delete'] = False
                    line.write(vals)
                else:
                    balance_line_model.create(vals)

    def init_lines(self, params):
        """Initialize balance lines values and mark them as to delete"""
        nature_list = list(ID_2_NATURE.keys()) + ['1', '2']
        if self.select_details in ('customers_suppliers',
                                   'only_customers',
                                   'only_suppliers'):
            nature_list += ['CD', 'SD']
        for nature in nature_list:
            query = self.build_sql_block(
                {'1': self.line_table[nature]},
                params,
                initial='UPDATE ')
            if nature == '2':
                query += self.build_sql_block(
                    {
                        '1': 'to_delete=true',
                        '2': 'amount_balance=0.0',
                    },
                    params,
                    sep=',',
                    initial=' SET ')
            else:
                query += self.build_sql_block(
                    {
                        '1': 'to_delete=true',
                        '2': 'amount_start=0.0',
                        '3': 'amount_credit=0.0',
                        '4': 'amount_debit=0.0',
                        '5': 'amount_balance=0.0',
                    },
                    params,
                    sep=',',
                    initial=' SET ')
            query += self.build_sql_block(
                {'1': 'balance_id=%(active_id)s'},
                params,
                initial=' WHERE ')
            self.env.cr.execute(query)
            # Delete dirty records
            if nature in ID_2_NATURE:
                query = self.build_sql_block(
                    {'1': self.line_table[nature]},
                    params,
                    initial='DELETE FROM ')
                query += self.build_sql_block(
                    {
                        '1': 'balance_id=%(active_id)s',
                        '2': 'seq1<>%d' % self.seq1[nature],
                    },
                    params,
                    sep=' AND ',
                    initial=' WHERE ')
                self.env.cr.execute(query)

    def init_lines_accrual(self, params):
        """Initialize accrual lines values and mark them as to delete"""
        query = self.build_sql_block(
            {'1': 'italy_account_balance_line_accrual'},
            params,
            initial='UPDATE ')
        query += self.build_sql_block(
            {
                '1': 'to_delete=true',
                '2': 'previous_year_amount=0.0',
                '3': 'current_year_amount=0.0',
                '4': 'next_year_amount=0.0',
            },
            params,
            sep=',',
            initial=' SET ')
        query += self.build_sql_block(
            {
                '1': 'balance_id=%(active_id)s',
            },
            params,
            initial=' WHERE ')
        self.env.cr.execute(query)

    def purge_lines(self, params, sel=None):
        if sel:
            if isinstance(sel, (list, tuple)):
                selection = sel
            else:
                selection = [sel]
        else:
            selection = list(ID_2_NATURE.keys())
        for nature in selection:
            query = self.build_sql_block(
                {'1': self.line_table[nature]},
                params,
                initial='DELETE FROM ')
            query += self.build_sql_block(
                {'1': 'balance_id=%(active_id)s', '2': 'to_delete=true'},
                params,
                sep=' AND ',
                initial=' WHERE ')
            self.env.cr.execute(query)

    def purge_lines_accrual(self, params):
        query = self.build_sql_block(
            {'1': 'italy_account_balance_line_accrual'},
            params,
            initial='DELETE FROM ')
        query += self.build_sql_block(
            {'1': 'balance_id=%(active_id)s', '2': 'to_delete=true'},
            params,
            sep=' AND ',
            initial=' WHERE ')
        self.env.cr.execute(query)

    def purge_by_line_level(self, params):
        """
        only purge lines by level
        """
        selection = list(ID_2_NATURE.keys()) + ['1', '2']
        if self.hierarchy_level and self.hierarchy_level != '0':
            where_and_conditions = {
                '1': 'balance_id=%(active_id)s',
                '2': {
                    '1': "pos_balance NOT IN ('E', 'H')",
                    '2': "pos_balance NOT IN ('E', 'H', 'I')",
                    '3': "pos_balance NOT IN ('I', 'L')",
                    '4': "pos_balance <> 'L'",
                }[self.hierarchy_level],
            }
            for nature in selection:
                query = self.build_sql_block(
                    {'1': self.line_table[nature]},
                    params,
                    initial='DELETE FROM ')
                query += self.build_sql_block(
                    where_and_conditions,
                    params,
                    sep=' AND ',
                    initial=' WHERE ')
                self.env.cr.execute(query)

    def purge_by_zero_subaccount(self, params):
        """
        execute the delete query only if flag is True
        purge lines with level_balance = 3 and
        amount_balance = 0
        """
        self.hide_account_at_0 = 'no_zero'
        if self.hide_account_at_0 != 'all':
            selection = list(ID_2_NATURE.keys()) + ['1', '2']
            where_and_conditions = {
                '1': 'balance_id=%(active_id)s',
                '2': 'level_balance=%s' % LEVEL_BALANCE_LINE,
                '3': 'amount_balance=0',
            }
            if self.hide_account_at_0 == 'only_posted':
                where_and_conditions['4'] = 'amount_debit = 0'
                where_and_conditions['5'] = 'amount_credit = 0'
                where_and_conditions['5'] = 'amount_start = 0'
            for nature in selection:
                query = self.build_sql_block(
                    {'1': self.line_table[nature]},
                    params,
                    initial='DELETE FROM ')
                query += self.build_sql_block(
                    where_and_conditions,
                    params,
                    sep=' AND ',
                    initial=' WHERE ')
                self.env.cr.execute(query)

    def purge_partner_balance_line(self, params):
        query = self.build_sql_block(
            {'1': 'italy_account_balance_line_partner_details'},
            params,
            initial='DELETE FROM ')
        query += self.build_sql_block(
            {
                '1': 'balance_id=%(active_id)s',
                '2': 'level_balance=%s' % LEVEL_BALANCE_PARTNER,
                '3': 'to_delete=true',
            },
            params,
            sep=' AND ',
            initial=' WHERE ')
        self.env.cr.execute(query)

    def purge_partner_balance(self, params):
        if self.balance_type == 'trial':
            balance_line_name = 'italy_account_balance_line'
        else:
            balance_line_name = 'italy_account_balance_line2'
        query = self.build_sql_block(
            {'1': balance_line_name},
            params,
            initial='DELETE FROM ')
        query += self.build_sql_block(
            {
                '1': 'balance_id=%(active_id)s',
                '2': 'level_balance=%s' % LEVEL_BALANCE_PARTNER,
                '3': 'to_delete=true',
            },
            params,
            sep=' AND ',
            initial=' WHERE ')
        self.env.cr.execute(query)

    def build_main_query(self, params):
        """Build SQL statement: "SELECT what FROM from WHERE domain group"
        We build the blocks <what> <from> and <domain> base on selection.
        We have to build data for 3 different years: the previous year,
        the current year and the next year we have to join 3 queries.
        """
        # -----------------------------------------------------------------
        # BLOCK 0: block common to all years
        # Clause SELECT what
        if not self.no_opening_balances:
            sql_what = {
                "00": "COALESCE(c.nature,p.nature) AS nature",
                "01": "COALESCE(c.code,p.code) AS code",
                "02": "COALESCE(c.name,p.name) AS name",
                "03": "COALESCE(c.group_id,p.group_id) AS group_id",
                "04": "COALESCE(c.account_id,p.account_id) AS account_id",
                "05": "COALESCE(p.amount_start, 0.0) AS amount_start",
                "06": "COALESCE(c.amount_debit, 0.0) AS amount_debit",
                "07": "COALESCE(c.amount_credit, 0.0) AS amount_credit",
                "08": "COALESCE(p.amount_start, 0.0)+"
                      "COALESCE(c.amount_credit, 0.0)-"
                      "COALESCE(c.amount_credit, 0.0) AS amount_balance",
            }
        else:
            sql_what = {
                "00": "c.nature AS nature",
                "01": "c.code AS code",
                "02": "c.name AS name",
                "03": "c.group_id AS group_id",
                "04": "c.account_id AS account_id",
                "05": "0.0 AS amount_start",
                "06": "c.amount_debit AS amount_debit",
                "07": "c.amount_credit AS amount_credit",
                "08": "c.amount_credit-"
                      "c.amount_credit AS amount_balance",
            }
        if self.select_details in ('customers_suppliers', 'only_customers',
                                   'only_suppliers'):
            sql_what.update({
                "09": "'' as vat",
                "10": "'' as partner",
                "11": "'' as type",
                "12": "0 as partner_id",
            })
        # Clause ... FROM tables
        sql_from = {
            "a": "account_account a",
            # "g": "account_group g",
            "m": "account_move m",
            "t": "account_account_type t",
            "l": "account_move_line l",
        }

        # Clause ... WHERE conditions
        sql_domain = {
            "1": "a.user_type_id = t.id",
            # "2": "a.group_id = g.id",
            "3": "l.account_id = a.id",
            "4": "l.move_id = m.id",
            "9": "$eval(target_move!='all')::m.state = '%(target_move)s'",
        }

        if self.move_ids and self.has_debug_mode():
            if self.no_selected_moves:
                sql_domain['A'] = (
                        "m.id not in %s" % [x.id for x in self.move_ids]
                ).replace('[', '(').replace(']', ')')
            else:
                sql_domain['A'] = ("m.id in %s" % [x.id for x in self.move_ids]
                                   ).replace('[', '(').replace(']', ')')

        # Clause GROUP BY
        if not self.no_opening_balances:
            sql_group = {
                "00": "COALESCE(c.nature,p.nature)",
                "01": "COALESCE(c.code,p.code)",
                "02": "COALESCE(c.name,p.name)",
                "03": "COALESCE(c.group_id,p.group_id)",
                "04": "COALESCE(c.account_id,p.account_id)",
                "05": "p.amount_start",
                "06": "c.amount_debit",
                "07": "c.amount_credit",
            }
            sql_order = {
                "00": "COALESCE(c.nature,p.nature)",
                "01": "COALESCE(c.code,p.code)"
            }
        else:
            sql_group = {
                "00": "nature",
                "01": "code",
                "02": "name",
                "03": "group_id",
                "04": "account_id",
                "05": "amount_start",
                "06": "amount_debit",
                "07": "amount_credit",
            }
        sql_order = {
            "00": "nature",
            "01": "code"
        }

        # -----------------------------------------------------------------
        # BLOCK 1: previous year
        # Clause SELECT what
        sql_what_prior = {
            "00": "t.nature AS nature",
            "01": "a.code AS code",
            "02": "a.name AS name",
            "03": "a.group_id AS group_id",
            "04": "l.account_id AS account_id",
            "05": "COALESCE(SUM(l.debit)-SUM(l.credit), 0.0) AS amount_start",
            "06": "0.0 AS amount_debit",
            "07": "0.0 AS amount_credit",
        }
        # Clause ... WHERE conditions
        if self.date_balance_option == 'competence_date':
            sql_domain_prior = {
                "1": "t.nature not in ('C', 'R')",
                "2": "COALESCE(%(m.date_apply_balance)s, %(m.date)s) < '%(date_from)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }
        elif self.date_balance_option == 'vat_date':
            sql_domain_prior = {
                "1": "t.nature not in ('C', 'R')",
                "2": "COALESCE(%(m.date_apply_vat)s, %(m.date)s) < '%(date_from)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }
        else:
            sql_domain_prior = {
                "1": "t.nature not in ('C', 'R')",
                "2": "%(m.date)s < '%(date_from)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }
        # Clause GROUP BY
        sql_group_prior = {
            "0": "t.nature",
            "1": "a.code",
            "2": "a.name",
            "3": "a.group_id",
            "4": "l.account_id",
        }
        # -----------------------------------------------------------------
        # BLOCK 2: current year
        # Clause SELECT what
        sql_what_cur = {
            "00": "t.nature AS nature",
            "01": "a.code AS code",
            "02": "a.name AS name",
            "03": "a.group_id AS group_id",
            "04": "l.account_id AS account_id",
            "05": "0.0 AS amount_start",
            "06": "SUM(l.debit) AS amount_debit",
            "07": "SUM(l.credit) AS amount_credit",
        }

        # Clause ... WHERE conditions
        if self.date_balance_option == 'competence_date':
            sql_domain_cur = {
                "1": "COALESCE(%(m.date_apply_balance)s, %(m.date)s) >= '%(date_from)s'",
                "2": "COALESCE(%(m.date_apply_balance)s, %(m.date)s) <= '%(date_to)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }
        elif self.date_balance_option == 'vat_date':
            sql_domain_cur = {
                "1": "COALESCE(%(m.date_apply_vat)s, %(m.date)s) >= '%(date_from)s'",
                "2": "COALESCE(%(m.date_apply_vat)s, %(m.date)s) <= '%(date_to)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }
        else:
            sql_domain_cur = {
                "1": "%(m.date)s >= '%(date_from)s'",
                "2": "%(m.date)s <= '%(date_to)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }

        nature_transcoding = {
            'balance_sheets_only': "('A','P')",
            'economic_accounts_only': "('C','R')",
            'memorandum_accounts': "('O')"
        }
        if (self.nature_of_accounts and
                self.nature_of_accounts in nature_transcoding.keys()):
            sql_domain_cur["5"] = "t.nature IN %s" % (
                nature_transcoding[self.nature_of_accounts])
        # Clause GROUP BY
        sql_group_cur = {
            "0": "t.nature",
            "1": "a.code",
            "2": "a.name",
            "3": "a.group_id",
            "4": "l.account_id",
        }

        # Query previous year
        prior_query = self.build_sql_block(sql_what_prior, params,
                                           sep=',', initial='SELECT ')
        prior_query += self.build_sql_block(sql_from, params,
                                            sep=',', initial=' FROM ')
        prior_query += self.build_sql_block(sql_domain, params,
                                            sep=' AND ', initial=' WHERE ')
        prior_query += self.build_sql_block(sql_domain_prior, params,
                                            sep=' AND ', initial=' AND ')
        prior_query += self.build_sql_block(sql_group_prior, params,
                                            sep=',', initial=' GROUP BY ')
        # Query current year
        cur_query = self.build_sql_block(sql_what_cur, params,
                                         sep=',', initial='SELECT ')
        cur_query += self.build_sql_block(sql_from, params,
                                          sep=',', initial=' FROM ')
        cur_query += self.build_sql_block(sql_domain, params,
                                          sep=' AND ', initial=' WHERE ')
        cur_query += self.build_sql_block(sql_domain_cur, params,
                                          sep=' AND ', initial=' AND ')
        cur_query += self.build_sql_block(sql_group_cur, params,
                                          sep=',', initial=' GROUP BY ')
        # Join previous and current year queries
        # FIX: to test
        query = ''
        if self.select_details in ('customers_suppliers',
                                   'only_customers',
                                   'only_suppliers'):
            query += self.build_partner_balance_query(params)
            query += ' UNION '

        query += self.build_sql_block(sql_what, params,
                                      sep=',', initial='SELECT ')
        if not self.no_opening_balances:
            query += ' FROM (%s) p' % prior_query
            query += ' FULL JOIN (%s) c' % cur_query
            query += ' ON p.code=c.code'
        else:
            query += ' FROM (%s) c' % cur_query
        query += self.build_sql_block(sql_group, params,
                                      sep=',', initial=' GROUP BY ')

        if self.select_details in ('customers_suppliers', 'only_customers',
                                   'only_suppliers'):
            if 'code' not in sql_order.values():

                sql_order.update({
                    '02': 'code',
                    '03': 'partner_id',
                })
            else:
                sql_order.update({
                        '02': 'partner_id',
                    })

        query += self.build_sql_block(sql_order, params,
                                      sep=',', initial=' ORDER BY ')
        # if self.select_details in ('customers_suppliers', 'only_customers',
        #                            'only_suppliers'):
        #     if 'ORDER BY' not in query:
        #         query += ' ORDER BY code,partner_id '
        #     else:
        #         query += ',code,partner_id '
        return query

    @api.multi
    def write_accrual(self, params):
        """
        For every invoice with accrual dates we have to evaluate rated amounts
        into 3 parts: prior, current and next year rated amount.
        Previous year rated amount is called cut-off (italian rateo)
        Next year rated amount is called pre-payment (italian rifasconto)
        Trial balance has 4 columns: start, debit, credit and balance.
        In order to move rated amount from an year to another one we have
        reduce the balance that is equal to debit - credit.
        Because debit & credit always must be positive, we cannot reduce
        credit or debit column but we have to add amount to the opposite side.
        Example:                    start debit credit balance
            Debits from supplier        0     0    100    -100
            Expense                     0   100      0     100
        We want to reduce expense amount by 15.
            Debits from supplier        0     0    100    -100
            Expense                     0   100     15      85
            cut-off or pre-payments     0    15      0      15

        Eventually, if reduction is a cut-off we have to reply the opposite
        operations in the prior year.
            Expense                     0    15      0      15
            cut-off                     0     0     15     -15
        """

        def build_accrual_query(params):
            sql_what = {
                "00": "a.nature",
                "01": "a.code",
                "02": "a.name",
                "03": "a.group_id",
                "04": "l.account_id",
                "05": "l.debit",
                "06": "l.credit",
                "07": "l.accrual_start_date",
                "08": "l.accrual_end_date",
                "09": "m.ref",
                "10": "m.name as mname",
                "11": "m.date",
                "12": "m.fiscalyear_id",
            }
            # Clause ... FROM tables
            sql_from = {
                "a": "account_account a",
                "m": "account_move m",
                "l": "account_move_line l",
                "t": "account_account_type t",
            }
            # Clause ... WHERE conditions
            sql_domain = {
                "1": "t.nature in ('C', 'R')",
                "2": "a.user_type_id = t.id",
                "3": "l.account_id = a.id",
                "4": "l.move_id = m.id",
                "5": "l.accrual_start_date is not null",
                "6": "l.accrual_end_date is not null",
                "9": "$eval(target_move!='all')::m.state = '%(target_move)s'",
            }

            if self.move_ids and self.has_debug_mode():
                if self.no_selected_moves:
                    sql_domain['A'] = (
                            "m.id not in %s" % [x.id for x in self.move_ids]
                    ).replace('[', '(').replace(']', ')')
                else:
                    sql_domain['A'] = (
                            "m.id in %s" % [x.id for x in self.move_ids]
                    ).replace('[', '(').replace(']', ')')

            accrual_query = self.build_sql_block(sql_what, params,
                                                 sep=',', initial='SELECT ')
            accrual_query += self.build_sql_block(sql_from, params,
                                                  sep=',', initial=' FROM ')
            accrual_query += self.build_sql_block(sql_domain, params,
                                                  sep=' AND ',
                                                  initial=' WHERE ')
            return accrual_query

        def set_accrual_date(accr_env, row, params):

            def get_date_from(row, params, sel_fy):
                out_fy = ''
                accr_date_from = row[DATE_FROM]
                if (row[DATE_FROM] < params[sel_fy]['date_from'] and
                        sel_fy == 'cur_fy') or sel_fy == 'prior_fy':
                    # anno precedente (rateo)
                    out_fy = '<'
                    accr_date_from = max(params['prior_fy']['date_from'],
                                         row[DATE_FROM])
                elif (row[DATE_FROM] > params[sel_fy]['date_to'] and
                        sel_fy == 'cur_fy') or sel_fy == 'next_fy':
                    # anno successivo (risconto)
                    out_fy = '>'
                    accr_date_from = min(params['next_fy']['date_from'],
                                         row[DATE_FROM])
                return accr_date_from, out_fy

            def get_date_to(row, params, sel_fy):
                out_fy = ''
                accr_date_to = row[DATE_TO]
                if (row[DATE_TO] > params[sel_fy]['date_to'] and
                        sel_fy == 'cur_fy') or sel_fy == 'next_fy':
                    # anno successivo (risconto)
                    out_fy = '>'
                    accr_date_to = min(params['next_fy']['date_to'],
                                       row[DATE_TO])
                elif (row[DATE_TO] < params[sel_fy]['date_from'] and
                        sel_fy == 'cur_fy'):
                    # anno precedente (rateo)
                    out_fy = '<'
                    accr_date_to = max(params['prior_fy']['date_to'],
                                       row[DATE_TO])
                elif sel_fy == 'prior_fy':
                    accr_date_to = params['prior_fy']['date_to']
                return accr_date_to, out_fy

            for nm in ('accrual_type', 'accrual_type2'):
                accr_env[nm] = ''
            for nm in ('days_expired', 'days_prior', 'days_cur', 'days_next',
                       'days_accrual'):
                accr_env[nm] = 0
            # The interval contains both date from both date to
            accr_env.days_accrual = (row[DATE_TO] - row[DATE_FROM]).days + 1
            accr_date_from, from_fy = get_date_from(row, params, 'cur_fy')
            accr_date_to, to_fy = get_date_to(row, params, 'cur_fy')
            accr_env.days_cur = (min(accr_date_to, self.date_to) -
                                 max(accr_date_from, self.date_from)).days + 1
            accr_env.days_expired = 0
            if from_fy == '<' and to_fy == '>':
                # DATE_FROM < fiscal_year < DATE_TO
                if row[0] == 'C':
                    accr_env.accrual_type = 'cutoff_passive'
                    accr_env.accrual_type2 = 'prepayment_active'
                else:
                    accr_env.accrual_type = 'cutoff_active'
                    accr_env.accrual_type2 = 'prepayment_passive'
                accr_date_from, from_fy = get_date_from(row, params, 'prior_fy')
                accr_date_to, to_fy = get_date_to(row, params, 'prior_fy')
                accr_env.days_expired = (accr_date_from - row[DATE_FROM]).days
                accr_env.days_prior = (accr_date_to - accr_date_from).days + 1
                accr_env.days_next = accr_env.days_accrual - (
                        accr_env.days_cur + accr_env.days_prior)
            elif from_fy == '<' and to_fy == '<':
                # DATE_FROM <= DATE_TO < fiscal_year
                if row[0] == 'C':
                    accr_env.accrual_type = 'cutoff_active'
                else:
                    accr_env.accrual_type = 'cutoff_passive'
                accr_env.days_expired = (accr_date_from - row[DATE_FROM]).days
                accr_env.days_prior = (accr_env.days_accrual -
                                       accr_env.days_expired)
                accr_env.days_cur = 0
            elif from_fy == '<':
                # DATE_FROM < fiscal_year / DATE_TO
                if row[0] == 'C':
                    accr_env.accrual_type = 'cutoff_passive'
                else:
                    accr_env.accrual_type = 'cutoff_active'
                accr_env.days_expired = (accr_date_from - row[DATE_FROM]).days
                accr_env.days_prior = (accr_env.days_accrual -
                                       accr_env.days_cur -
                                       accr_env.days_expired)
            elif from_fy == '>':
                # fiscal_year < DATE_FROM <= DATE_TO
                if row[NATURE] == 'C':
                    accr_env.accrual_type = 'prepayment_active'
                else:
                    accr_env.accrual_type = 'prepayment_passive'
                accr_env.days_next = accr_env.days_accrual
                accr_env.days_cur = 0
            elif to_fy == '>':
                # fiscal_year / DATE_FROM < DATE_TO
                if row[NATURE] == 'C':
                    accr_env.accrual_type = 'prepayment_active'
                else:
                    accr_env.accrual_type = 'prepayment_passive'
                accr_env.days_next = accr_env.days_accrual - accr_env.days_cur
            return accr_env

        def set_accrual_values(accr_env, row):
            for nm in ('rated_debit', 'rated_credit'):
                accr_env[nm] = 0.0
            accrual_type = accr_env.accrual_type
            invoice_debit = row[5] or 0.0
            invoice_credit = row[6] or 0.0
            accr_env.amount_expired = round(
                (invoice_debit - invoice_credit) *
                accr_env.days_expired / accr_env.days_accrual, precision)
            accr_env.amount_prior = round(
                (invoice_debit - invoice_credit) *
                accr_env.days_prior / accr_env.days_accrual, precision)
            accr_env.amount_current = round(
                (invoice_debit - invoice_credit) *
                accr_env.days_cur / accr_env.days_accrual, precision)
            accr_env.amount_next = round(
                (invoice_debit - invoice_credit) -
                (accr_env.amount_prior +
                 accr_env.amount_current +
                 accr_env.amount_expired), precision)
            if (accrual_type in ('prepayment_passive', 'cutoff_active') or
                    not accrual_type and row[NATURE] == 'R'):
                accr_env.amount_expired = -accr_env.amount_expired
                accr_env.amount_prior = -accr_env.amount_prior
                accr_env.amount_next = -accr_env.amount_next
                accr_env.amount_current = -accr_env.amount_current
            if accr_env.days_cur != accr_env.days_accrual:
                accr_env.rated_debit = round(
                    invoice_debit - invoice_debit *
                    accr_env.days_cur / accr_env.days_accrual,
                    precision)
                accr_env.rated_credit = round(
                    invoice_credit - invoice_credit *
                    accr_env.days_cur / accr_env.days_accrual,
                    precision)
                accr_env[accrual_type]['amount_debit'] += accr_env.rated_debit
                accr_env[accrual_type]['amount_credit'] += accr_env.rated_credit
                accr_env[accrual_type]['amount_balance'] += (
                        accr_env.rated_debit - accr_env.rated_credit)
                # Rated amount in the opposite side (read above)
                accr_env.rated_debit, accr_env.rated_credit = \
                    accr_env.rated_credit, accr_env.rated_debit
            accr_env.rated_debit += invoice_debit
            accr_env.rated_credit += invoice_credit
            return accr_env

        def set_line_values(vals, accr_env):
            vals['amount_start'] = 0.0
            vals['amount_debit'] = accr_env.rated_debit
            vals['amount_credit'] = accr_env.rated_credit
            vals['amount_balance'] = (accr_env.rated_debit -
                                      accr_env.rated_credit)
            return vals

        def add_line_values(line, vals, accr_env):
            vals = set_line_values(vals, accr_env)
            del vals['seq2']
            if 'amount_start' in vals and not vals['amount_start']:
                vals['amount_start'] = 0.0
            if self.balance_type == 'trial':
                vals['amount_debit'] += line.amount_debit
                vals['amount_credit'] += line.amount_credit
                vals['amount_balance'] = (line.amount_start +
                                          vals['amount_debit'] -
                                          vals['amount_credit'])
            else:
                vals['amount_debit'] = vals['amount_credit'] = 0.0
                vals['amount_balance'] += line.amount_balance
            return vals

        def init_accr_vals(row, params, accr_env, accrual_type):
            accrual_vals = {
                'balance_id': params['active_id'],
                'type': accrual_type,
                'move_number': row[10],
                'move_date': row[11],
                'move_count': row[1],
                'invoiced_amount': row[6] - row[5],
                'expired_year_amount': accr_env.amount_expired,
                'previous_year_amount': accr_env.amount_prior,
                'current_year_amount': accr_env.amount_current,
                'next_year_amount': accr_env.amount_next,
                'start_date_competence': row[DATE_FROM],
                'end_date_competence': row[DATE_TO],
                'to_delete': False,
            }
            if accrual_vals['invoiced_amount'] < 0.0:
                for nm in ('expired_year_amount', 'previous_year_amount',
                           'current_year_amount', 'next_year_amount'):
                    accrual_vals[nm] = -accrual_vals[nm]
            return accrual_vals

        def create_accr_env():
            # Constructor for dynamic class Accrual
            def cls_setitem(self, key, val):
                self.__dict__[key] = val

            def cls_getitem(self, key):
                return self.__dict__[key]

            Accrual = type('Accrual class',
                           (),
                           {
                               '__setitem__': cls_setitem,
                               '__getitem__': cls_getitem
                           }
                           )

            profile_account = self.company_id.account_profile_id

            # Build cut-off/pre-payments amount matrix
            accr_env = Accrual()
            accr_env['accrual_type'] = accr_env['accrual_type2'] = ''
            for accrual_type in ('cutoff_active', 'cutoff_passive',
                                 'prepayment_active', 'prepayment_passive'):
                accr_env[accrual_type] = {}

                for amount in AMOUNT_NAMES:
                    accr_env[accrual_type][amount] = 0.0
                if (profile_account and
                        hasattr(profile_account[accrual_type], 'code')):
                    accr_env[accrual_type]['account_id'] = getattr(
                        profile_account[accrual_type], 'id')
                    for nm in ('parent_id', 'code', 'name'):
                        if nm == 'parent_id':
                            mdel = getattr(profile_account[accrual_type],
                                           'group_id')
                            accr_env[accrual_type][nm] = mdel.id
                        else:
                            accr_env[accrual_type][nm] = getattr(
                                profile_account[accrual_type], nm)
                else:
                    accr_env[accrual_type]['account_id'] = False
                    accr_env[accrual_type]['parent_id'] = False
                    for nm in ('code', 'name'):
                        accr_env[accrual_type][nm] = ACCRUAL_TYPES[
                            nm][accrual_type]
                nm = 'nature'
                accr_env[accrual_type][nm] = ACCRUAL_TYPES[nm][accrual_type]
            return accr_env

        for nature in enumerate(self.order_by):
            self.seq2[nature] = SEQ2_LAST
        accr_line_model = self.env['italy.account.balance.line.accrual']
        accr_env = create_accr_env()
        accrual_query = build_accrual_query(params)
        self.env.cr.execute(accrual_query)
        # TODO: set currency precision
        precision = 2
        for row in self.env.cr.fetchall():
            vals, nature = self.vals_from_sqlrow(row, params)
            accr_env = set_accrual_date(accr_env, row, params)
            accr_env = set_accrual_values(accr_env, row)
            accr_type = (accr_env.accrual_type if not accr_env.accrual_type2
                         else '%s+%s' % (accr_env.accrual_type,
                                         accr_env.accrual_type2))
            accrual_vals = init_accr_vals(row, params, accr_env, accr_type)

            # Row in accrual tab
            accr_line = accr_line_model.search([
                ('balance_id', '=', params['active_id']),
                ('move_number', '=', row[10]),
                ('start_date_competence', '=', row[DATE_FROM]),
                ('end_date_competence', '=', row[DATE_TO]),
                ('type', '=', accr_type),
            ])
            if accr_line:
                if accr_line[0].to_delete:
                    accrual_vals['to_delete'] = False
                else:
                    for item in ('expired_year_amount',
                                 'previous_year_amount',
                                 'current_year_amount',
                                 'next_year_amount'):
                        accrual_vals[item] += accr_line[0][item]
                accr_line[0].write(accrual_vals)
            else:
                accr_line_model.create(accrual_vals)

            # Row in balance sheet
            line = self.line_model[vals['nature']].search(
                [('code', '=', vals['code']),
                 ('balance_id', '=', params['active_id'])])
            if line:
                vals = add_line_values(line, vals, accr_env)
                line.write(vals)
            else:
                vals = set_line_values(vals, accr_env)
                self.line_model[vals['nature']].create(vals)

            # Summary of accrual account
            for accrual_type in ('cutoff_active', 'cutoff_passive',
                                 'prepayment_active', 'prepayment_passive'):
                if (accrual_type != accr_env.accrual_type and
                        accrual_type != accr_env.accrual_type2):
                    continue
                nature = accr_env[accrual_type]['nature']
                line = self.line_model[nature].search([
                    ('balance_id', '=', params['active_id']),
                    ('code', '=', accr_env[accrual_type]['code']),
                ])
                level_balance = LEVEL_BALANCE_LINE
                if accrual_type in ('cutoff_active', 'cutoff_passive'):
                    seq2 = SEQ2_LAST - 12
                else:
                    seq2 = SEQ2_LAST - 10
                vals = {
                    'seq1': self.seq1[nature],
                    'seq2': seq2,
                    'balance_id': params['active_id'],
                    'to_delete': False,
                    'level_balance': level_balance,
                }
                for nm in ('nature', 'code', 'account_id', 'parent_id'):
                    vals[nm] = accr_env[accrual_type][nm]
                if accrual_type == 'cutoff_passive':
                    vals['amount_debit'] = accr_env.amount_prior
                    vals['amount_balance'] = accr_env.amount_prior
                elif accrual_type == 'cutoff_active':
                    vals['amount_credit'] = accr_env.amount_prior
                    vals['amount_balance'] = -accr_env.amount_prior
                elif accrual_type == 'prepayment_passive':
                    vals['amount_debit'] = accr_env.amount_next
                    vals['amount_balance'] = -accr_env.amount_next
                elif accrual_type == 'prepayment_active':
                    vals['amount_credit'] = accr_env.amount_next
                    vals['amount_balance'] = accr_env.amount_next
                vals['name'] = self.lpad_name_by_level(
                    accr_env[accrual_type]['name'],
                    level_balance)
                if vals['amount_balance'] != 0.0:
                    if line:
                        vals['to_delete'] = False
                        if self.balance_type == 'trial':
                            if 'amount_debit' in vals:
                                vals['amount_debit'] += line.amount_debit
                            else:
                                vals['amount_debit'] = line.amount_debit

                            if 'amount_credit' in vals:
                                vals['amount_credit'] += line.amount_credit
                            else:
                                vals['amount_credit'] = line.amount_credit

                            vals['amount_balance'] = (line.amount_start +
                                                      vals['amount_debit'] -
                                                      vals['amount_credit'])
                        else:
                            vals['amount_debit'] = vals['amount_credit'] = 0.0
                            vals['amount_balance'] += line.amount_balance
                        line.write(vals)
                    else:
                        self.line_model[nature].create(vals)

    def build_accrual_balance_query(self, params):
        sql_what = {
            "0": "balance_id",
            "1": "type",
            "2": "SUM(previous_year_amount)",
            "3": "SUM(current_year_amount)",
            "4": "SUM(next_year_amount)",
        }
        # Clause ... FROM tables
        sql_from = {
            "0": "italy_account_balance_line_accrual",
        }
        # Clause ... WHERE conditions
        sql_domain = {
            "1": "balance_id=%(active_id)s",
        }
        sql_group = {
            "1": "balance_id",
            "2": "type",
        }

        accrual_balance_query = self.build_sql_block(
            sql_what, params, sep=',', initial='SELECT ')
        accrual_balance_query += self.build_sql_block(
            sql_from, params, sep=',', initial=' FROM ')
        accrual_balance_query += self.build_sql_block(
            sql_domain, params, sep=' AND ', initial=' WHERE ')
        accrual_balance_query += self.build_sql_block(
            sql_group, params, sep=',', initial=' GROUP BY ')
        return accrual_balance_query

    def apply_for_inversion(self, params):
        moved = False
        for cur_nature in self.order_by:
            for cur_line in self.line_model[cur_nature].search(
                    [('balance_id', '=', params['active_id']),
                     ('nature', '!=', cur_nature)]):
                domain = [('balance_id', '=', params['active_id']),
                          ('level_balance', '=', LEVEL_BALANCE_LINE),
                          ('seq2', '>', 10),
                          ('seq2', '<', SEQ2_LAST - SEQ2_INCR)]
                line = self.line_model[cur_line.nature].search(
                    domain + [('code', '>', cur_line.code)],
                    limit=1, order='seq2')
                max_seq = line[0].seq2 if len(line) else SEQ2_LAST
                line = self.line_model[cur_line.nature].search(
                    domain + [('code', '<', cur_line.code)],
                    limit=1, order='seq2 desc')
                min_seq = line[0].seq2 if len(line) else 10
                vals = self.vals_from_rec(
                    cur_line, cur_line.nature, params)
                vals['seq2'] = int((max_seq - min_seq) / 2 + min_seq)
                vals['amount_balance'] = -vals['amount_balance']
                vals = self.apply_opposite_description(vals)
                self.write_1_line(vals)
                cur_line.write({'to_delete': True})
                moved = True
        if moved:
            self.purge_lines(params)

    def build_partner_balance_query(self, params):
        # prior
        sql_what_prior = {
            "01": "t.nature AS nature",
            "02": "a.code AS code",
            "03": "a.name AS name",
            "04": "a.group_id AS group_id",
            "05": "l.account_id AS account_id",
            "06": "COALESCE(SUM(l.debit)-SUM(l.credit),0.0) AS amount_start",
            "07": "0.0 AS amount_debit",
            "08": "0.0 AS amount_credit",
            "09": "r.vat",
            "10": "r.name as partner",
            "11": "t.type",
            "12": "r.id AS partner_id",
        }
        if self.date_balance_option == 'competence_date':
            sql_domain_prior = {
                "1": "t.nature not in ('C', 'R')",
                "2": "COALESCE(%(m.date_apply_balance)s, %(m.date)s) < '%(date_from)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }
        elif self.date_balance_option == 'vat_date':
            sql_domain_prior = {
                "1": "t.nature not in ('C', 'R')",
                "2": "COALESCE(%(m.date_apply_vat)s, %(m.date)s) < '%(date_from)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }
        else:
            sql_domain_prior = {
                "1": "t.nature not in ('C', 'R')",
                "2": "%(m.date)s < '%(date_from)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }
        # current
        sql_what_cur = {
            "01": "t.nature AS nature",
            "02": "a.code AS code",
            "03": "a.name AS name",
            "04": "a.group_id AS group_id",
            "05": "l.account_id AS account_id",
            "06": "0.0 AS amount_start",
            "07": "SUM(l.debit) AS amount_debit",
            "08": "SUM(l.credit) AS amount_credit",
            "09": "r.vat",
            "10": "r.name as partner",
            "11": "t.type",
            "12": "r.id AS partner_id",
        }

        if self.date_balance_option == 'competence_date':
            sql_domain_cur = {
                "1": "COALESCE(%(m.date_apply_balance)s, %(m.date)s) >= '%(date_from)s'",
                "2": "COALESCE(%(m.date_apply_balance)s, %(m.date)s) <= '%(date_to)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }
        elif self.date_balance_option == 'vat_date':
            sql_domain_cur = {
                "1": "COALESCE(%(m.date_apply_vat)s, %(m.date)s) >= '%(date_from)s'",
                "2": "COALESCE(%(m.date_apply_vat)s, %(m.date)s) <= '%(date_to)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }
        else:
            sql_domain_cur = {
                "1": "%(m.date)s >= '%(date_from)s'",
                "2": "%(m.date)s <= '%(date_to)s'",
                "3": "$eval(evaluate_accrual)::l.accrual_start_date is null",
                "4": "$eval(evaluate_accrual)::l.accrual_end_date is null",
            }

        sql_from_prior_current = {
            "1": "account_account a",
            "2": "account_move m",
            "3": "account_account_type t",
            "4": "account_move_line l",
        }
        sql_group_prior_current = {
            "1": "t.nature",
            "2": "a.code",
            "3": "a.name",
            "4": "a.group_id",
            "5": "l.account_id",
            "6": "r.vat",
            "7": "r.id",
            "8": "t.type",
        }
        sql_left_join = {
            "1": "res_partner r",
            "2": "r.id = l.partner_id"
        }
        account_type = {
            "customers_suppliers": "('receivable', 'payable')",
            "only_customers": "('receivable')",
            "only_suppliers": "('payable')",
        }
        sql_domain = {
            "1": "a.user_type_id = t.id",
            "2": "l.account_id = a.id",
            "3": "l.move_id = m.id",
            "4": "t.type in %s" % account_type[self.select_details],
            "9": "$eval(target_move!='all')::m.state = '%(target_move)s'",
        }
        nature_transcoding = {
            'balance_sheets_only': "('A','P')",
            'economic_accounts_only': "('C','R')",
            'memorandum_accounts': "('O')"
        }
        if (self.nature_of_accounts and
                self.nature_of_accounts in nature_transcoding.keys()):
            sql_domain_prior.update({"10": "t.nature IN %s" % (
                nature_transcoding[self.nature_of_accounts])})
            sql_domain_cur.update({"10": "t.nature IN %s" % (
                nature_transcoding[self.nature_of_accounts])})

        if self.move_ids and self.has_debug_mode():
            if self.no_selected_moves:
                sql_domain['A'] = (
                        "m.id not in %s" % [x.id for x in self.move_ids]
                ).replace('[', '(').replace(']', ')')
            else:
                sql_domain['A'] = ("m.id in %s" % [x.id for x in self.move_ids]
                                   ).replace('[', '(').replace(']', ')')
        sql_what = {
            "01": "nature",
            "02": "code",
            "03": "name",
            "04": "group_id",
            "05": "account_id",
            "06": "SUM(amount_start) as amount_start",
            "07": "SUM(amount_debit) as amount_debit",
            "08": "SUM(amount_credit) as amount_credit",
            "09": "COALESCE(SUM(amount_start) + SUM(amount_debit) - "
                  "SUM(amount_credit), 0.0) as amount_balance",
            "99": "MAX(vat) as vat",
            "999": "MAX(partner) as partner",
            "9999": "type",
            "99999": "partner_id",
        }
        sql_from = {
            "1": "customers_suppliers"
        }
        sql_group = {
            "1": "nature",
            "2": "code",
            "3": "name",
            "4": "group_id",
            "5": "account_id",
            "6": "type",
            "7": "partner_id",
        }
        sql_prior = self.build_sql_block(sql_what_prior, params,
                                         sep=',', initial='SELECT ')
        sql_prior += self.build_sql_block(sql_from_prior_current, params,
                                          sep=',', initial=' FROM ')
        sql_prior += self.build_sql_block(sql_left_join, params,
                                          sep=' ON ',
                                          initial=' LEFT JOIN ')
        sql_prior += self.build_sql_block(sql_domain, params,
                                          sep=' AND ', initial=' WHERE ')
        sql_prior += self.build_sql_block(sql_domain_prior, params,
                                          sep=' AND ', initial=' AND ')
        sql_prior += self.build_sql_block(sql_group_prior_current, params,
                                          sep=',', initial=' GROUP BY ')
        sql_current = self.build_sql_block(sql_what_cur, params,
                                           sep=',', initial='SELECT ')
        sql_current += self.build_sql_block(sql_from_prior_current, params,
                                            sep=',', initial=' FROM ')
        sql_current += self.build_sql_block(sql_left_join, params,
                                            sep=' ON ',
                                            initial=' LEFT JOIN ')
        sql_current += self.build_sql_block(sql_domain, params,
                                            sep=' AND ', initial=' WHERE ')
        sql_current += self.build_sql_block(sql_domain_cur, params,
                                            sep=' AND ', initial=' AND ')
        sql_current += self.build_sql_block(sql_group_prior_current, params,
                                            sep=',', initial=' GROUP BY ')
        query = 'with customers_suppliers as ( '
        query += ' %s ' % sql_prior
        query += ' UNION '
        query += ' %s ' % sql_current
        query += ')'
        query += self.build_sql_block(sql_what, params,
                                     sep=',', initial='SELECT ')
        query += self.build_sql_block(sql_from, params,
                                      sep=',', initial=' FROM ')
        query += self.build_sql_block(sql_group, params,
                                      sep=',', initial=' GROUP BY ')
        return query

    @api.multi
    def generate_balance(self):
        active_id = self._context.get('active_id')

        def fy_prior(fy_date):
            return date(fy_date.year - 1, fy_date.month, fy_date.day)

        def fy_next(fy_date):
            return date(fy_date.year + 1, fy_date.month, fy_date.day)

        def init_env():
            self.balance_model = self.env['italy.account.balance']
            self.line_model_name = {}
            self.line_model = {}
            self.line_table = {}
            for nat in ID_2_NATURE.keys():
                self.line_model_name[
                    nat] = 'italy.account.balance.line.%s' % ID_2_NATURE[nat]
                self.line_model[nat] = self.env[self.line_model_name[nat]]
                self.line_table[nat] = self.line_model_name[nat].replace('.',
                                                                         '_')
            # Use dict to store merged line models 1 (trial) and 2 (ordinary)
            self.line_model_name['1'] = 'italy.account.balance.line'
            self.line_model['1'] = self.env[self.line_model_name['1']]
            self.line_table['1'] = self.line_model_name['1'].replace('.', '_')
            self.line_model_name['2'] = 'italy.account.balance.line2'
            self.line_model['2'] = self.env[self.line_model_name['2']]
            self.line_table['2'] = self.line_model_name['2'].replace('.', '_')
            self.line_model_name['CD'] = \
                'italy.account.balance.line.customer.detail'
            self.line_model['CD'] = self.env[self.line_model_name['CD']]
            self.line_table['CD'] = self.line_model_name['CD'].replace('.',
                                                                       '_')
            self.line_model_name['SD'] = \
                'italy.account.balance.line.supplier.detail'
            self.line_model['SD'] = self.env[self.line_model_name['SD']]
            self.line_table['SD'] = self.line_model_name['SD'].replace('.',
                                                                       '_')
            self.seq1 = {}
            self.seq2 = {}
            if self.order_by == 'code':
                self.order_by = 'APCRO'
            # ii = 0
            for nature in self.order_by:
                self.env.cr.execute('''
                select substring(code for 1),count(id) as code
                from account_account
                where company_id=%d and nature='%s'
                group by substring(code for 1) order by count(id) desc;''' % (
                    self.company_id.id, nature))
                ii = max(self.seq1.values() or [0]) + 1
                for row in self.env.cr.fetchall():
                    if row[0].isdigit():
                        ii = int(row[0])
                        break
                self.seq1[nature] = ii
                self.seq2[nature] = 0
            rev = {self.seq1[k]: k for k in self.seq1}
            avai = [ii for ii in range(10) if ii not in rev]
            ii = 1
            for k in self.seq1:
                if k not in rev.values():
                    self.seq1[k] = avai[ii]
                    ii += 1

            self.grand_total_start = self.grand_total_balance = 0.0
            self.grand_total_debit = self.grand_total_credit = 0.0
            self.loss_profit = self.loss_profit_a = 0.0
            self.lp_asset = self.lp_expense = 0.0
            self.prior_earning = 0.0
            params = {
                'm.date': 'm.date',
                'm.date_apply_balance': 'm.date_apply_balance',
                'm.date_apply_vat': 'm.date_apply_vat',
                'date_from': self.date_from,
                'date_to': self.date_to,
                'active_id': active_id,
                'target_move': self.target_move,
                'evaluate_accrual': self.evaluate_accrual,
                'fys': {}
            }
            for fy in self.env['account.fiscal.year'].search([]):
                params['fys'][fy.id] = fy
                if (fy.date_from <= self.date_to <= fy.date_to):
                    params['cur_fy'] = {
                        'date_from': fy.date_from,
                        'date_to': fy.date_to
                    }
            if 'cur_fy' not in params:
                raise UserWarning(
                    'Nessun anno fiscale per il periodo richiesto')
            for fy in params['fys'].values():
                if fy.date_to < self.date_from:
                    if ('prior_fy' not in params or
                            fy.date_to > params['prior_fy']['date_to']):
                        params['prior_fy'] = {
                            'date_from': fy.date_from,
                            'date_to': fy.date_to
                        }
                if fy.date_from > self.date_to:
                    if ('next_fy' not in params or
                            fy.date_from < params['next_fy']['date_from']):
                        params['next_fy'] = {
                            'date_from': fy.date_from,
                            'date_to': fy.date_to
                        }
            if 'prior_fy' not in params:
                params['prior_fy'] = {
                    'date_from': fy_prior(params['cur_fy']['date_from']),
                    'date_to': fy_prior(params['cur_fy']['date_to'])
                }
            if 'next_fy' not in params:
                params['next_fy'] = {
                    'date_from': fy_next(params['cur_fy']['date_from']),
                    'date_to': fy_next(params['cur_fy']['date_to'])
                }
            return params

        def check_for_accrual_profile():
            to_raise = False
            raise_messages = []
            if not self.company_id.account_profile_id.id:
                raise Warning('Attenzione! Profilo contabile non impostato.')
            else:
                profile_account = self.company_id.account_profile_id

            for prop in ACCRUAL_MESSAGES.keys():
                if profile_account[prop].id:
                    if profile_account[prop].nature != \
                            ACCRUAL_MESSAGES[prop]['nature']:
                        to_raise = True
                        raise_messages.append(
                            ACCRUAL_MESSAGES[prop]['wrong_type'])
                else:
                    to_raise = True
                    raise_messages.append(ACCRUAL_MESSAGES[prop]['empty'])
            if to_raise:
                msg = "\n- ".join(raise_messages)
                raise Warning("Attenzione: Anomalie profilo contabile\n - " +
                              msg)

        if self.evaluate_accrual:
            check_for_accrual_profile()
        params = init_env()
        self.init_lines(params)
        if self.evaluate_accrual:
            self.init_lines_accrual(params)
        query = self.build_main_query(params)
        self.write_lines_from_query(query, params)
        if self.evaluate_accrual:
            self.write_accrual(params)
            self.write_depreciations(params)

        # From now, liability & income accounts can have inverted balance sign
        # Trial balance keeps the real sign
        self.apply_balance_sign(params)
        self.purge_by_zero_subaccount(params)
        self.purge_lines(params)
        if self.evaluate_accrual:
            self.purge_lines_accrual(params)
        # Negative balance may be moved to opposite nature
        self.apply_for_inversion(params)
        self.evaluate_parent_lines(params)
        self.merge_lines(params)

        if self.balance_type != 'opposite':
            if self.no_nature_total is False:
                self.write_L_n_P(params, sel=LINE_SEL[self.balance_type])
            if not self.no_grand_total:
                self.write_gran_totals(params, sel=LINE_SEL[self.balance_type])
            self.purge_lines(params, sel=LINE_SEL[self.balance_type])
        else:
            if self.no_nature_total is False:
                self.write_L_n_P(params)
        self.purge_by_line_level(params)
        if self.select_details in ('customers_suppliers', 'only_customers',
                                   'only_suppliers'):
            self.purge_partner_balance(params)
        # self.apply_balance_sign(params)

        self.balance_model.browse(active_id).write(
            {'last_update': datetime.today()})
        return {'type': 'ir.actions.act_window_close'}
