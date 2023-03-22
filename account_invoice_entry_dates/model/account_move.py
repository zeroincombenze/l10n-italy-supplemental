# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#


from collections import defaultdict

from odoo import models, fields, api
# from odoo.exceptions import UserError
# import odoo.addons.decimal_precision as dp


# TODO: eliminazione righe "VAT brief" e "account brief"
class AccountMove(models.Model):
    _inherit = 'account.move'

    MONEY_IN = ('out_invoice', 'in_refund')
    MONEY_OUT = ('in_invoice', 'out_refund')

    journal_type = fields.Char(
        string='Journal Type', compute='_compute_journal_type')
    accountbrief_ids = fields.One2many(
        comodel_name='account.move.accountbrief',
        inverse_name='move_id',
        string='Prima nota'
    )
    vatbrief_ids = fields.One2many(
        comodel_name='account.move.vatbrief',
        inverse_name='move_id',
        string='Riepilogo IVA'
    )

    # Decimals to keep when rounding currency amounts
    precision_rel = fields.Integer(
        string='Decimal positions to use for calculations.',
        related='currency_id.decimal_places'
    )

    @api.depends('journal_id.type')
    def _compute_journal_type(self):
        for move in self:
            move.journal_type = move.journal_id.type
        # end for
    # end _compute_journal_type

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ORM METHODS OVERRIDE - begin

    @api.model
    def create(self, values):
        # Apply modifications inside DB transaction
        self = super().create(values)

        # If sale or purchase apply additional actions
        self._purchase_and_sale_extentions()

        # Return the result of the write command
        return self
    # end create

    @api.multi
    def write(self, values):
        for move in self:
            # If sale or purchase apply additional actions
            move._purchase_and_sale_extentions()
        # end for

        # Apply modifications inside DB transaction
        write_result = super().write(values)

        # Return the result of the write command
        return write_result
    # end write


    # ORM METHODS OVERRIDE - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # VALIDATION METHODS - begin

    # VALIDATION METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ACTIONS

    def action_accountbrief_update(self):
        self._accountbrief_purge()
        self._accountbrief_generate()
    # end action_accountbrief_update

    def action_vatbrief_update(self):
        self._vatbrief_purge()
        self._vatbrief_generate()
    # end action_vatbrief_update

    # ACTIONS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # PROTECTED METHODS

    @api.model
    def _purchase_and_sale_extentions(self):

        stop_write_recursion = 'stop_recursion' in self._context
        sale_or_purchase = self.type in (
            'out_invoice', 'in_invoice', 'out_refund', 'in_refund'
        )

        if sale_or_purchase and not stop_write_recursion:

            self = self.with_context(stop_recursion=True)

            # Fix amount computed by Odoo
            self._fix_amount()

            # Generazione del riassunto prima nota
            self.action_accountbrief_update()

            # Generazione del riassunto IVA
            self.action_vatbrief_update()

        # end if

    # end _purchase_and_sale_extentions

    @api.model
    def _accountbrief_generate(self):

        # TODO: unlink old lines before generation

        def get_accrual_dates(move_line):
            '''Return acrrual dates if field exists, an empty filed otherwise'''
            if hasattr(move_line, 'accrual_start_date'):
                return move_line.accrual_start_date, move_line.accrual_end_date
            else:
                return '', ''
            # end if
        # end get_accrual_dates

        def gen_key(move_line):
            '''
            Generate a string key for each line. The key is composed by
                - the account id
                - accrual start date (if the field is actually there, empty string otherwise)
                - accrual end date (if the field is actually there, empty string otherwise)
            '''
            accr_date_start, accr_date_end = get_accrual_dates(move_line)

            return '{account_id}_{accr_date_start}_{accr_date_end}'.format(
                account_id=move_line.account_id.id,
                accr_date_start=accr_date_start,
                accr_date_end=accr_date_end,
            )
        # end get_key

        # Holds lines groups
        lines_groups = defaultdict(list)

        # Holds the generated accountbrief records so the create()
        # method can be called just one time instead of calling it
        # for each individual accountbrief record.
        generated_account_briefs = list()

        # Get move lines
        # NB: All the move lines must be taken into account, not
        #     just the receivable or payable ones
        move_lines = list(self.line_ids)

        # Group lines by account and accrual dates
        for line in move_lines:
            lines_groups[gen_key(line)].append(line)
        # end for

        # Perform and store sums.
        for group in lines_groups.values():
            debit, credit = self._compute_total_debit_credit(group)

            # Get account id and accrual dates for the first record.
            # Since the record have been grouped by account id and accrual
            # dates it's certain that these fields are the same values for all
            # the records in the same group (aka list)
            account_id = group[0].account_id.id
            partner_id = group[0].partner_id and group[0].partner_id.id or False
            accrual_date_start, accrual_date_end = get_accrual_dates(group[0])

            brief_data = {
                'move_id': self.id,
                'account_id': account_id,
                'partner_id': partner_id,
                'debit': debit,
                'credit': credit,

                # If accrual dates are empty set the field to None
                # to pass NULL to the DB instead of an empty string
                # which would raise an error.
                'accrual_date_start': accrual_date_start or None,
                'accrual_date_end': accrual_date_end or None,
            }

            generated_account_briefs.append(brief_data)
        # end for

        # Create the brief lines
        self.env['account.move.accountbrief'].create(generated_account_briefs)
    # end _generate_account_brief

    @api.model
    def _vatbrief_generate(self):

        # unlink old lines before generation
        self.vatbrief_ids.unlink()

        # Holds the generated vatbrief records so the create()
        # method can be called just one time instead of calling it
        # for each individual vatbrief record.
        generated_vat_briefs = list()

        # Dictionaries to hold groups of VAT base amounts and VAT amounts.
        # Lines are grouped by tax ID, so the keys of both groups are
        # tax IDs
        vat_groups = defaultdict(list)
        vat_base_amount_groups = defaultdict(list)

        # Get VAT lines and group by tax ID
        move_lines_vat = self._get_lines_vat()
        for line in move_lines_vat:
            vat_groups[line.tax_line_id.id].append(line)
        # end for

        # Get VAT base amount lines and group by tax ID
        move_lines_base_amount = self._get_lines_vat_base_amount()
        for line in move_lines_base_amount:
            # NB: the field line.tax_ids is assured to have at least one
            #     element because self._get_lines_vat_base_amount()
            #     returns only fields with a non empty tax_ids field
            vat_base_amount_groups[line.tax_ids[0].id].append(line)
        # end for

        # Perform and store sums
        for group in vat_base_amount_groups.values():
            # For each group in move_lines_base_amount:
            # - perform totals for debit and credit
            # - lookup for a matching vat group
            # - perform totals for debit and credit for the lines in the
            #   matching vat group, if no group was found set the totals to 0
            # - create the mew VAT brief record

            # Common attributes for lines in the same group are taken from
            # the first line in the group
            tax_id = group[0].tax_line_id or group[0].tax_ids[0]

            # VAT base amount sum
            base_amount_debit, base_amount_credit = self._compute_total_debit_credit(group)

            # Full amount
            vat_debit = 0
            vat_credit = 0

            # "detraibile" amount
            vat_debit_det = 0
            vat_credit_det = 0

            # VAT sum
            if tax_id.id in vat_groups:

                # Simple tax, just sum the amounts
                vat_debit, vat_credit = self._compute_total_debit_credit(
                    vat_groups[tax_id.id]
                )

                # Fully "detraibile"
                if tax_id.account_id:
                    vat_debit_det = vat_debit
                    vat_credit_det = vat_credit
                else: # Fully "indetraibile"
                    vat_debit_det = 0
                    vat_credit_det = 0
                # end if

            elif tax_id.children_tax_ids:
                # Composite tax (a tax composed of children taxes)

                for child_tax in tax_id.children_tax_ids:

                    vat_debit_child, vat_credit_child = self._compute_total_debit_credit(
                        vat_groups[child_tax.id]
                    )

                    vat_debit = vat_debit + vat_debit_child
                    vat_credit = vat_credit + vat_credit_child

                    # If "detraibile"
                    if child_tax.account_id:
                        vat_debit_det = vat_debit_det + vat_debit_child
                        vat_credit_det = vat_credit_det + vat_credit_child
                    # end if

                # end for
            else:
                # No tax, everything is = 0
                pass
            # end if

            # Check the invoice type to determine the type of sum to be done
            if self.type in self.MONEY_IN:
                vat_total = round(vat_credit - vat_debit, self.precision_rel)
                vat_det = round(vat_credit_det - vat_debit_det, self.precision_rel)
                vat_base_amount_total = round(
                    base_amount_credit - base_amount_debit, self.precision_rel
                )
            elif self.type in self.MONEY_OUT:
                vat_total = round(vat_debit - vat_credit, self.precision_rel)
                vat_det = round(vat_debit_det - vat_credit_det, self.precision_rel)
                vat_base_amount_total = round(
                    base_amount_debit - base_amount_credit, self.precision_rel
                )
            else:
                assert False
            # end if

            # New record
            generated_vat_briefs.append(
                {
                    'move_id': self.id,
                    'tax_id': tax_id.id,
                    'vat_total': vat_total,
                    'vat_det': vat_det,
                    'base_amount_total': vat_base_amount_total,
                }
            )
        # end for

        # Create the brief lines
        self.env['account.move.vatbrief'].create(generated_vat_briefs)
    # end _vatbrief_generate

    @api.model
    def _fix_amount(self):

        # Check the type of the invoice
        money_in = self.type in self.MONEY_IN
        money_out = self.type in self.MONEY_OUT

        # Ensure this move is the move of an invoice
        # (already checked before calling _fix_amount
        # ...but better checking again)
        if money_in or money_out:

            # Totali dare (debot) e avere (credit)
            filtered_lines = self._get_lines_receivable_payable()
            debit, credit = self._compute_total_debit_credit(filtered_lines)

            if money_in:
                self.amount = debit - credit
            elif money_out:
                self.amount = credit - debit
            else:
                assert False, 'Sto generando il movimento contabile per una ' \
                              'fattura, ma non è ne una fattura cliente ne ' \
                              'una fattura fornitore ....NON E\' POSSIBILE'
            # end if

        # end if
    # end _fix_amount

    # PROTECTED METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # UTILITIES

    @api.model
    def _accountbrief_purge(self):
        self.accountbrief_ids.unlink()
    # end _accountbrief_purge

    @api.model
    def _vatbrief_purge(self):
        self.vatbrief_ids.unlink()
    # end _vatbrief_purge

    @api.model
    def _compute_total_debit_credit(self, lines_list):
        debit_total = 0
        credit_total = 0

        for line in lines_list:
            debit_total = round(debit_total + line.debit, self.precision_rel)
            credit_total = round(credit_total + line.credit, self.precision_rel)
        # end for

        return debit_total, credit_total
    # end sum_credit_debit

    @api.model
    def _get_lines_receivable_payable(self):

        lines = [
            line for line in self.line_ids
            if
            len(line.tax_ids) == 0
            and
            not line.tax_line_id
            and
            line.account_id.user_type_id.type in ('payable', 'receivable')
        ]

        return lines
    # end _get_lines_receivable_payable

    @api.model
    def _get_lines_vat(self):
        lines = [line for line in self.line_ids if line.tax_line_id]
        return lines
    # end _get_lines_vat

    @api.model
    def _get_lines_vat_base_amount(self):
        lines = [line for line in self.line_ids if line.tax_ids]
        return lines
    # end _get_lines_vat_base_amount

    # UTILITIES - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# end AccountMove
