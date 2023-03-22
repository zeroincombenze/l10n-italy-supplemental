# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
"""
Account entries are (invoice amount is 100):

1.generated2uploaded()       | (3) one journal entry per due date
    Create account entry after banking file is uploaded. Managed by OCA module
    account_payment_order. Journal depends on payment mode.
    Account entry; account date is due date (in the future)
    if no wallet transfer bank account is used.
    | Description             | Debit | Credit | Notes
    |🕑Receivable account     |       |    100 | (2) from invoice
    |🕓Pay off/Effetti attivi |   100 |        | (1)/(2)(4) from journal debit/credit

TYPE 1
2.action_accreditato() -> registra_accredito()
    Create account entry after bank accepted the uploaded file.
    Account entry type 1, one entry:
    | Description             | Debit | Credit | Notes
    |🕘Portafoglio SBF        |       |    100 | (3) from journal portafoglio_sbf
    |🕕Effetti allo sconto    |   100 |        | (3) from journal effetti_allo_sconto
3.open_wizard_payment_confirm() -> registra_incasso()
    Create account entry when customer really pays for invoice. Bank transfer customer
    payment on company banking account. All account balances must be closed.
    Account entry type 1, 1 entry for every bank transfer (invoice amount 100):
    | Description             | Debit | Credit | Notes
    |🕓Pay off/Effetti attivi |       |    100 | (2)(4) from journal debit/credit
    |🕛Liquidity account      |   100 |        | (1) from parent journal debit/credit
    |🕕Effetti allo sconto    |       |    100 | (1) from journal effetti_allo_sconto
    |🕘Portafoglio SBF        |   100 |        | (1) from journal portafoglio_sbf

TYPE 2
2.action_accreditato() -> registra_accredito()
    Create account entry after bank accepted the uploaded file.
    Account entry type 2, one entry:
    | Description             | Debit | Credit | Notes
    |🕓Pay off/Effetti attivi |       |    100 | (2)(4) from journal debit/credit
    |🕕Effetti allo sconto    |   100 |        | (3) from journal effetti_allo_sconto
    |                         |       |        |
    |🕕Effetti allo sconto    |       |    100 | (3) from journal effetti_allo_sconto
    |  Effetti presentati     |   100 |        | (3) from journal effetti_presentati
3.open_wizard_payment_confirm() -> registra_incasso()
    Create account entry when customer really pays for invoice. Bank transfer customer
    payment on company banking account. All account balances must be closed.
    Account entry type 2, 1 entry for every bank transfer (invoice amount 100):
    | Description             | Debit | Credit | Notes
    |  Effetti presentati     |       |    100 | (3) from journal effetti_presentati
    |🕛Liquidity account      |   100 |        | (1) from parent journal debit/credit

Notes:
    (1) One line for journal entry
    (2) One line for every line in payment order (invoice line due date)
    (3) One line per due date (records grouped by due date)
    (4) OCA uses an ordinary asset account; Librerp uses receivable account with partner


All account entries are based on following elements:

- sezionale (journal): journal used in some account entries
- transfer_journal (journal): journal used in some account entries
- bank_journal (journal): journal used in some account entries
- pay-off (account): debit / credit account from journal
- transfer_account (account); usused (it servers for OCA modules)
- portafoglio_sbf (account): same of portafoglio_sbf for type 1 entries
- conto_effetti_attivi (account): credit account of action_accreditato()
- effetti_allo_sconto (account): debit account of action_accreditato()
                                 on journal/bank record may be called portafoglio_sbf
- conto_spese_bancarie (account): banking expenses
"""
from collections import defaultdict
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    @api.depends("payment_line_ids")
    def _compute_incassi_effettuati(self):
        for order in self:
            order.has_incassi_effettuati = False
            for line in order.payment_line_ids:
                if line.move_line_id.incasso_effettuato:
                    order.has_incassi_effettuati = True
                    break
                # end if
            # end for
        # end for

    # end _compute_incassi_effettuati

    payment_method_code = fields.Char(
        string="Codice metodo di pagamento",
        related="payment_method_id.code",
    )

    is_wallet_company_bank = fields.Boolean(
        string="Conto di portafoglio aziendale",
        related="company_partner_bank_id.bank_is_wallet",
    )

    has_incassi_effettuati = fields.Boolean(
        string="Ha incassi effettuati",
        compute="_compute_incassi_effettuati",
    )

    @api.multi
    def action_accreditato(self):

        for order in self:
            if order.state == "uploaded":
                # validation
                if order.payment_method_code not in ["riba_cbi", "sepa_direct_debit"]:
                    raise UserError(
                        "Attenzione!\nIl metodo di pagamento non "
                        "permette l'accreditamento."
                    )

                # apertura wizard
                return {
                    "type": "ir.actions.act_window",
                    "name": "Accreditamento",
                    "res_model": "wizard.payment.order.credit",
                    "view_type": "form",
                    "view_mode": "form",
                    "view_id": self.env.ref(
                        "account_banking_common.wizard_payment_order_credit"
                    ).id,
                    "target": "new",
                    "res_id": False,
                    "binding_model_id": "account.model_account_payment_order",
                }

    @api.multi
    def registra_accredito(self):
        # The payment method of the selected lines
        raise UserError(
            f"Procedura di registrazione accredito non definita "
            f"per il metodo di pagamento {self.payment_mode_id.name}"
        )

    # end registra_accredito

    @api.multi
    def registra_accredito_standard(self):

        account_expense_id = self._context.get("expenses_account_id")
        amount_expense = self._context.get("expenses_amount")
        credit_date = self._context.get("credit_date")

        if not credit_date:
            credit_date = fields.Date.today()

        for payment_order in self:

            cfg = payment_order.get_move_config()

            # validazione conti impostati

            if not cfg["sezionale"].id:
                raise UserError("Attenzione!\nSezionale non " "impostato.")

            if not cfg["effetti_allo_sconto"].id:
                raise UserError(
                    "Attenzione!\nConto effetti allo sconto " "non impostato."
                )

            if not cfg["bank_journal"].id:
                raise UserError("Attenzione!\nConto di costo non impostato.")

            # bank_account = cfg['bank_journal'].default_credit_account_id

            lines = self.env["account.payment.line"].search(
                [("order_id", "=", payment_order.id)]
            )

            for line in lines:

                # per ogni riga
                # genero una registrazione

                line_ids = []

                # se ci sono spese le aggiungo
                if amount_expense > 0:

                    credit_account = self.set_expense_credit_account(
                        cfg["bank_journal"]
                    )

                    expense_move_line = {
                        "account_id": account_expense_id,
                        "credit": 0,
                        "debit": amount_expense,
                    }
                    line_ids.append((0, 0, expense_move_line))

                    bank_expense_line = {
                        "account_id": credit_account.id,
                        "credit": amount_expense,
                        "debit": 0,
                    }
                    line_ids.append((0, 0, bank_expense_line))
                # end if

                # conto effetti allo sconto
                effetti_allo_sconto = {
                    "account_id": cfg["effetti_allo_sconto"].id,
                    "credit": 0,
                    "debit": line.amount_currency,
                }
                line_ids.append((0, 0, effetti_allo_sconto))

                effetti_attivi = {
                    "account_id": cfg["conto_effetti_attivi"].id,
                    "partner_id": line.partner_id.id,
                    "credit": line.amount_currency,
                    "debit": 0,
                }
                line_ids.append((0, 0, effetti_attivi))

                vals = self.env["account.move"].default_get(
                    [
                        # 'date_apply_balance',
                        "date_effective",
                        "fiscalyear_id",
                        "invoice_date",
                        "narration",
                        "payment_term_id",
                        "reverse_date",
                        "tax_type_domain",
                    ]
                )
                vals.update(
                    {
                        "date": credit_date,
                        "date_apply_vat": credit_date,
                        "journal_id": cfg["sezionale"].id,
                        "type": "entry",
                        "ref": "Accreditamento ",
                        "state": "draft",
                        "line_ids": line_ids,
                        "payment_order_id": payment_order.id,
                    }
                )

                # Creazione registrazione contabile
                self.env["account.move"].create(vals)

            payment_order.action_done()

    # end registra_accredito_standard

    @api.multi
    def unlink(self):

        for order in self:
            if order.state != "cancel":
                raise UserError(
                    f"L'ordine di pagamento {order.name} non può essere"
                    f'eliminato perché non è nello stato "Annullato"'
                )
            # end if
        # end for

        return super(AccountPaymentOrder, self).unlink()

    # end unlink

    @api.multi
    def cancel2draft(self):
        res = super().cancel2draft()
        for order in self:
            lines = self.env["account.move.line"].search(
                [("payment_order", "=", order.id)]
            )
            lines.write({"incasso_effettuato": False})

        return res

    @api.model
    def get_move_config(self):
        """Returns the journals and accounts to be used for new account.move records."""

        po = self
        pay_mode = po.payment_mode_id

        # 1 - Get default config from journal

        cfg = po.journal_id.get_payment_method_config()

        # 2 - Get overrides from payment mode
        if pay_mode.offsetting_account == "transfer_account":
            assert pay_mode.transfer_journal_id.id
            cfg["transfer_journal"] = pay_mode.transfer_journal_id
            cfg["sezionale"] = cfg["transfer_journal"]

            assert pay_mode.transfer_account_id.id
            cfg["transfer_account"] = pay_mode.transfer_account_id
            cfg["conto_effetti_attivi"] = cfg["transfer_account"]
            cfg["effetti_allo_sconto"] = cfg["transfer_account"]
        # end if

        # 3 - Add bank journal
        cfg["bank_journal"] = po.journal_id

        return cfg

    # end get_move_config

    @api.model
    def set_expense_credit_account(self, journal):

        if journal.is_wallet:
            main_journal = journal.main_bank_account_id
            credit_account = main_journal.default_credit_account_id
        else:
            credit_account = journal.default_credit_account_id
        # end if

        return credit_account

    def prepare_move_lines(self, account, side, mode=None):
        """Prepare all move line from payment order
        Line may be grouped by date (mode="date")

        Args:
            account (obj): account ID for move line
            side (str): may be 'debit' or 'credit'
            mode (str): may be 'line', 'duedate', 'sum'
                * line: means 1 line of every payment line
                * duedate: group bye due date
                * sum: sum all line amounts
                * auto: means 'line' if account is receivable else duedate

        Returns:
            list of account.move.line values to use in account_move.line_ids
        """
        if mode == "auto":
            mode = "line" if account.user_type_id.type == "receivable" else "duedate"
        move_lines = list()
        if mode == "line":
            for line in self.payment_line_ids:
                vals = line.prepare_1_move_line(account.id, side)
                move_lines.append((0, 0, vals))
        elif mode == "duedate":
            groups = defaultdict(list)
            [
                groups[line.ml_maturity_date].append(line.amount_currency)
                for line in self.payment_line_ids
            ]
            sum_list = [
                (key, sum(groups[key]))
                for key in groups.keys()
            ]
            line = self.payment_line_ids[0]
            for duedate in sum_list:
                vals = line.prepare_1_move_line(
                    account.id, side, duedate=duedate[0], amount=duedate[1])
                move_lines.append((0, 0, vals))
        elif mode == "sum":
            amount = sum([list.amount_currency for line in self.payment_line_ids])
            vals = self.payment_line_ids[0].prepare_1_move_line(
                account.id, side, amount=amount)
            move_lines.append((0, 0, vals))
        else:
            raise UserError(
                "Invalid %s value: must be 'line' or 'duedate' or 'sum'" % mode
            )
        return move_lines

    @api.multi
    def _create_reconcile_move(self, hashcode, blines):
        self.ensure_one()
        post_move = self.payment_mode_id.post_move
        am_obj = self.env["account.move"]
        mvals = self._prepare_move(blines)
        move = am_obj.create(mvals)
        is_wallet = self.company_partner_bank_id.bank_is_wallet
        if is_wallet:
            move.invoice_date = move.date
            move.date = fields.Date.today()
        blines.reconcile_payment_lines()
        if post_move:
            move.post()

    # end _create_reconcile_move

    @api.multi
    def _prepare_move(self, bank_lines=None):
        vals = super()._prepare_move(bank_lines)

        if self.payment_mode_id.offsetting_account == "bank_account":
            account = self.journal_id.default_debit_account_id
        elif self.payment_mode_id.offsetting_account == "transfer_account":
            account = self.payment_mode_id.transfer_account_id

        if account.user_type_id.type not in ("payable", "receivable"):
            return vals
        else:
            vals["line_ids"] = []
            for bline in bank_lines:
                partner_ml_vals = self._prepare_move_line_partner_account(bline)
                vals["line_ids"].append((0, 0, partner_ml_vals))
                trf_ml_vals = self._prepare_move_line_single_offsetting_account(bline)
                vals["line_ids"].append((0, 0, trf_ml_vals))
        return vals

    @api.multi
    def _prepare_move_line_single_offsetting_account(self, bank_line):
        vals = {}
        if self.payment_type == "outbound":
            name = _("Payment order %s") % self.name
        else:
            name = _("Debit order %s") % self.name
        if self.payment_mode_id.offsetting_account == "bank_account":
            vals.update({"date": bank_line.date})
        else:
            vals.update({"date_maturity": bank_line.date})

        if self.payment_mode_id.offsetting_account == "bank_account":
            account_id = self.journal_id.default_debit_account_id.id
        elif self.payment_mode_id.offsetting_account == "transfer_account":
            account_id = self.payment_mode_id.transfer_account_id.id
        partner_id = bank_line.payment_line_ids[0].partner_id.id
        vals.update(
            {
                "name": name,
                "partner_id": partner_id,
                "account_id": account_id,
                "credit": (
                    self.payment_type == "outbound"
                    and bank_line.amount_company_currency
                    or 0.0
                ),
                "debit": (
                    self.payment_type == "inbound"
                    and bank_line.amount_company_currency
                    or 0.0
                ),
            }
        )
        if bank_line.currency_id != bank_line.company_currency_id:
            sign = self.payment_type == "outbound" and -1 or 1
            vals.update(
                {
                    "currency_id": bank_line.currency_id.id,
                    "amount_currency": bank_line.amount_currency * sign,
                }
            )
        return vals


class AccountPaymentLine(models.Model):
    _inherit = "account.payment.line"

    def prepare_1_move_line(self, account_id, side, duedate=None, amount=None):
        """Prepare account move line value"""
        if side not in ("debit", "credit"):
            raise UserError(
                "Invalid %s value: must be 'debit' or 'credit'" % side
            )
        amount_side = amount or self.amount_currency
        if amount_side < 0.0:
            opposite_side = side
            side = "debit" if opposite_side == "credit" else "credit"
            amount_side = abs(amount_side)
        else:
            opposite_side = "debit" if side == "credit" else "credit"
        values = {
            "account_id": account_id,
            side: amount_side,
            opposite_side: 0.0,
        }
        if not duedate and amount:
            values["name"] = str(
                f'Distinta scadenze {self.order_id.name}'
            )
        elif duedate:
            values["name"] = str(
                f'Distinta scadenze {self.order_id.name}'
                ' - '
                f'Scadenza {duedate}'
            )
        else:
            values["name"] = str(
                f'Distinta scadenze {self.order_id.name}'
                ' - '
                f'Fattura {self.move_line_id.move_id.name}'
            )
            values["partner_id"] = self.partner_id.id
        return values
