#
# Copyright 2020-24 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-24 librERP enterprise network <https://www.librerp.it>
# Copyright 2020-24 Didotech s.r.l. <https://www.didotech.com>
#


import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends("payment_line_ids")
    def _compute_amount_payment_line(self):
        for record in self:
            if record.payment_line_ids and len(record.payment_line_ids) > 0:
                order_line = record.payment_line_ids[len(record.payment_line_ids) - 1]
                record.amount_into_payment_line = order_line.amount_currency
            else:
                record.amount_into_payment_line = False

    @api.model
    def set_default_company_bank(self):
        if (
            self.invoice_id.type == "out_invoice"
            and hasattr(self.move_id, "company_bank_id")
            and self.move_id.company_bank_id
        ):
            return self.move_id.company_bank_id.id
        else:
            return False

    # end set_default_company_bank

    @api.model
    def set_default_counterparty_bank(self):
        if (
            self.invoice_id.type == "out_invoice"
            and hasattr(self.move_id, "counterparty_bank_id")
            and self.move_id.counterparty_bank_id
        ):
            return self.move_id.counterparty_bank_id
        else:
            return False

    # end set_default_counterparty_bank

    payment_method = fields.Many2one(
        "account.payment.method", string="Metodo di pagamento"
    )

    calculate_field = fields.Char(string="Domain test", compute="_domain_test")

    is_duedate = fields.Boolean(string="Riga di scadenza", compute="_compute_is_dudate")

    duedate_line_id = fields.Many2one(
        comodel_name="account.duedate_plus.line",
        string="Riferimento riga scadenza",
        indexed=True,
    )

    payment_order = fields.Many2one(
        comodel_name='account.payment.order',
        string='Record ordine di pagamento',
        readonly=True,
    )

    payment_order_name = fields.Char(
        string='Ordine di pagamento',
        related='payment_order.name',
        readonly=True,
    )

    state = fields.Selection(
        string="Stato",
        related="payment_line_ids.order_id.state",
        readonly=True,
    )

    in_order = fields.Boolean(
        string='In distinta',
        compute='_has_order',
        inverse='_inverse_has_order',
        search='_search_has_order',
    )

    payment_line_ids = fields.One2many(
        comodel_name='account.payment.line',
        inverse_name='move_line_id',
        string="Payment lines",
        # oldname="payment_order_lines"
    )

    incasso_effettuato = fields.Boolean(
        string='Incasso effettuato', default=False
    )

    prorogation_ctr = fields.Integer(string='Numero di proroghe')

    unpaid_ctr = fields.Integer(string="Numero di insoluti")

    iban = fields.Char(related="partner_bank_id.acc_number", string="IBAN")

    company_bank_id = fields.Many2one(
        comodel_name="res.partner.bank",
        string="Conto Bancario aziendale",
        default=set_default_company_bank,
        domain=lambda self: [
            ("partner_id", "=", self.env.user.company_id.partner_id.id)
        ],
    )

    counterparty_bank_id = fields.Many2one(
        string="Banca d'appoggio",
        comodel_name="res.partner.bank",
        default=set_default_company_bank,
        copy=True,
    )

    pagamento_effettuato = fields.Boolean(string="Pagamento effettuato", default=False)

    amount_into_payment_line = fields.Float(
        string="Importo in distinta", compute=_compute_amount_payment_line
    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ONCHANGE METHODS

    @api.onchange("account_id")
    def onchange_account_id(self):

        domain = []

        if self.account_id:
            account_type = self.env["account.account.type"].search(
                [("id", "=", self.account_id.user_type_id.id)]
            )
            if account_type:
                if account_type.type == "payable":
                    domain = [
                        "|",
                        ("debit_credit", "=", "debit"),
                        ("debit_credit", "=", False),
                    ]
                elif account_type.type == "receivable":
                    domain = [
                        "|",
                        ("debit_credit", "=", "credit"),
                        ("debit_credit", "=", False),
                    ]

        return {"domain": {"payment_method": domain}}

    # ONCHANGE METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _has_order(self):
        for line in self:
            rec = self.env['account.payment.line'].search(
                [('move_line_id', '=', line.id)]
            )
            if rec:
                line.in_order = True
            else:
                line.in_order = False

    def _inverse_has_order(self):
        for line in self:
            rec = self.env['account.payment.line'].search(
                [('move_line_id', '=', line.id)]
            )
            if rec:
                line.in_order = True
            else:
                line.in_order = False

    def _search_has_order(self, operator, value):
        recs = self.search([]).filtered(lambda x: x.in_order is False)
        if recs:
            return [('id', 'in', [x.id for x in recs])]

    @api.model
    def _compute_is_dudate(self):
        for line in self:

            not_vat_line = (not line.tax_ids) and (not line.tax_line_id)
            credit_or_debit = line.account_id.user_type_id.type in (
                "payable",
                "receivable",
            )

            line.is_duedate = not_vat_line and credit_or_debit

    # end _compute_is_dudate

    def _domain_test(self):
        for rec in self:
            if rec.account_id:
                account_type = self.env["account.account.type"].search(
                    [("id", "=", rec.account_id.user_type_id.id)]
                )
                if account_type:
                    if account_type.type == "payable":
                        rec.calculate_field = "debit"
                    elif account_type.type == "receivable":
                        rec.calculate_field = "credit"

    # @api.model
    # def create(self, values):
    #     res = super().create(values)
    #     return res
    # # end create

    @api.multi
    def write(self, values):

        result = super().write(values)

        if not self.env.context.get("RecStop"):
            if "date_maturity" in values:
                for move in self:
                    move.with_context(RecStop=True).update_date_maturity()

            if "payment_method" in values:
                for move in self:
                    move.with_context(RecStop=True).update_payment_method()

        return result

    # Update the associated duedate_line
    @api.model
    def update_date_maturity(self):
        if self.duedate_line_id:
            self.duedate_line_id.due_date = self.date_maturity

    @api.model
    def update_payment_method(self):
        if self.duedate_line_id:
            self.duedate_line_id.payment_method_id = self.payment_method

