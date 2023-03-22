import logging
from odoo import models

_logger = logging.getLogger(__name__)


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def compute_totals_tax(self, ctx):

        def compute_total_child(self, domain, registry_type):

            total_base = 0.0
            total_tax = 0.0
            deductible = 0.0
            undeductible = 0.0

            for line in self.env['account.move.line'].search(domain):
                if self in line.tax_ids:
                    if registry_type == 'supplier':
                        total_base += (line.debit - line.credit)
                        _logger.info(f'{line.id} BS| {line.debit} | {line.credit}')
                    else:
                        total_base += (line.credit - line.debit)
                        _logger.info(f'{line.id} BC| {line.debit} | {line.credit}')
                        _logger.info(f' So far base {total_base}')

                elif self == line.tax_line_id:
                    if registry_type == 'supplier':
                        total_tax += (line.debit - line.credit)
                        _logger.info(f'{line.id} TS| {line.debit} | {line.credit}')
                    else:
                        total_tax += (line.credit - line.debit)
                        _logger.info(f'{line.id} TC| {line.debit} | {line.credit}')
                        _logger.info(f' so far tax {total_tax}')

            # se è una tassa secondaria devo verificare la deducibilità
            # della tassa primaria
            against_account = self._against_account()
            if against_account and against_account.id:
                if against_account.is_deductible():
                    deductible = total_tax
                    undeductible = 0.0
                else:
                    deductible = 0.0
                    undeductible = total_tax
                # end if
            # se è una tassa primaria verifico se è deducibile
            elif self.is_deductible():
                deductible = total_tax
                undeductible = 0.0
            else:
                deductible = 0.0
                undeductible = total_tax
            # end if

            return total_base, total_tax, deductible, undeductible

        domain = []
        tax_name = self._get_tax_name()
        registry_type = ctx.get('registry_type', 'customer')
        date_by = ctx.get('filter_date', 'date_apply_vat')
        state = ctx.get('state', 'posted')

        if 'from_date' in ctx:
            if date_by == 'date_apply_vat':
                domain.append('|')
                domain.append('&')
                domain.append(('date_apply_vat', '<>', False))
                domain.append(('date_apply_vat', '>=', ctx['from_date']))
                domain.append('&')
                domain.append(('date_apply_vat', '=', False))
                domain.append(('date', '>=', ctx['from_date']))
            else:
                domain.append(('date', '>=', ctx['from_date']))

        if 'to_date' in ctx:
            if date_by == 'date_apply_vat':
                domain.append('|')
                domain.append('&')
                domain.append(('date_apply_vat', '<>', False))
                domain.append(('date_apply_vat', '<=', ctx['to_date']))
                domain.append('&')
                domain.append(('date_apply_vat', '=', False))
                domain.append(('date', '<=', ctx['to_date']))
            else:
                domain.append(('date', '<=', ctx['to_date']))

        domain.append(('journal_id.type', '=', self.type_tax_use))

        journal = self.env['account.journal']
        # if hasattr(journal, 'comunicazione_dati_iva_escludi'):
        #     domain.append(
        #         ('journal_id.comunicazione_dati_iva_escludi', '=', False))

        header_domain = [x for x in domain]
        header_domain.append(('state', '=', state))

        if 'registry_ids' in ctx:
            header_domain.append(('journal_id', 'in', ctx['registry_ids']))
        # end if
        move_ids = self.env['account.move'].search(header_domain).ids
        # esclusione righe di testata
        domain.append(('line_type', 'not in', ['debit', 'credit']))
        domain.append(('move_id', 'in', move_ids))
        # TODO patch da verificare !!!
        domain.append(('account_id.internal_type', '!=', 'payable'))

        (total_base,
         total_tax,
         deductible,
         undeductible) = compute_total_child(self, domain, registry_type)
        if self.children_tax_ids:
            total_tax = deductible = undeductible = 0.0
            for child in self.children_tax_ids:
                (total_base,
                 total_tax,
                 deductible,
                 undeductible) = map(
                    sum,
                    zip((total_base, total_tax, deductible, undeductible)),
                    compute_total_child(child, domain, registry_type)
                )

        _logger.info(f"tax_name: {tax_name}\t total_base: {total_base}\t "
                     f"total_tax {total_tax}\t deductible {deductible}\t "
                     f"undeductible {undeductible}")

        return tax_name, total_base, total_tax, deductible, undeductible

    def is_deductible(self):
        if not self.account_id:
            is_deductible = False
        elif getattr(self, 'is_split_payment', None):
            is_deductible = False
        elif getattr(self, 'rc_type', None) and self.rc_type == 'local':
            is_deductible = False
        else:
            is_deductible = True
        # end if
        return is_deductible
    # end is_deductible

    def _against_account(self):
        against_tax = self.env['account.tax']
        if self.account_id:
            if getattr(self, 'rc_sale_tax_id', None):
                num_taxes = self.search_count([
                    ('rc_sale_tax_id', '=', self.id)])

                if num_taxes == 1:
                    against_tax = self.search([
                        ('rc_sale_tax_id', '=', self.id),
                        ])
                # end if
            # end if

        # end if
        return against_tax
    # end is_deductible
