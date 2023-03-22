# Copyright 2021-2022 LibrERP enterprise network <https://www.librerp.it>
#
# License OPL-1 or later
#   https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps)
#
import datetime

from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Helper classes
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class _SumCalculator:

    JOURNALS = ("sale", "purchase")
    KEY_TEMPL = "{fy_id}_{move_type}"
    MONEY_IN = ("out_invoice", "in_refund")
    MONEY_OUT = ("in_invoice", "out_refund")
    MOVE_TYPES = MONEY_IN + MONEY_OUT

    class _Brief:
        def __init__(self, fiscalyar_obj, move_type):
            self._fiscalyear_obj = fiscalyar_obj
            self._move_type = move_type
            self.base_amount = 0.0
            self.tax_amount = 0.0

            if self._move_type not in _SumCalculator.MOVE_TYPES:
                assert False, "Invalid move type: ({})".format(self._move_type)
            # end if

        # end __init__

        @property
        def total(self):
            return self.base_amount + self.tax_amount

        # end total

        def as_vat_brief_line_dict(self):
            return {
                "fiscal_year": self._fiscalyear_obj.id,
                "line_type": self._move_type,
                "description": "",
                "base_amount": self.base_amount,
                "tax_amount": self.tax_amount,
                "total_amount": self.total,
            }

        # end as_vat_brief_line_dict

    # end _Brief

    def __init__(self):

        # Briefs objects stored by key.
        self._move_briefs = dict()

        # Keep track of already processed moves to avoid
        # processing things more than one time.
        self._processed_moves = dict()

    # end __init__

    def process_line(self, move_line_wrapper):
        """Retrieve the move data from the move_line_wrapper and process it.
        If the move has already been processed just skip the line
        """

        # Get the move object
        move = move_line_wrapper.move_id

        if move.id in self._processed_moves:
            # ===>> Move already processed
            return

        elif move.journal_type not in self.JOURNALS or move.type not in self.MOVE_TYPES:
            # ===>> Line with a type we are not interested in.

            # Store the move id in _processed moves with
            # a value of False just to remember this
            # move was considered for processing and
            # skipped because the move type was not
            # 'sale' nor 'purchase'
            self._processed_moves[move.id] = False

            return

        else:
            # ===>> Line to be processed

            # Remember the move was processed to avoid
            # processing it again
            self._processed_moves[move.id] = True

            # Build the key to the relevant _brief object
            brief_object = self._get_brief(move)

            # Process each line in the move
            for mline in move.line_ids:

                if mline.tax_line_id:

                    # - - - - - - - - -
                    # Tax line
                    # - - - - - - - - -

                    if move.type in self.MONEY_IN:
                        tax_amount = mline.credit
                    elif move.type in self.MONEY_OUT:
                        tax_amount = mline.debit
                    else:
                        assert False, (
                            "Move type ({}) is not MONEY_IN {}"
                            " nor in MONEY_OUT {}".format(
                                move.type, self.MONEY_IN, self.MONEY_OUT
                            )
                        )

                    # end if

                    brief_object.tax_amount += tax_amount

                elif mline.tax_ids:

                    # - - - - - - - - -
                    # Base amount line
                    # - - - - - - - - -

                    if move.type in self.MONEY_IN:
                        base_amount = mline.credit
                    elif move.type in self.MONEY_OUT:
                        base_amount = mline.debit
                    else:
                        assert False, (
                            "Move type ({}) is not MONEY_IN {}"
                            " nor in MONEY_OUT {}".format(
                                move.type, self.MONEY_IN, self.MONEY_OUT
                            )
                        )
                    # end if

                    brief_object.base_amount += base_amount

                else:
                    # Something else we are not interested in.
                    pass

                # end if

            # end for

        # end if

    # end process_line

    def build_vat_brief_lines_dicts(self):
        """
        Build account_mastrini_vat_brief_lines from the data stored in the
        object
        """
        dicts = [
            self._move_briefs[key].as_vat_brief_line_dict()
            for key in sorted(self._move_briefs.keys())
        ]

        return dicts

    # end build_vat_brief_lines

    def _get_brief(self, move):
        """
        :param move:
        :return: the _Brief object to be used for this move, if the _Brief
                 object does not exist it will be created and returned.
        """
        fy = move.fiscalyear_id

        key = self.KEY_TEMPL.format(fy_id=fy.id, move_type=move.type)
        brief = self._move_briefs.get(key, False)

        if not brief:
            brief = self._Brief(fiscalyar_obj=fy, move_type=move.type)
            self._move_briefs[key] = brief
        # end if

        return brief


# end SumCalculator


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Wizard model
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class AccountMastriniWizard(models.TransientModel):

    _name = "account.mastrini.wizardmodel"

    # Nature dei conti economici e patrimoniali
    CONTI_ECONOMICI = ("c", "r")
    CONTI_PATRIMONIALI = ("a", "p", "o")

    ACCOUNTS_WITH_PARTNER = ("receivable", "payable")

    # Possibili scelte per il massimo numero di righe visualizzabili
    MAX_ROWS_SELECTION = [50, 100, 200, 500, 750, 1000, 1500, 2000, 3000, 5000, 10000]

    # def select_currency(self):
    #     ccy = [self.env.user.company_id.currency_id.id]
    #     if (self.account_id
    #             and self.account_id.currency_id
    #             and self.account_id.currency_id not in ccy):
    #         ccy.append(self.account_id.currency_id)
    #     if self.partner_id and len(ccy) == 1:
    #         ccy = [x.id for x in self.env["res.currency"].search([])]
    #     return {"currency_id": [("id", "in", ccy)]}
    #     return ccy

    # - - - - - - - - - - - - - - - - - - - - - - -
    # Fields - Filters fields

    # Conto -> account.account
    account_id = fields.Many2one(string="Conto", comodel_name="account.account")
    account_nature = fields.Selection(
        string="Natura",
        selection=[
            ("A", "Attivo"),
            ("P", "Passivo"),
            ("C", "Costi"),
            ("R", "Ricavi"),
            ("O", "Ordine"),
        ],
    )
    account_user_type = fields.Many2one(
        string="Tipo", comodel_name="account.account.type"
    )

    # Data iniziale -> default primo giorno esercizio corrente
    @api.model
    def _default_fy(self):
        if self._search_fy(datetime.date.today()):
            return self._search_fy(datetime.date.today()).id
        else:
            return False
        # end if

    # end _default_fy

    @api.model
    def _is_company_currency(self):
        return (not self.currency_id
                or self.currency_id == self.env.user.company_id.currency_id)

    fiscalyear_id = fields.Many2one(
        string="Anno fiscale:", comodel_name="account.fiscal.year", default=_default_fy
    )

    date_range_id = fields.Many2one(
        string="Periodo",
        comodel_name="date.range",
    )

    filter_by_partner = fields.Boolean(string="Filtra per partner", default=True)
    max_rows = fields.Selection(
        string="Massimo numero di righe visualizzate",
        selection=[(x, str(x)) for x in MAX_ROWS_SELECTION],
        default=50,
    )

    retrieved_rows = fields.Integer(string="Righe totali")

    # Selezione partner
    partner_id = fields.Many2one(
        string="Partner:",
        comodel_name="res.partner",
    )

    # Data iniziale -> default primo giorno esercizio corrente
    date_from = fields.Date(string="Da:")

    # Data finale -> default primo giorno esercizio corrente
    date_to = fields.Date(string="A:")

    # Journal
    journal_id = fields.Many2one(string="Registro", comodel_name="account.journal")

    # Output control fields
    accrual_dates_show = fields.Boolean(string="Date competenze", default=False)

    show_amount_type = fields.Selection(
        string="Tipo importi",
        selection=[
            ("dc", "Dare/Avere"),
            ("residual", "Saldo aperto"),
            ("no-zero-residual", "Partite aperte"),
        ],
        default="dc",
        required=True,
    )

    # Output control fields
    move_state = fields.Selection(
        string="Stato registrazione",
        selection=[
            ("posted", "Confermata"),
            ("draft", "Non Confermata"),
            ("all", "Tutte"),
        ],
        default="posted",
        required=True,
    )

    # Output control fields
    show_contropartite = fields.Selection(
        string="Contropartite",
        selection=[
            ("no", "No"),
            ("partite", "Partite"),
            ("valori", "Valori"),
        ],
        default="no",
        required=True,
    )

    print_order = fields.Selection(
        string="Opzione ordine di stampa",
        selection=[
            ("date", "Data registrazione"),
            ("date_maturity", "Data scadenza"),
            ("date_apply_vat", "Data competenza IVA"),
        ],
        default="date",
        required=False,
    )
    currency_id = fields.Many2one(
        string="Divisa", comodel_name="res.currency")

    is_company_currency = fields.Boolean(
        "Is company currency", default=lambda self: self._is_company_currency)

    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Fields - Data to be shown

    # Righe da visualizzare in Prima Nota
    move_line_ids = fields.One2many(
        compute="_compute_move_line_ids",
        comodel_name="account.move.line.wrapper",
        string="Movimenti",
        inverse_name="wizard_id",
    )

    # Righe da visualizzare in Riepilogo IVA
    vat_brief_line_ids = fields.One2many(
        compute="_compute_vat_brief_line_ids",
        comodel_name="account.mastrini.vat.brief.line",
        string="Riepilogo IVA",
        inverse_name="wizard_id",
    )

    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Fields - Auxiliary data

    # True if a partner must be specified in order to load data
    # This field is True if the account is of type 'receivable' or 'payable'
    partner_needed = fields.Boolean(compute="_compute_partner_needed", default=False)

    # Totali prima dell'inizio periodo selezionato

    # Date from which compute pre-totals
    # This field is not intended to be shown
    pre_date_from = fields.Date(compute="_compute_pre_date_from")

    # Date to which compute pre-totals
    # This field is not intended to be shown
    pre_date_to = fields.Date(compute="_compute_pre_date_to")

    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # OnChange methods

    @api.onchange("fiscalyear_id")
    def _onchange_fy(self):

        # Do nothing if the field is not set to an existing fiscal year
        if self.fiscalyear_id:
            # Update start and end dates
            self.date_from = self.fiscalyear_id.date_from
            self.date_to = self.fiscalyear_id.date_to

        # end if

    # end onchange_fy

    @api.onchange("date_range_id")
    def _onchange_date_range_id(self):

        # Do nothing if the field is not set to an existing fiscal year
        if self.date_range_id:
            # Update start and end dates
            self.date_from = self.date_range_id.date_start
            self.date_to = self.date_range_id.date_end

        # end if

    # end onchange_fy

    @api.onchange("date_from", "date_to")
    def _onchange_date_from_to(self):

        fy = self.fiscalyear_id
        dr = self.date_range_id

        # Unset fiscal year if start and end dates does not match
        if fy:
            if fy.date_from != self.date_from:
                self.fiscalyear_id = False
            # end if

            if fy.date_to != self.date_to:
                self.fiscalyear_id = False
            # end if
        # end if

        # Unset date range if start and end dates does not match
        if dr:
            if dr.date_start != self.date_from:
                self.date_range_id = False
            # end if

            if dr.date_end != self.date_to:
                self.date_range_id = False
            # end if
        # end if

    # end onchange_date_from_to

    @api.multi
    @api.onchange("filter_by_partner")
    def _onchange_filter_by_partner(self):
        if self.filter_by_partner:
            self.max_rows = self.MAX_ROWS_SELECTION[0]
        # end if

    # end onchange_filter_by_partner

    @api.multi
    @api.onchange("account_id")
    def _onchange_account_id(self):
        if self.account_id.id:
            self.account_nature = self.account_id.nature
            self.account_user_type = self.account_id.user_type_id
        else:
            self.account_nature = False
            self.account_user_type = False
        # end if
        # return {"domain": self.select_currency()}
    # end onchange_filter_by_partner

    @api.onchange("currency_id")
    def _onchange_currency_id(self):
        self.is_company_currency = self._is_company_currency()
        if not self.is_company_currency:
            self.show_amount_type = "dc"

    @api.multi
    @api.onchange("move_line_ids")
    def _onchange_move_line_ids(self):
        if self.retrieved_rows > self.max_rows:

            msg = (
                f"Le righe presenti nel database eccedono il limite al numero di righe "
                f'impostato nel campo "Numero massimo righe visualizzate"'
                f"({self.max_rows}/{self.retrieved_rows}).\n"
                f"Per visualizzare ulteriori risultati aumentare il numero di righe "
                f"visualizzabili o cambiare l'intervallo date"
            )

            return {
                "warning": {"title": "Visualizzazione parziale E/C", "message": msg}
            }
        else:
            return None
        # end if

    # end _onchange_move_line_ids

    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Computed fields methods

    @api.multi
    @api.depends("account_id")
    def _compute_partner_needed(self):

        self.ensure_one()
        self.partner_needed = self._is_partner_needed(self.account_id)

    # end _compute_partner_needed

    @api.multi
    @api.depends(
        "account_id",
        "account_nature",
        "account_user_type",
        "currency_id",
        "partner_id",
        "date_from",
        "date_to",
        "journal_id",
        "move_state",
        "max_rows",
        "print_order",
        "show_amount_type",
    )
    def _compute_move_line_ids(self):
        def get_contropartite(line, with_values=False):

            # Select the signs for credit and debit values
            sign_d, sign_c = (-1, 1) if line.debit else (1, -1)

            # Symbol of the current currency to be set
            # after credit/debit values
            cur_sym = line.company_id.currency_id.symbol or ""

            # List with one string for each line
            data_list = list()

            # For each line generate the corresponding string
            # and append it to data_list
            for c_line in line.move_id.line_ids:

                if c_line.id == line.id:
                    # Skip the line currently shown in the mastrino table
                    continue

                else:

                    # - - - - - - - - - - - - -
                    # Account name part
                    act_code = c_line.account_id.code
                    act_name = c_line.account_id.name.strip()

                    if self._is_partner_needed(c_line):
                        act_partner = " ({})".format(c_line.partner_id.name)
                    else:
                        act_partner = ""
                    # end if

                    acct_str = "{code} {name}{partner} ".format(
                        code=act_code, name=act_name, partner=act_partner
                    )

                    # - - - - - - - - - - - - -
                    # Values part
                    if with_values:

                        deb_v = c_line.debit * sign_d
                        cred_v = c_line.credit * sign_c

                        if deb_v or cred_v:
                            # At least one between credit and debit value in != 0,
                            # build the string for each non zero value
                            deb_str = deb_v and "[{}{}]".format(deb_v, cur_sym) or ""
                            cred_str = cred_v and "[{}{}]".format(cred_v, cur_sym) or ""
                        else:
                            # Both values at zero,
                            # set a string to show both values are at zero
                            deb_str = "0.0"
                            cred_str = "0.0"
                        # end if

                        # Set e value separator if both debit and credit strings
                        # are not empty
                        separator = (deb_str and cred_str) and "  /  " or ""

                        # Build the final string and append it to the data_list
                        c_line_str = (
                            "<li>" + acct_str + deb_str + separator + cred_str + "</li>"
                        )

                    else:
                        c_line_str = "<li>" + acct_str + "</li>"

                    # end if

                    data_list.append(c_line_str)

                # end if

            # end for

            # Join the lines and enclose in <ul> tag
            data_str = "<ul>" + "".join(data_list) + "</ul>"

            return data_str

        # end get_contropartite

        # NB: while this function depends on "partner_id" this field is not
        #     used explicitly here since the function _get_lines already
        #     employs it under the hood to filter out account.move.line records

        self.ensure_one()
        _logger.debug(
            f"[{datetime.datetime.now()}] DEBUG - _compute_move_line_ids start"
        )

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Check if all required data are set
        date_filter_ok = self.date_from or self.date_to
        account_filter_ok = bool(self.account_id.id)
        partner_filter_ok = bool(self.partner_id.id)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # If conditions are met start the calculation
        if date_filter_ok and (account_filter_ok or partner_filter_ok):

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Pre-Periodo
            #

            # Init to zero and update if conditions are met
            pre_debit = 0.0
            pre_credit = 0.0
            pre_balance = 0.0
            pre_debit_ccy = 0.0
            pre_credit_ccy = 0.0
            pre_balance_ccy = 0.0
            sym = self.env.user.company_id.currency_id.symbol or ""
            sym_ccy = self.currency_id.symbol or ""

            if self.pre_date_from and self.pre_date_to:

                ts = datetime.datetime.now()
                _logger.debug(
                    f"[{ts}] DEBUG - _compute_move_line_ids\t"
                    "\tSomme periodo precedente BEGIN"
                )

                # Ensure move_lines is an iterable even when the _get_lines method
                # returns False
                # if conditions to start a search were not met.
                move_lines = (
                    self._get_lines(
                        self.pre_date_from, self.pre_date_to, self.move_state
                    )
                    or list()
                )

                # NB: sum() of an empty list is '0' (zero)
                pre_debit = sum([line.debit for line in move_lines])
                pre_credit = sum([line.credit for line in move_lines])
                pre_balance = pre_debit - pre_credit
                pre_debit_ccy = sum([self.get_line_debit(line) for line in move_lines])
                pre_credit_ccy = sum(
                    [self.get_line_credit(line) for line in move_lines])
                pre_balance_ccy = pre_debit_ccy - pre_credit_ccy

                te = datetime.datetime.now()
                _logger.debug(
                    f"[{te}] DEBUG - _compute_move_line_ids\t"
                    "\tSomme periodo precedente END ({te - ts})"
                )

            # end if

            pre_period_wrapped_lines = [
                # Linea vuota
                {"empty_line": True},
                # Totali Pre-Periodo
                {
                    "position_in_view": 0,
                    "debit": pre_debit,
                    "credit": pre_credit,
                    "balance": pre_balance,
                    "ref": "Totali al {:%d/%m/%Y}".format(self.pre_date_to),
                    "hide_zeros": False,
                },
                # Linea vuota
                {"empty_line": True},
            ]

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Periodo
            #

            # Estrazione linee periodo
            ts = datetime.datetime.now()
            _logger.debug(
                f"[{ts}] DEBUG - _compute_move_line_ids\t"
                "\tEstrazione linee periodo BEGIN"
            )
            move_lines = self._get_lines(self.date_from, self.date_to, self.move_state)
            te = datetime.datetime.now()
            _logger.debug(
                f"[{te}] DEBUG - _compute_move_line_ids\t"
                "\tEstrazione linee periodo END ({te - ts})"
            )

            # Calcolo totali PERIODO
            current_debit = sum([line.debit for line in move_lines])
            current_credit = sum([line.credit for line in move_lines])
            current_balance = current_debit - current_credit
            current_debit_ccy = sum([self.get_line_debit(line) for line in move_lines])
            current_credit_ccy = sum(
                [self.get_line_credit(line) for line in move_lines])
            current_balance_ccy = current_debit_ccy - current_credit_ccy

            # Limitazione numero di righe visualizzate
            move_lines = move_lines[: self.max_rows]

            ts = datetime.datetime.now()
            _logger.debug(
                f"[{ts}] DEBUG - _compute_move_line_ids\t\tWrapping linee periodo BEGIN"
            )
            period_wrapped_lines = [
                {
                    "my_line_id": line,
                    "debit": line.debit,
                    "credit": line.credit,
                    "sym": sym,
                    "debit_ccy": self.get_line_debit(line),
                    "credit_ccy": self.get_line_credit(line),
                    "sym_ccy": sym_ccy,
                    "ref": line.ref,
                    "contropartite": get_contropartite(line),
                    "controvalori": get_contropartite(line, with_values=True),
                }
                for line in move_lines
            ]  # SLOW FUNCTION
            te = datetime.datetime.now()
            _logger.debug(
                f"[{te}] DEBUG - _compute_move_line_ids\t"
                "\tWrapping linee periodo END ({te - ts})"
            )

            # Add balance to each line ts = datetime.datetime.now()
            ts = datetime.datetime.now()
            _logger.debug(
                f"[{ts}] DEBUG - _compute_move_line_ids\t\tRolling balance BEGIN"
            )
            self._rolling_balance(
                initial_balance=pre_balance,
                initial_balance_ccy=pre_balance_ccy,
                wrapped_lines=period_wrapped_lines
            )
            te = datetime.datetime.now()
            _logger.debug(
                f"[{te}] DEBUG - _compute_move_line_ids\t"
                "\tRolling balance END ({te - ts})"
            )

            # Change the 'my_line_id' attribute from object to integer id
            # since the ORM wants numeric IDs not objects
            for line in period_wrapped_lines:
                line["my_line_id"] = line["my_line_id"].id
            # end for

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Post-Periodo
            #

            # Calcolo totali POST (= totali PRE + totali PERIODO)
            post_debit = pre_debit + current_debit
            post_credit = pre_credit + current_credit
            post_balance = post_debit - post_credit
            post_debit_ccy = pre_debit_ccy + current_debit_ccy
            post_credit_ccy = pre_credit_ccy + current_credit_ccy
            post_balance_ccy = post_debit_ccy - post_credit_ccy

            post_period_wrapped_lines = [
                # Linea vuota
                {"empty_line": True},
                # Totali Periodo
                {
                    "debit": current_debit,
                    "credit": current_credit,
                    "balance": current_balance,
                    "debit_ccy": current_debit_ccy,
                    "credit_ccy": current_credit_ccy,
                    "balance_ccy": current_balance_ccy,
                    "ref": "Totali periodo",
                    "hide_zeros": False,
                },
                # Totali Post-Periodo
                {
                    "debit": post_debit,
                    "credit": post_credit,
                    "balance": post_balance,
                    "debit_ccy": post_debit_ccy,
                    "credit_ccy": post_credit_ccy,
                    "balance_ccy": post_balance_ccy,
                    "ref": "Totali al {:%d/%m/%Y}".format(self.date_to),
                    "hide_zeros": False,
                },
                # Linea vuota
                {"empty_line": True},
            ]
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Creazione recordset di line.wrappers
            #
            wrapped_lines_values = list()
            wrapped_lines_values += pre_period_wrapped_lines
            wrapped_lines_values += period_wrapped_lines[
                : self.max_rows
            ]  # Limitazione numero di righe da visualizzare
            wrapped_lines_values += post_period_wrapped_lines

            # Create the wrapped lines
            ts = datetime.datetime.now()
            _logger.debug(
                f'[{ts}] DEBUG - _compute_move_line_ids\t"'
                f'"\t"Create" delle linee wrapped BEGIN'
            )
            line_wrappers = self.env["account.move.line.wrapper"].create(
                wrapped_lines_values
            )
            te = datetime.datetime.now()
            _logger.debug(
                f'[{te}] DEBUG - _compute_move_line_ids\t"'
                f'"\t"Create" delle linee wrapped END ({te - ts})'
            )
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Assegnazione linee a wizard recordset
            ts = datetime.datetime.now()
            _logger.debug(
                f"[{ts}] DEBUG - _compute_move_line_ids"
                f"\t\tAssegnazione delle wrapped lines al wizard BEGIN"
            )
            self.move_line_ids = line_wrappers
            te = datetime.datetime.now()
            _logger.debug(
                f"[{te}] DEBUG - _compute_move_line_ids"
                f"\t\tAssegnazione delle wrapped lines al wizard END ({te - ts})"
            )

            _logger.debug(
                f"[{datetime.datetime.now()}] "
                "DEBUG - _compute_move_line_ids end ({len(self.move_line_ids)} lines)"
            )
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        else:
            _logger.debug(
                f"[{datetime.datetime.now()}] "
                "DEBUG - _compute_move_line_ids end (no lines)"
            )
            self.move_line_ids = False
        # end if

    # end _compute_pre_amounts

    @api.multi
    @api.depends("move_line_ids")
    def _compute_vat_brief_line_ids(self):

        # TODO: se il conto NON è ne receivable ne payable:
        #       - COME IMPOSTO I SEGNI?
        #       - DEVO CALCOLARE IL RIEPILOGO IVA SOLO PER I CONTI receivable / payable?

        # Get the journal type, if not set store False in the variable
        journal_type = (
            self.account_id
            and self.account_id.user_type_id
            and self.account_id.user_type_id.type
        )

        # Perform the VAT brief calculation only for
        # 'receivable' or 'payable' journals
        if journal_type in ("receivable", "payable"):

            sum_calculator = _SumCalculator()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Create the brief lines
            for mline in self.move_line_ids:
                sum_calculator.process_line(mline)
            # end for

            brief_dicts = sum_calculator.build_vat_brief_lines_dicts()
            brief_lines = self.env["account.mastrini.vat.brief.line"].create(
                brief_dicts
            )

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Set sign of the lines
            if journal_type == "receivable":
                out_sign = 1
                in_sign = -1
            elif journal_type == "payable":
                out_sign = -1
                in_sign = 1
            else:
                assert False
            # end if

            for brief_line in brief_lines:
                if brief_line.line_type in ("out_invoice", "in_refund"):
                    brief_line.sign = out_sign
                elif brief_line.line_type in ("in_invoice", "out_refund"):
                    brief_line.sign = in_sign
                else:
                    assert False
                # end if
            # end for

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Create record for totals
            base_amount = sum(
                [brief_line.base_amount * brief_line.sign
                 for brief_line in brief_lines]
            )
            tax_amount = sum(
                [brief_line.tax_amount * brief_line.sign
                 for brief_line in brief_lines]
            )
            totals_line = self.env["account.mastrini.vat.brief.line"].create(
                {
                    "line_type": "totals",
                    "base_amount": base_amount,
                    "tax_amount": tax_amount,
                    "total_amount": base_amount + tax_amount,
                }
            )

            spacer_before = self.env["account.mastrini.vat.brief.line"].create(
                {"line_type": "spacer"}
            )
            spacer_after = self.env["account.mastrini.vat.brief.line"].create(
                {"line_type": "spacer"}
            )

            # Add the totals record to the brief_lines record set
            brief_lines = brief_lines | spacer_before | totals_line | spacer_after
            # TODO: sort the record set!!!!

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Assign the lines
            self.vat_brief_line_ids = brief_lines

        # end if

    # end _compute_vat_brief_line_ids

    @api.multi
    @api.depends("account_id", "date_from")
    def _compute_pre_date_from(self):

        self.ensure_one()

        if self.account_id:

            account_nature = self.account_id.user_type_id.nature.lower()

            # Selezione data di inizio
            if account_nature in self.CONTI_ECONOMICI:

                # Conti economici: date_from è l'inizio dell'anno fiscale
                #                  corrispondente al filtro data inizio.
                #
                # NB: date_from viene impostata a False se:
                # - non trovo un anno fiscale che combacia
                # - il filtro data inizio non è impostato
                # in questo caso la ricerca NON viene eseguita e i totali
                # vengono impostati a zero.
                if self.date_from:
                    fy = self._search_fy(self.date_from)
                    self.pre_date_from = fy and fy.date_from or False
                #  else:
                #     date_from = False
                # end if

            elif account_nature in self.CONTI_PATRIMONIALI:
                # Conti patrimoniali: si parte dall'inizio dei tempi
                self.pre_date_from = datetime.date(1, 1, 1)

            else:
                assert False, (
                    "Il conto in esame non rientra ne tra quelli economici "
                    "(natura 'r' o 'c') ne tra quelli patrimoniali "
                    "(natura 'a', 'p', 'o'). Natura rilevata {}".format(
                        account_nature)
                )
            # end if
        # end if

    # end _compute_pre_date_from

    @api.multi
    @api.depends("date_from")
    def _compute_pre_date_to(self):
        self.ensure_one()

        assert self.date_from, 'Data "Da:" non impostata!'
        assert self.date_from > datetime.date(
            1, 1, 1
        ), 'Data "Da:" fuori intervallo validità!'

        self.pre_date_to = self.date_from - datetime.timedelta(days=1)

    # end _compute_pre_date_to

    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - -
    # Utility methods

    @api.model
    def _is_partner_needed(self, account):
        # Check if both the fields account_id has and account_id.user_type_id
        # have a valid value, if not return False
        if account and account.user_type_id:
            return account.user_type_id.type in self.ACCOUNTS_WITH_PARTNER
        else:
            return False
        # end if

    # end _is_partner_needed

    @api.model
    def _search_fy(self, search_date):

        fiscalyears = self.env["account.fiscal.year"].search(
            [
                ("date_from", "<=", search_date),
                ("date_to", ">=", search_date),
            ],
        )

        if fiscalyears:
            return fiscalyears[0]
        else:
            return None
        # end if

    # end _search_fy

    @api.model
    def _get_lines(self, date_from, date_to, state):

        assert state in ("posted", "draft", "all")

        # Setup the domain filter
        domain = []

        # # Filter by partner
        # if self.partner_id.id:
        #     domain.append(('partner_id', '=', self.partner_id.id))
        # # end if

        # Filter by account
        if self.account_id.id:
            domain.append(("account_id", "=", self.account_id.id))

        else:
            account_model = self.env["account.account"]

            if self.account_nature:
                accounts_list = account_model.search(
                    [("nature", "=", self.account_nature)]
                )
                if accounts_list:
                    domain.append(("account_id", "in", accounts_list.ids))
                else:
                    domain.append(("account_id", "in", "[]"))
            # end if

            if self.account_user_type:
                accounts_list = account_model.search(
                    [("user_type_id", "=", self.account_user_type.id)]
                )
                if accounts_list:
                    domain.append(("account_id", "in", accounts_list.ids))
                else:
                    domain.append(("account_id", "in", "[]"))
                # end if
            # end if
        # end if

        # Filter by move state if required
        if state != "all":
            domain.append(("move_id.state", "=", state))
        # end if

        if date_from:
            domain.append(("date", ">=", date_from))
        # end if

        if date_to:
            domain.append(("date", "<=", date_to))
        # end if

        # Filter by partner
        if self.partner_id.id:
            domain.append(("partner_id", "=", self.partner_id.id))
        # end if

        # Filter by journal
        if self.journal_id.id:
            domain.append(("journal_id", "=", self.journal_id.id))
        # end if

        if self.show_amount_type == "no-zero-residual":
            domain.append(("amount_residual", "!=", 0.0))

        order_by = "date asc"

        if self.print_order:
            order_by = self.print_order + " asc"
        # end if

        # Search for matching elements
        lines = self.env["account.move.line"].search(
            domain,
            order=order_by + ", id asc",
            # order=order_by + 'date asc, id asc',
        )

        # Store the number of rows retrieved from the DB to be able to
        # warn the user when part of the lines gets discarded due to
        # the max limits of rows to be shown
        self.retrieved_rows = len(lines)

        # Return the result
        return lines

    # end _get_lines

    @api.model
    def get_line_debit(self, line):
        if self.show_amount_type != "dc":
            return line.amount_residual if line.amount_residual > 0.0 else 0.0
        elif self.is_company_currency:
            return line.debit
        elif line.currency_id == self.currency_id:
            return line.amount_currency if line.amount_currency > 0.0 else 0.0
        if line.currency_id:
            amount_currency = line.currency_id._convert(
                line.debit,
                self.env.user.company_id.currency_id,
                line.company_id,
                line.date
            )
        else:
            amount_currency = line.debit
        return self.env.user.company_id.currency_id._convert(
            amount_currency,
            self.currency_id,
            line.company_id,
            line.date
        )

    @api.model
    def get_line_credit(self, line):
        if self.show_amount_type != "dc":
            return -line.amount_residual if line.amount_residual < 0.0 else 0.0
        elif self.is_company_currency:
            return line.credit
        elif line.currency_id == self.currency_id:
            return -line.amount_currency if line.amount_currency < 0.0 else 0.0
        if line.currency_id:
            amount_currency = line.currency_id._convert(
                line.credit,
                self.env.user.company_id.currency_id,
                line.company_id,
                line.date
            )
        else:
            amount_currency = line.credit
        return self.env.user.company_id.currency_id._convert(
            amount_currency,
            self.currency_id,
            line.company_id,
            line.date
        )

    @api.model
    def _rolling_balance(self, initial_balance, initial_balance_ccy, wrapped_lines):
        """
        Computes the "rolling balance" and set it's value on each line.
        """

        # Start from the "pre-balance"
        rolling_balance = initial_balance
        rolling_balance_ccy = initial_balance_ccy
        for line in wrapped_lines:
            line_balance = line["debit"] - line["credit"]  # Balance for this line
            rolling_balance = (
                rolling_balance + line_balance
            )  # Update the rolling balance
            line["balance"] = rolling_balance
            line["sym"] = self.env.user.company_id.currency_id.symbol or ""

            line_balance_ccy = line["debit_ccy"] - line["credit_ccy"]
            rolling_balance_ccy = (
                rolling_balance_ccy + line_balance_ccy
            )  # Update the rolling balance
            line["balance_ccy"] = rolling_balance_ccy
            line["sym_ccy"] = self.currency_id.symbol or ""
        # end for

        return True

    # end _rolling_balance

    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# end AccountMastrino
