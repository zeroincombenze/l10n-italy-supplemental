# Copyright 2021-24 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#

import time
from odoo import models, api
from odoo.tools.translate import _
from odoo.tools.misc import formatLang


class VatPeriodEndStatementReport(models.AbstractModel):
    _name = 'report.l10n_it_vat_statement.vat_statement'
    _description = "VAT Statement report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.vat.period.end.statement'].browse(docids)
        vals = {
            'docs': docs,
            'time': time,
            'tax_amounts': self._get_taxes_amounts,
            'account_vat_amounts': self._get_account_vat_amounts,
            'formatLang': formatLang,
            'one_cent_deviation': self._one_cent_deviation,
            'env': self.env,
        }
        return vals

    def _get_statement(self, statement_id):
        statement_obj = self.env['account.vat.period.end.statement']
        statement = False
        if statement_id:
            statement = statement_obj.browse(statement_id)
        return statement

    def _get_taxes_amounts(
        self, period_id, tax_ids=None, registry_type='customer'
    ):
        if tax_ids is None:
            tax_ids = []
        res = {}
        date_range = self.env['date.range'].browse(period_id)
        tax_model = self.env['account.tax']

        for tax_id in tax_ids:
            tax = tax_model.browse(tax_id)
            tax_name, base, tax_val, deductible, undeductible = (
                tax.compute_totals_tax({
                    'from_date': date_range.date_start,
                    'to_date': date_range.date_end,
                    'registry_type': registry_type,
                })
            )

            if (
                tax.cee_type and tax.parent_tax_ids and
                len(tax.parent_tax_ids) == 1
            ):
                # In caso di integrazione iva l'imponibile è solo sulla
                # padre
                parent = tax.parent_tax_ids[0]

                tax_data = parent.compute_totals_tax({
                    'from_date': date_range.date_start,
                    'to_date': date_range.date_end,
                    'registry_type': registry_type,
                    })
                # return tax_name, base, tax_val, deductible, undeductible
                base = tax_data[1]

            # patch split payment
            if getattr(tax, 'is_split_payment', None):
                undeductible = deductible
                deductible = 0.0
            # end if

            # patch N6
            if tax.kind_id and tax.kind_id.code.startswith('N6'):
                undeductible = deductible
                deductible = 0.0
            # end if

            # patch EU OSS
            # if tax.eu_vat:
            if tax.tax_group_id.country_id.code != 'IT':
                undeductible = 0.0
                deductible = 0.0
            # end if

            res[tax_name] = {
                'code': tax_name,
                'vat': tax_val,
                'vat_deductible': deductible,
                'vat_undeductible': undeductible,
                'base': base
            }
        return res

    def _get_account_vat_amounts(
        self, account_type='credit', statement_account_line=None,
    ):
        if statement_account_line is None:
            statement_account_line = []
        if account_type != 'credit' and account_type != 'debit':
            raise Exception(_('Account type neither credit and debit !'))

        account_amounts = {}
        for line in statement_account_line:
            if line.tax_id.eu_vat:
                continue
            account_id = line.account_id.id
            if account_id and line.amount:
                if account_id not in account_amounts:
                    account_amounts[account_id] = {
                        'account_id': line.account_id.id,
                        'account_name': line.account_id.name,
                        'amount': line.amount
                    }
                else:
                    account_amounts[account_id]['amount'] += line.amount
                # end if
            # end if

        return account_amounts

    def _one_cent_deviation(self, statement):

        authority_amount = statement.authority_vat_amount
        statement_total = 0.0

        for line in statement.credit_vat_account_line_ids:
            statement_total += line.amount

        for line in statement.debit_vat_account_line_ids:
            statement_total -= line.deductible_amount

        for line in statement.generic_vat_account_line_ids:
            statement_total += (line.amount*-1)

        statement_total -= statement.previous_credit_vat_amount
        statement_total += statement.previous_debit_vat_amount
        statement_total += statement.interests_debit_vat_amount
        # if there more then 1 cent between the two totals hide
        # the amount into the report is hidden
        one_cent = 0.01

        return (abs(authority_amount) - abs(statement_total)) > one_cent
