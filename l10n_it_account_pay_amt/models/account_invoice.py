# -*- coding: utf-8 -*-
# Copyright 2021-25 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-25 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-25 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    amount_net_pay = fields.Float(
        string="Net to pay",
        store=True,
        digits=dp.get_precision("Account"),
        readonly=True,
        compute="_compute_net_pay",
    )
    hide_net_pay = fields.Boolean(string="Hide Net to pay",
                                  store=True,
                                  readonly=True,
                                  compute="_compute_net_pay")

    @api.depends("amount_total", "amount_tax")
    def _compute_net_pay(self):
        # TODO> Need to overidden
        for inv in self:
            if not inv.amount_total:
                inv.hide_net_pay = True
                continue
            amount_sp = inv.amount_sp if hasattr(inv, "amount_sp") else 0.0
            amount_rc = inv.amount_rc if hasattr(inv, "amount_rc") else 0.0
            withholding_tax_amount = (
                inv.withholding_tax_amount
                if hasattr(inv, "withholding_tax_amount")
                else 0.0
            )
            inv.amount_net_pay = (
                inv.amount_total
                + amount_sp
                - withholding_tax_amount
                + amount_rc
            )
            inv.hide_net_pay = inv.amount_net_pay == inv.amount_total

    @api.multi
    def action_invoice_draft(self):
        res = True
        for invoice in self:
            saved_date = invoice.date
            res = super(AccountInvoice, self).action_invoice_draft() and res
            if saved_date and invoice.journal_id.type == "purchase":
                invoice.date = saved_date
        return res
