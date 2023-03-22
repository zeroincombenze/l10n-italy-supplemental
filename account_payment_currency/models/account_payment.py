#
# Copyright 2022-23 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _default_currency_amount(self):
        amount_total_company = 0.0
        for invoice in self.invoice_ids:
            amount_total_company += invoice.amount_total_company_signed
        return amount_total_company

    company_currency_amount = fields.Monetary(
        string='Company Currency Payment Amount',
        default=_default_currency_amount)
    company_currency_id = fields.Many2one(
        'res.currency',
        string='Company Currency',
        related='company_id.currency_id',
        store=True)

    @api.onchange("amount", "currency_id", "payment_date", "journal_id")
    def _onchange_any_currency_amount(self):
        invoice_currency = False
        amount_total_company = 0.0
        for invoice in self.invoice_ids:
            if not invoice_currency:
                invoice_currency = invoice.currency_id
            if invoice.currency_id != invoice_currency:
                raise UserError(_("You cannot pay invoices with different currencies"))
            amount_total_company += invoice.amount_total_company_signed
        if self.journal_id.currency_id == invoice_currency:
            self.company_currency_amount = amount_total_company
        else:
            currency_rate_ids = self.env["res.currency.rate"].search(
                [
                    ("currency_id", "=", self.currency_id.id),
                    ("name", "=", datetime.strftime(self.payment_date, "%Y-%m-%d")),
                    '|',
                    ('company_id', '=', self.company_id.id),
                    ('company_id', '=', False),
                ]
            )
            if currency_rate_ids:
                self.company_currency_amount = (
                    currency_rate_ids[0].currency_id._convert(
                        self.amount,
                        self.company_currency_id,
                        self.company_id,
                        self.payment_date))
            else:
                self.company_currency_amount = 0.0
