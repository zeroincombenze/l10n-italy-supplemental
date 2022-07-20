# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo.osv import expression
from odoo import models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

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
             strftime(strptime(self.date, '%Y-%m-%d') - timedelta(days=60),
                      '%Y-%m-%d')),
            ('date',
             '<=',
             strftime(strptime(self.date, '%Y-%m-%d') + timedelta(days=60),
                      '%Y-%m-%d')),
        ]
        domain = expression.AND([domain, domain_date])

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
            domain, offset=offset, limit=limit, order="date_maturity asc, id asc"
        )
