# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import time

from odoo.osv import expression
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    # journal_entry_ids = fields.Many2many(
    #     'account.move',
    #     'bank_statement_move_rel',
    #     'statement_line_id',
    #     'id',
    #     copy=False,
    #     readonly=True
    # )

    @api.multi
    def button_cancel_reconciliation(self):
        super(AccountBankStatementLine, self).button_cancel_reconciliation()
        for st_line in self:
            st_line.journal_entry_ids = [(5, 0)]

    def get_move_lines_for_reconciliation(
        self,
        excluded_ids=None,
        str=False,
        offset=0,
        limit=None,
        additional_domain=None,
        overlook_partner=False,
    ):

        super(AccountBankStatementLine, self).get_move_lines_for_reconciliation(
            excluded_ids=excluded_ids,
            str=str,
            offset=offset,
            limit=limit,
            additional_domain=additional_domain,
            overlook_partner=overlook_partner,
        )

        reconciliation_aml_accounts = [
            self.journal_id.default_credit_account_id.id,
            self.journal_id.default_debit_account_id.id,
        ]
        domain_reconciliation = [
            "&",
            ("statement_id", "=", False),
            ("account_id", "in", reconciliation_aml_accounts),
        ]

        domain_matching = [("reconciled", "=", False)]
        if self.partner_id.id or overlook_partner:
            domain_matching = expression.AND(
                [
                    domain_matching,
                    [("account_id.internal_type", "in", ["payable", "receivable"])],
                ]
            )
        # else:
            # domain_account = expression.OR(
            #     [
            #         [("account_id.reconcile", "=", True)],
            #         [
            #             (
            #                 "account_id.user_type_id",
            #                 "=",
            #                 self.env.ref("account.data_account_type_liquidity").id,
            #             )
            #         ],
            #     ]
            # )
            # domain_matching = expression.AND([domain_matching, domain_account])

        domain = expression.OR([domain_reconciliation, domain_matching])

        strftime = datetime.strftime
        strptime = datetime.strptime
        domain_date = [
            ('date',
             '>=',
             strftime(strptime(self.date, '%Y-%m-%d') - timedelta(days=35),
                      '%Y-%m-%d')),
            ('date',
             '<=',
             strftime(strptime(self.date, '%Y-%m-%d') + timedelta(days=35),
                      '%Y-%m-%d')),
        ]
        domain = expression.AND([domain, domain_date])

        if self.amount_currency and self.currency_id:
            amount = self.amount_currency
        else:
            amount = self.amount
        if amount < 0.0:
            domain_amount = [("credit", "<=", abs(amount))]
        else:
            domain_amount = [("debit", "<=", amount)]
        # domain = expression.AND([domain, domain_amount])

        if self.partner_id.id and not overlook_partner:
            domain = expression.AND([domain, [("partner_id", "=", self.partner_id.id)]])

        ctx = dict(self._context or {})
        ctx["bank_statement_line"] = self
        generic_domain = (
            self.env["account.move.line"]
            .with_context(ctx)
            .domain_move_lines_for_reconciliation(excluded_ids=excluded_ids, str=str)
        )
        domain = expression.AND([domain, generic_domain])

        if additional_domain is None:
            additional_domain = []
        else:
            additional_domain = expression.normalize_domain(additional_domain)
        domain = expression.AND([domain, additional_domain])

        return self.env["account.move.line"].search(
            domain, offset=offset, limit=limit, order="date asc, id asc"
        )

    def process_reconciliation(
            self, counterpart_aml_dicts=None, payment_aml_rec=None, new_aml_dicts=None):
        res = super(AccountBankStatementLine, self).process_reconciliation(
            counterpart_aml_dicts=counterpart_aml_dicts,
            payment_aml_rec=payment_aml_rec,
            new_aml_dicts=new_aml_dicts,
        )
        payment_aml_rec = payment_aml_rec or self.env['account.move.line']
        for aml_rec in payment_aml_rec:
            self.journal_entry_ids = [(3, aml_rec.move_id.id)]
        # self.move_lines_ids = [(3, x) for x in datum['payment_aml_ids']]
