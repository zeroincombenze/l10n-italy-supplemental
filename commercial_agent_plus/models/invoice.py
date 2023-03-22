# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class CommercialAgentPlusInvoice(models.Model):
    _inherit = "account.invoice"
    
    commercial_agent_msg = fields.Char(
        string="Message",
        compute="_compute_agent"
    )
    commercial_agent_id = fields.Many2one(
        string="Agent",
        comodel_name="res.users",
        compute="_compute_agent",
        search="_search_agent"
    )
    settlement_id = fields.Many2one(
        string="Settlement",
        comodel_name="commercial.agent.commission.settlement"
    )
    settlement_commission = fields.Monetary(
        string="Total Commission",
        currency_field='currency_id'
    )
    agent_reverse = fields.Boolean(
        string="Agent Reverse?",
        default=False
    )
    agent_reversed = fields.Boolean(
        string="Agent Reversed",
        default=False
    )
    
    @api.depends('invoice_line_ids')
    def _compute_agent(self):
        for invoice in self:
            invoice.commercial_agent_msg = ''
            invoice.commercial_agent_id = False
            agent = invoice.invoice_line_ids.mapped('sale_line_ids.order_id.commercial_agent_id')
            if len(agent) > 1:
                invoice.commercial_agent_msg = _('An invoice must have one agent only')
            else:
                if agent:
                    invoice.commercial_agent_id = agent.id
    
    def _search_agent(self, operator, value):
        return [('invoice_line_ids.sale_line_ids.order_id.commercial_agent_id',operator,value)]

class CommercialAgentPlusPayment(models.Model):
    _inherit = "account.payment"
    
    settlement_id = fields.Many2one(
        string="Settlement",
        comodel_name="commercial.agent.commission.settlement"
    )
    settlement_commission = fields.Monetary(
        string="Total Commission",
        currency_field='currency_id'
    )
    agent_reverse = fields.Boolean(
        string="Agent Reverse?",
        default=False
    )
    agent_reversed = fields.Boolean(
        string="Agent Reversed",
        default=False
    )
    commercial_agent_id = fields.Many2one(
        string="Agent",
        comodel_name="res.users",
        compute="_compute_agent",
        store=True
    )
    
    @api.depends('reconciled_invoice_ids')
    def _compute_agent(self):
        for payment in self:
            payment.commercial_agent_id = False
            agent = payment.reconciled_invoice_ids.mapped('invoice_line_ids.sale_line_ids.order_id.commercial_agent_id')
            if agent:
                payment.commercial_agent_id = agent[0].id
    
    @api.model
    def create(self, vals):
        payment = super(CommercialAgentPlusPayment, self).create(vals)
        payment._compute_agent()
        return payment
