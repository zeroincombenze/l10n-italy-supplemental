# Copyright 2021-2022 LibrERP enterprise network <https://www.librerp.it>
#
# License OPL-1 or later
#   https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps)
#
from odoo import fields, models, api


class AccountMoveLineWrapper(models.TransientModel):
    """
    Wraps he account.move.line model to add feature and to allow the creation
    of "fake" lines that holds the initial and final totals
    """

    _name = "account.move.line.wrapper"

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Fields

    #
    # Link field
    #

    # Field that points the related the account.move.line (if any)
    my_line_id = fields.Many2one(
        comodel_name="account.move.line",
        select=-True,
    )

    #
    # Mirror account.move.line fields needed by the wizard
    #
    date = fields.Date(string="Data registrazione", related="my_line_id.date")

    journal_id = fields.Many2one(
        string="Registro",
        comodel_name="account.journal",
        related="my_line_id.journal_id",
    )

    journal_code = fields.Char(string="Registro", related="my_line_id.journal_id.code")

    move_id = fields.Many2one(
        string="Registrazione Contabile",
        comodel_name="account.move",
        related="my_line_id.move_id",
    )

    ref = fields.Char(string="Riferimento", default=False)

    debit = fields.Monetary(
        string="Dare", currency_field="company_currency_id", default=False
    )
    credit = fields.Monetary(
        string="Avere", currency_field="company_currency_id", default=False
    )
    sym = fields.Char(
        string="€"
    )

    debit_ccy = fields.Monetary(
        string="Dare (valuta)", currency_field="currency_id", default=False
    )
    credit_ccy = fields.Monetary(
        string="Avere (valuta)", currency_field="currency_id", default=False
    )
    sym_ccy = fields.Char(
        string="Ccy"
    )

    name = fields.Char(string="Etichetta", related="my_line_id.name")

    date_maturity = fields.Date(string="Scadenza", related="my_line_id.date_maturity")

    move_type = fields.Selection(string="Tipo reg.", related="my_line_id.move_id.type")

    # Date competenza ratei
    accrual_start_date = fields.Date(
        string="Inizio competenza", related="my_line_id.accrual_start_date"
    )
    accrual_end_date = fields.Date(
        string="Fine competenza", related="my_line_id.accrual_end_date"
    )

    full_reconcile_id = fields.Many2one(
        string="Numero Abbinamento",
        comodel_name="account.full.reconcile",
        related="my_line_id.full_reconcile_id",
    )

    company_currency_id = fields.Many2one(
        comodel_name="res.currency", related="my_line_id.company_currency_id"
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency", related="my_line_id.currency_id"
    )

    #
    # New fields
    #

    move_state = fields.Selection(
        related="my_line_id.move_id.state", string="Stato registrazione"
    )

    # Campo calcolato per visualizzare il saldo giornaliero nell'ultima
    # riga di ciascun giorno
    balance = fields.Monetary(
        string="Saldo", currency_field="company_currency_id", default=0
    )
    balance_ccy = fields.Monetary(
        string="Saldo (valuta)", currency_field="currency_id", default=0
    )

    # Campo per visualizzare la data del documento collegato alla fattura,
    # ossia la fattura / nota di credito collegata alla registrazione
    ref_date = fields.Date(
        string="Data Riferimento", readonly=True, related="my_line_id.invoice_id.date"
    )

    wizard_id = fields.Many2one(comodel_name="account.mastrini.wizardmodel")

    # Field for contropartite and controvalori
    contropartite = fields.Html(string="Contropartite")

    # Field for contropartite and controvalori
    controvalori = fields.Html(string="Controvalori")

    # Flag that if True identifies the line as an empty line whos purpose
    # is to visually render a spacer
    empty_line = fields.Boolean(default=False)

    # Flag that if True identifies the line as a line which is currently
    # live, so it is to be displayed in the UI.
    # If this flag is False the line should be discarded.
    is_alive = fields.Boolean(default=True)

    # Hide tha value of the 'debit', 'credit' and 'balance' fields
    # if the value is 0 (zero)
    hide_zeros = fields.Boolean(default=True)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Actions

    @api.multi
    def account_move_edit_form(self):
        self.ensure_one()
        return {
            "name": "Movimento contabile",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "res_id": self.move_id.id,
            "target": "new",
            "context": self._context.copy(),
        }

    # edn account_move_edit_form

    @api.multi
    def account_move_line_edit_form(self):
        self.ensure_one()
        return {
            "name": "Movimento contabile",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "account.move.line",
            "type": "ir.actions.act_window",
            "res_id": self.my_line_id.id,
            "target": "new",
            "context": self._context.copy(),
        }

    # end account_move_line_edit_form


# end AccountMoveLineWrapper
