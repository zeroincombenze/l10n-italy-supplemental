# -*- coding: utf-8 -*-
# Copyright 2021-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.depends(
        "amount_total",
        "amount_sp",
        "amount_rc",
        "withholding_tax_amount",
    )
    def _compute_net_pay(self):
        res = super()._compute_net_pay()
        for inv in self:
            inv.amount_net_pay = (
                inv.amount_total
                - inv.amount_sp
                - inv.amount_rc
                - inv.withholding_tax_amount
            )
            inv.hide_net_pay = inv.amount_net_pay == inv.amount_total
        return res
