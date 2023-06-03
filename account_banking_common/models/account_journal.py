# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    _DEFAULT_FINANCING_PCT = {
        "invoice_amount": 80,
        "taxable_amount": 100,
    }

    def _domain_accreditation_account_debit_id(self):
        return [
            (
                "user_type_id",
                "in",
                [
                    self.env.ref("account.data_account_type_current_assets").id,
                    self.env.ref("account.data_account_type_liquidity").id,
                    self.env.ref("account.data_account_type_receivable").id,
                    self.env.ref("account.data_account_type_payable").id,
                ],
            )
        ]

    def _domain_accreditation_account_credit_id(self):
        return [
            (
                "user_type_id",
                "in",
                [
                    self.env.ref("account.data_account_type_current_assets").id,
                    self.env.ref("account.data_account_type_liquidity").id,
                    self.env.ref("account.data_account_type_receivable").id,
                    self.env.ref("account.data_account_type_payable").id,
                ],
            )
        ]

    def _domain_expenses_account(self):
        return [
            (
                "user_type_id",
                "in",
                [
                    self.env.ref("account.data_account_type_expenses").id,
                    self.env.ref("account.data_account_type_direct_costs").id,
                ],
            )
        ]

    def _domain_sezionale(self):
        return [
            ("type", "in", ["bank", "general"]),
        ]

    def _domain_main_sezionale(self):
        return [
            ("type", "in", ["bank", "cash"]),
            ("is_wallet", "=", False),
        ]

    @api.depends("accreditation_account_credit_id")
    def _importo_effetti(self):
        for rec in self:
            if (
                rec.accreditation_account_credit_id
                and rec.accreditation_account_credit_id.id
            ):
                query_select_account_balance = """
                 SELECT
                    SUM(debit) - SUM(credit) as balance
                    FROM account_move_line, account_move
                    WHERE account_move_line.account_id = {account_id}
                    and account_move_line.move_id = account_move.id
                    and account_move.state = 'posted'
                """.format(
                    account_id=rec.accreditation_account_credit_id.id
                )

                self.env.cr.execute(query_select_account_balance)

                anticipo = [r[0] for r in self.env.cr.fetchall()]
                rec.importo_effetti_sbf = anticipo[0]
            else:
                rec.importo_effetti_sbf = 0.0

    @api.depends("accreditation_account_credit_id")
    def _impegno_effetti(self):
        for rec in self:
            if (
                rec.accreditation_account_credit_id
                and rec.accreditation_account_credit_id.id
            ):
                query_select_account_balance = """
                SELECT
                    SUM(debit) - SUM(credit) as balance
                    FROM account_move_line, account_move
                    WHERE (account_move_line.account_id = {account_id}
                    and account_move_line.move_id = account_move.id
                    and account_move.state <> 'posted')
                """.format(
                    account_id=rec.accreditation_account_credit_id.id,
                )

                self.env.cr.execute(query_select_account_balance)

                impegno = [r[0] for r in self.env.cr.fetchall()]
                rec.impegno_effetti_sbf = impegno[0]
            else:
                rec.impegno_effetti_sbf = 0.0

    @api.depends("limite_effetti_sbf", "importo_effetti_sbf")
    def _disponibilita_effetti(self):
        for bank in self:
            if bank.wallet_ids:
                residuo = 0.0
                for wallet in bank.wallet_ids:
                    wallet._disponibilita_effetti()
                    residuo += wallet.disponibilita_effetti_sbf
            else:
                residuo = bank.limite_effetti_sbf + (
                    bank.importo_effetti_sbf + bank.impegno_effetti_sbf
                )

            if residuo > 0:
                bank.disponibilita_effetti_sbf = residuo
            else:
                bank.disponibilita_effetti_sbf = 0.0

    def _set_main_bank_account_id_default(self):
        return self.env["account.journal"]

    def _set_wallet_ids_default(self):
        domain = [
            ("type", "in", ["bank", "cash"]),
            ("is_wallet", "=", True),
            ("main_bank_account_id", "=", self.id),
        ]

        return self.search(domain)

    def is_wallet_default(self):
        if self.bank_account_id:
            return self.bank_account_id.bank_is_wallet
        else:
            return False

    @api.depends("wallet_ids")
    def _has_children(self):
        for journal in self:
            if journal.wallet_ids:
                journal.has_children = True
            else:
                journal.has_children = False

    is_wallet = fields.Boolean(string="Conto di portafoglio", default=is_wallet_default)

    wallet_ids = fields.One2many(
        comodel_name="account.journal",
        inverse_name="main_bank_account_id",
        string="Conti di portafoglio",
        default=_set_wallet_ids_default,
        readonly=True,
    )

    main_bank_account_id = fields.Many2one(
        comodel_name="account.journal",
        string="Conto principale di liquidità",
        domain=_domain_main_sezionale,
        default=_set_main_bank_account_id_default,
    )

    has_children = fields.Boolean(string="Conto padre", compute="_has_children")

    invoice_financing_evaluate = fields.Selection(
        [
            ("invoice_amount", "percentuale su totale"),
            ("taxable_amount", "imponibile su imponibile"),
        ],
        default="invoice_amount",
        string="Metodo calcolo anticipo fatture",
    )

    invoice_financing_percent = fields.Float(
        string="Percentuale di anticipo fatture",
        default=80.0,
    )

    sezionale = fields.Many2one(
        string="Sezionale",
        comodel_name="account.journal",
        domain=_domain_sezionale,
    )

    accreditation_account_debit_id = fields.Many2one(
        string="Accreditation account (debit side - Subject To Collection C/O)",
        comodel_name="account.account",
        oldname="effetti_allo_sconto",
        domain=_domain_accreditation_account_debit_id,
    )

    accreditation_account_credit_id = fields.Many2one(
        string="Accreditation account (credit side - C/O portfolio bank)",
        comodel_name="account.account",
        oldname="portafoglio_sbf",
        domain=_domain_accreditation_account_credit_id,
    )

    accreditation2_account_debit_id = fields.Many2one(
        string="Accreditation account (debit side – supplemental)",
        comodel_name="account.account",
        oldname="effetti_presentati",
        domain=_domain_accreditation_account_debit_id,
    )

    accreditation2_account_credit_id = fields.Many2one(
        string="Accreditation account (credit side – supplemental)",
        comodel_name="account.account",
        domain=_domain_accreditation_account_credit_id,
    )

    bank_expense_account_id = fields.Many2one(
        string="Bank Expenses account",
        oldname="default_bank_expenses_account",
        comodel_name="account.account",
        domain=_domain_expenses_account,
        help="Conto predefinito per registrare le spese bancarie",
    )

    limite_effetti_sbf = fields.Float(string="Affidamento bancario SBF", default=0.0)

    importo_effetti_sbf = fields.Float(
        string="Portafoglio utilizzato", compute="_importo_effetti"
    )

    impegno_effetti_sbf = fields.Float(
        string="Importo da presentare", compute="_impegno_effetti"
    )

    disponibilita_effetti_sbf = fields.Float(
        string="Disponibilità residua", compute="_disponibilita_effetti"
    )

    liquidity_account_id = fields.Many2one(
        "account.account",
        related='main_bank_account_id.default_debit_account_id',
        string='A/C Bank Account',
        readonly=True)

    @api.onchange("is_wallet")
    def _on_change_is_wallet(self):
        if not self.is_wallet:
            if self.main_bank_account_id:
                self.main_bank_account_id = self._set_main_bank_account_id_default()
        else:
            if self.default_debit_account_id.user_type_id != self.env.ref(
                "account.data_account_type_receivable"
            ):
                return {
                    "warning": {
                        "title": _("Attenzione"),
                        "message": _(
                            "Il conto dare predefinito deve essere "
                            "un conto di tipo credito clienti"
                        ),
                    }
                }
            if self.default_credit_account_id.user_type_id != self.env.ref(
                "account.data_account_type_receivable"
            ):
                return {
                    "warning": {
                        "title": _("Attenzione"),
                        "message": _(
                            "Il conto avere predefinito deve essere "
                            "un conto di tipo credito clienti"
                        ),
                    }
                }
        if self.bank_account_id:
            bank_account = self.env["res.partner.bank"].browse(self.bank_account_id.id)
            bank_account.write({"bank_is_wallet": self.is_wallet})

    @api.model
    def get_payment_method_config(self):
        if self.is_wallet:
            return {
                "sezionale": self.sezionale,
                "transfer_journal": self.sezionale,
                "bank_journal": self.main_bank_account_id,
                "liquidity_account_id": self.liquidity_account_id,
                "transfer_account": self.accreditation_account_credit_id,
                "acceptance_account_id": self.default_debit_account_id,
                "accreditation_account_debit_id": self.accreditation_account_debit_id,
                "accreditation_account_credit_id": self.accreditation_account_credit_id,
                "accreditation2_account_debit_id": self.accreditation2_account_debit_id,
                "accreditation2_account_credit_id":
                    self.accreditation2_account_credit_id,
                "bank_expense_account_id": self.bank_expense_account_id,
            }
        else:
            return {
                "sezionale": self.sezionale,
                "transfer_journal": self.sezionale,
                "bank_journal": self,
                "liquidity_account_id": self.default_debit_account_id,
                "transfer_account": False,
                "acceptance_account_id": False,
                "accreditation_account_debit_id": False,
                "accreditation_account_credit_id": False,
                "accreditation2_account_debit_id": False,
                "accreditation2_account_credit_id": False,
                "bank_expense_account_id": self.bank_expense_account_id,
            }

    @api.onchange("invoice_financing_evaluate")
    def _onchange_invoice_financing_evaluate(self):
        method = self.invoice_financing_evaluate
        pct_default = self._DEFAULT_FINANCING_PCT.get(method, 0)
        pct_set = bool(self.invoice_financing_percent)

        if not pct_set or not method:
            self.invoice_financing_percent = pct_default
        # end if

    # _onchange_invoice_financing_evaluate

    @api.model
    def _validate_invoice_financing_percent(self):
        ife_set = self.invoice_financing_evaluate is not False
        pct_set = self.invoice_financing_percent not in [False, 0]

        if ife_set and not pct_set:
            raise UserError(
                "Percentuale anticipo non impostata! "
                "La percentuale deve essere maggiore di zero"
            )
        # end if

    # end _validate_invoice_financing_percent
