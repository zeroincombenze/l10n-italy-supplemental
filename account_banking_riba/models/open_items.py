# -*- coding: utf-8 -*-
# Copyright 2018-23 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Open items manager
This module manages Odoo open items of payment orders.
Open items are created from move lines (add_move_line) and result is a list of couple
(account, partner) to close on payment confirmation (settlement).
Payment order (account.payment.order) or l10n-italy C/o list (riba.distinta) must be
supplied in order to set configuration.

The function load_move_vals returns the value for new payment confirmation move. Notice
returned dict could be empty if there are no open items to close.
The move values may be configured by end user (see _load_line_ref function).

After added payment move created above to open items (function couple_settlement) you
can also reconcile all move line records using do_reconcile() function.

The class is designed to work on Odoo 10.0 and 12.0. It automatically recognizes the
type of payment line supplied.
"""

from datetime import date
import re

from odoo import fields
try:
    from odoo.exceptions import Warning as UserError
except ImportError:
    from odoo.exceptions import UserError



class OpenItems(object):

    def __init__(self):
        self.amount = 0.0
        self.account_ids = {}
        self.partner_amounts = {}
        self.move_line_ids = []
        self.payorder_lines = []
        self.env = None
        self.settlement_journal_id = False
        self.liquidity_account_id = False
        self.bank_expense_account_id = False
        self.receivable_accs = []
        self.move_date = False
        self.payment_ref = "Incasso RIBA %(order)s - %(name)s"
        self.odoo_version = 0

    def _load_line_ref(self, payorder_lines, name="name", partners=None, due_date=None):
        """Load line reference which is a composition of come items:
        * %(order)s -> Payment order number
        * %(ln)s -> Payment line reference
        * %(name)s -> Customer name(s)
        * %(date)s -> Due date
        """
        def _str(obj, name):
            return str(getattr(obj, name)) if name == "sequence" else getattr(obj, name)

        def _load_multiple_refs(refs, name, maxlen=30):
            if len(refs) == 0:
                return ""
            elif len(refs) == 1:
                return _str(refs[0], name)
            return ", ".join(
                set(
                    [
                        " ".join(_str(x, name).split(" ")[0:2])[0:maxlen]
                        for x in refs
                    ]
                )
            )

        params = {"name": "", "ln": "", "order": "", "date": ""}
        partners = partners or list(self.partner_amounts.keys())
        if not isinstance(partners, (list, tuple)):
            partners = [partners]
        if isinstance(partners, set):
            partners = list(partners)
        params["name"] = _load_multiple_refs(partners, name)

        if not isinstance(payorder_lines, (list, tuple)):
            payorder_lines = [payorder_lines]
        if isinstance(payorder_lines, set):
            payorder_lines = list(payorder_lines)
        payorders = []
        if hasattr(payorder_lines[0], "order_id"):
            params["ln"] = _load_multiple_refs(payorder_lines, "name")
            payorders = list(set([x.order_id for x in self.payorder_lines]))
        elif hasattr(payorder_lines[0], "distinta_id"):
            params["ln"] = "l." + _load_multiple_refs(payorder_lines, "sequence")
            payorders = list(set([x.distinta_id for x in self.payorder_lines]))
        params["order"] = _load_multiple_refs(payorders, "name")

        if due_date:
            if isinstance(due_date, date):
                params["date"] = date.today().strftime("%d-%m-%Y")
            else:
                params["date"] = due_date

        line_ref = (self.payment_ref % params).strip()
        return re.sub(
            "([/,:+-])+ +[/,:+-]+",
            r"\1",
            re.sub("^[ /,:+-]+(.*)", r"\1", re.sub("(.*)[ /,:+-]+$", r"\1", line_ref)),
        ).strip()

    def _get_side(self, move_line):
        return "credit" if move_line.credit > 0.0 else "debit"

    def _set_odoo_env(self, inv_line=None):
        if not self.env:
            self.env = inv_line.env
            self.valid_account_types = (
                self.env.ref("account.data_account_type_current_assets"),
                self.env.ref("account.data_account_type_current_liabilities"),
                self.env.ref("account.data_account_type_liquidity"),
                self.env.ref("account.data_account_type_receivable"),
                self.env.ref("account.data_account_type_payable"),
            )
            from odoo import release

            self.odoo_version = release.version_info[0]
        if (
            hasattr(inv_line, "account_id")
            and inv_line.account_id.user_type_id
            == self.env.ref("account.data_account_type_receivable")
            and inv_line.account_id not in self.receivable_accs
        ):
            self.receivable_accs.append(inv_line.account_id)

    def _load_config(self, payorder_line):
        """Load configuration from payment order line"""
        self._set_odoo_env(payorder_line)
        if self.odoo_version == 10:
            # Odoo 10.0: payment order line is <riba.distinta.line>
            self.move_date = date.today().strftime("%Y-%m-%d")
            config = payorder_line.distinta_id.config_id
            for field, cfgkey in (
                ("liquidity_account_id", "liquidity_account_id"),
                ("settlement_journal_id", "settlement_journal_id"),
                ("bank_expense_account_id", "bank_expense_account_id"),
            ):
                if not getattr(self, field):
                    if not getattr(config, cfgkey):
                        raise UserError(
                            "Missing value for configuration field '%s'" % field
                        )
                    setattr(self, field, getattr(config, cfgkey))
                elif getattr(self, field) != getattr(config, cfgkey):
                    raise UserError(
                        "Conflict values for configuration field '%s'" % field
                    )
        elif self.odoo_version == 12:
            # Odoo 12.0: payment order line is <account.payment.line>
            self.move_date = fields.Date.today()
            config = payorder_line.order_id.get_move_config()
            for field, cfgkey in (
                ("liquidity_account_id", "liquidity_account_id"),
                ("settlement_journal_id", "bank_journal"),
                ("bank_expense_account_id", "bank_expense_account_id"),
            ):
                if not getattr(self, field):
                    if not config[cfgkey]:
                        raise UserError(
                            "Missing value for configuration field '%s'" % field
                        )
                    setattr(self, field, config[cfgkey])
                elif getattr(self, field) != config[cfgkey]:
                    raise UserError(
                        "Conflict values for configuration field '%s'" % field
                    )

    def _load_line_values(self, account, partner, side, amount=None):
        if side not in ("debit", "credit"):
            raise UserError("Invalid %s value: must be 'debit' or 'credit'" % side)
        opposite_side = "debit" if side == "credit" else "credit"
        key = (account, partner)
        if self.odoo_version == 10:
            vals = {"name": self._load_line_ref(self.payorder_lines, partners=partner)}
        elif self.odoo_version == 12:
            if self.account_ids.get(key, {}).get("payorder_lines"):
                vals = {
                    "name": self._load_line_ref(
                        self.account_ids[key]["payorder_lines"], partners=partner
                    )
                }
            else:
                vals = {
                    "name": self._load_line_ref(self.payorder_lines, partners=partner)
                }
        vals.update(
            {
                "partner_id": partner.id if partner else False,
                "account_id": account.id,
                side: 0.0,
                opposite_side: amount
                or min(
                    abs(self.partner_amounts.get(partner, self.amount)),
                    abs(self.amount),
                ),
            }
        )
        return vals

    def declare_text_refs(self, payment_ref):
        self.payment_ref = payment_ref

    def add_move_line(self, move_line):
        """Add move line to Open Item"""
        if move_line in self.move_line_ids:
            return
        if move_line.move_id.journal_id.type in ("sale", "sale_refund"):
            self._set_odoo_env(move_line)
            if move_line.partner_id not in self.partner_amounts:
                self.partner_amounts[move_line.partner_id] = 0.0
            balance = move_line.debit - move_line.credit
            self.partner_amounts[move_line.partner_id] += balance
            self.amount += balance
        if move_line.account_id.user_type_id in self.valid_account_types and (
            not move_line.partner_id
            or move_line.partner_id in list(self.partner_amounts.keys())
        ):
            self.move_line_ids.append(move_line)
            side = self._get_side(move_line)
            key = (move_line.account_id, move_line.partner_id)
            if key not in self.account_ids:
                self.account_ids[key] = {
                    "debit": 0.0,
                    "credit": 0.0,
                    "payorder_lines": set(),
                }
            self.account_ids[key][side] += move_line[side]
            if self.odoo_version == 12:
                for payorder_line in move_line.payment_line_ids:
                    self.account_ids[key]["payorder_lines"].add(payorder_line)
                    self.add_payorder_line(payorder_line, force=False)

    def add_payorder_line(self, payorder_line, force=True):
        """Add payment order line to Open Item and set configuration if needed
        The move lines related to payment order line, are loaded too"""
        if payorder_line not in self.payorder_lines and (
            force or payorder_line.partner_id in list(self.partner_amounts.keys())
        ):
            self.payorder_lines.append(payorder_line)
            self._load_config(payorder_line)

            if self.odoo_version == 10:
                # Invoice lines
                for move_line in [x.move_line_id for x in payorder_line.move_line_ids]:
                    self.add_move_line(move_line)
                for move_line in payorder_line.acceptance_move_id.line_ids:
                    self.add_move_line(move_line)
                for (
                    move_line
                ) in payorder_line.distinta_id.accreditation_move_id.line_ids:
                    self.add_move_line(move_line)
            elif self.odoo_version == 12:
                for move in payorder_line.order_id.move_ids:
                    for move_line in move.line_ids:
                        self.add_move_line(move_line)
        return self

    def load_move_vals(self, move_date=None, expenses_amount=0.0):
        partners = list(self.partner_amounts.keys())
        if self.odoo_version == 10:
            vals = {
                "ref": self._load_line_ref(self.payorder_lines, partners=partners),
                "journal_id": self.settlement_journal_id.id,
                "date": move_date or self.move_date,
                "line_ids": [],
            }
        elif self.odoo_version == 12:
            vals = self.env["account.move"].default_get(
                [
                    "date_effective",
                    "fiscalyear_id",
                    "invoice_date",
                    "narration",
                    "payment_term_id",
                    "reverse_date",
                    "tax_type_domain",
                ]
            )
            if len(set([x.order_id for x in self.payorder_lines])) == 1:
                vals["payment_order_id"] = self.payorder_lines[0].order_id.id
            vals.update(
                {
                    "ref": self._load_line_ref(self.payorder_lines, partners=partners),
                    "journal_id": self.settlement_journal_id.id,
                    "date": move_date or self.move_date,
                    # "date_apply_vat": move_date or self.move_date,
                    "type": "entry",
                    "state": "draft",
                    "line_ids": [],
                }
            )

        total_debit = total_credit = 0.0
        for account, partner in self.account_ids.keys():
            key = (account, partner)
            balance = self.account_ids[key]["debit"] - self.account_ids[key]["credit"]
            # Ignore liquidity account and paired debit/credit accounts
            if (
                not balance
                or account == self.liquidity_account_id
                or account in self.receivable_accs
            ):
                continue
            side = "credit" if balance < 0.0 else "debit"
            line_vals = self._load_line_values(account, partner, side)
            if self.odoo_version == 12 and self.account_ids[key]["payorder_lines"]:
                line_vals["payment_line_ids"] = []
                for payorder_line in self.account_ids[key]["payorder_lines"]:
                    line_vals["payment_line_ids"].append((4, payorder_line.id))
            if vals.get("payment_order_id"):
                line_vals["payment_order"] = vals["payment_order_id"]
            vals["line_ids"].append((0, 0, line_vals))
            total_debit += line_vals["credit"]
            total_credit += line_vals["debit"]

        if total_debit == total_credit and not vals["line_ids"]:
            expenses_amount = 0.0
            vals = {}
        elif total_debit > total_credit:
            line_vals = self._load_line_values(
                self.liquidity_account_id,
                partners[0] if len(partners) == 1 else False,
                "credit",
                amount=(total_debit - total_credit),
            )
            vals["line_ids"].append((0, 0, line_vals))
        elif total_debit < total_credit:
            line_vals = self._load_line_values(
                self.liquidity_account_id,
                partners[0] if len(partners) == 1 else False,
                "debit",
                amount=(total_credit - total_debit),
            )
            vals["line_ids"].append((0, 0, line_vals))

        if expenses_amount > 0:
            line_vals = self._load_line_values(
                self.expense_id, False, "debit", amount=expenses_amount
            )
            vals["line_ids"].append((0, 0, line_vals))
            line_vals = self._load_line_values(
                self.liquidity_id, False, "credit", amount=expenses_amount
            )
            vals["line_ids"].append((0, 0, line_vals))
        return vals

    def couple_settlement(self, settlement_move):
        for line in settlement_move.line_ids:
            if line.account_id == self.liquidity_account_id:
                self.add_move_line(line)

    def do_reconciles(self):
        reconciles = {}
        for move_line in self.move_line_ids:
            if move_line.reconciled:
                continue
            side = self._get_side(move_line)
            account = move_line.account_id
            partner = move_line.partner_id
            if (account, partner) in self.account_ids and account.reconcile:
                if (account, partner) not in reconciles:
                    reconciles[(account, partner)] = {}
                reconciles[(account, partner)][side] = move_line
        for account, partner in reconciles:
            if reconciles[(account, partner)].get("debit") and reconciles[
                (account, partner)
            ].get("credit"):
                to_be_reconciled = self.env["account.move.line"]
                to_be_reconciled |= reconciles[(account, partner)]["debit"]
                to_be_reconciled |= reconciles[(account, partner)]["credit"]
                to_be_reconciled.reconcile()
