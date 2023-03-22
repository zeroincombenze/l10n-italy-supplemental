# Copyright 2019-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import api, models, fields
# from odoo.exceptions import UserError, Warning


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = 'account.invoice'

    amount_untaxed_goods = fields.Monetary(string='Untaxed Amount Goods',
        store=True, readonly=True, compute='_compute_amount_goods', track_visibility='always')

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type', 'date')
    def _compute_amount_goods(self):
        self.amount_untaxed_goods = sum(line.price_subtotal for line in self.invoice_line_ids if line.product_id.type not in ['service'] )

    @api.model
    def compute_amount_by_tax(self, tax_id):
        amount = 0.0
        for invoice_line_id in self.invoice_line_ids:
            for invoice_line_tax_id in invoice_line_id.invoice_line_tax_ids:
                if invoice_line_tax_id == tax_id.tax_id:
                    amount += invoice_line_id.price_subtotal
        return amount

    @api.model
    def compute_taxes_by_tax(self, tax_id):
        amount = 0.0
        for invoice_line_id in self.invoice_line_ids:
            for invoice_line_tax_id in invoice_line_id.invoice_line_tax_ids:
                if invoice_line_tax_id == tax_id.tax_id:
                    amount += invoice_line_id.price_tax
        return amount


    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        """Create move lines grouped by account invoice line values
        Account lines are marked as follow:
        'RP': Receivable or Payable line
        'LP': Loss & Profit line
        'TX': Tax line
        """

        def line_pos(line):
            if line.get('tax_ids', 'False'):
                return 'LP'
            elif line.get('tax_line_id', 'False'):
                return 'TX'
            else:
                return 'RP'

        def move_items(move_lines, selection):
            """Selection may be:
            'D': Debit (Payable lines with maturity date)
            'C': Credit (Receivable lines with maturity date)
            'RP': Generic Receivable or Payable lines (w/o maturity date)
            'LP': Loss & Profit line
            '='id: Tax line
            id: Tax line
            False: every line
            """
            for hash in group_lines.copy():
                if hash not in group_lines:
                    continue
                line = group_lines[hash]
                if selection in ('D', 'C'):
                    if (((selection == 'D' and line['debit']) or
                         (selection == 'C' and line['credit'])) and
                            not line.get('tax_ids', 'False') and
                            not line.get('tax_line_id', 'False') and
                            line['account_id.*'].user_type_id.type in (
                                    'receivable', 'payable')):
                        del line['account_id.*']
                        if not move_lines:
                            move_lines = [(0, 0, line)]
                        else:
                            ii = 0
                            while ii < len(move_lines):
                                ln = move_lines[ii][2]
                                if line['date_maturity'] < ln['date_maturity']:
                                    move_lines.insert(ii, (0, 0, line))
                                    break
                                ii += 1
                            if ii >= len(move_lines):
                                move_lines.append((0, 0, line))
                        del group_lines[hash]
                elif selection == 'RP':
                    if (not line.get('tax_ids', 'False') and
                            not line.get('tax_line_id', 'False') and
                            line['account_id.*'].user_type_id.type in (
                                    'receivable', 'payable')):
                        del line['account_id.*']
                        move_lines.append((0, 0, line))
                        del group_lines[hash]
                elif selection and isinstance(selection, int):
                    if line.get('tax_line_id', 'False') == selection:
                        del line['account_id.*']
                        move_lines.append((0, 0, line))
                        del group_lines[hash]
                        break
                elif selection and selection.startswith('='):
                    if (line.get('tax_ids', 'False') and
                            selection[1:] == '%s' % line['tax_ids']):
                        del line['account_id.*']
                        move_lines.append((0, 0, line))
                        del group_lines[hash]
                elif selection == 'LP':
                    if line.get('tax_ids', 'False'):
                        tax_id = line['tax_ids'][0][1]
                        del line['account_id.*']
                        move_lines.append((0, 0, line))
                        del group_lines[hash]
                        move_lines = move_items(
                            move_lines, '=%s' % line['tax_ids'])
                        move_lines = move_items(move_lines, tax_id)
                else:
                    del line['account_id.*']
                    move_lines.append((0, 0, line))
                    del group_lines[hash]
            return move_lines

        if self.journal_id.group_inv_lines_mode != 'account':
            return move_lines
        group_lines = {}
        account_model = self.env['account.account']
        debit = 0.0
        credit = 0.0
        has_accrual_dates = False
        for cmdline in move_lines:
            line = cmdline[2]
            pos = line_pos(line)
            if pos == 'RP':
                pos = 'Dt' if line['debit'] else 'Cr',
            if (hasattr(line, 'accrual_start_date') and
                    hasattr(line, 'accrual_end_date')):
                has_accrual_dates = True
                hash = '%s-%s-%s-%s-%s-%s-%s' % (
                    pos,
                    line.get('date_maturity', ''),
                    line.get('tax_ids', ''),
                    line.get('tax_line_id', ''),
                    line['account_id'],
                    line.get('accrual_start_date', ''),
                    line.get('accrual_end_date', ''),
                )
            else:
                hash = '%s-%s-%s-%s-%s' % (
                    pos,
                    line.get('date_maturity', ''),
                    line.get('tax_ids', ''),
                    line.get('tax_line_id', ''),
                    line['account_id'],
                )
            if hash not in group_lines:
                group_lines[hash] = []
                line['account_id.*'] = account_model.browse(line['account_id'])
                if line['account_id.*'].user_type_id.type in ('receivable',
                                                              'payable'):
                    debit += line['debit']
                    credit += line['credit']
            group_lines[hash].append(line)
        for hash in group_lines:
            line = group_lines[hash][0]
            for ln2 in group_lines[hash][1:]:
                for nm in ('debit', 'credit',
                           'amount_currency', 'analytic_line_ids'):
                    line[nm] += ln2[nm]
                for nm in ('product_id', 'name'):
                    if line[nm] != ln2[nm]:
                        line[nm] = False
                line['quantity'] = 1
                if not line['name']:
                    line['name'] = line['account_id.*'].name
                if has_accrual_dates:
                    for nm in ('accrual_start_date', 'accrual_en_date'):
                        line[nm] = ln2[nm]
            bal = line['debit'] - line['credit']
            line['debit'] = bal if bal > 0 else 0.0
            line['credit'] = -bal if bal < 0 else 0.0
            group_lines[hash] = line
        move_lines = move_items([], 'D' if debit >= credit else 'C')
        move_items(move_lines, 'RP')
        move_items(move_lines, 'LP')
        move_items(move_lines, False)
        return move_lines[::-1]
