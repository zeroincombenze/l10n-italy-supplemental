# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.tools.float_utils import float_round


class SettlementLine(models.Model):
    _inherit = "sale.commission.settlement.line"

    calculated_commission_rate = fields.Float(
        string="Commission Rate",
        compute="_compute_commission_rate",
    )
    customer_id = fields.Many2one(
        comodel_name="res.partner",
        related="agent_line.invoice.partner_id",
        readonly=True,
        store=True)

    def _compute_commission_rate(self):
        for line in self:
            if line.invoice_line and line.invoice_line.price_subtotal:
                line.calculated_commission_rate = float_round(
                    line.settled_amount * 100 / line.invoice_line.price_subtotal,
                    precision_digits=2)
            else:
                line.calculated_commission_rate = 0.0
