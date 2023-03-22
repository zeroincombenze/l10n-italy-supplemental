# -*- coding: utf-8 -*-
from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from .record_rules_plus import agent_group, agent_manager, agent_all


class CommercialAgentPlusSettlement(models.Model):
    _name = "commercial.agent.commission.settlement"
    _inherit = ['mail.thread']
    _description = "Settlement"

    def _default_currency(self):
        return self.env.user.company_id.currency_id.id

    def _commercial_agents_domain(self):
        """
        get users who are part of the agent_group or agent_manager group
        """
        return [
            ('groups_id', 'in', 
            [self.env.ref(agent_group).id,
            self.env.ref(agent_manager).id])
        ]

    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True
    )
    name = fields.Char(
        string="Name", 
        default="SE*****")
    currency_id = fields.Many2one(
        comodel_name="res.currency", readonly=True, default=_default_currency,
        tracking=True
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True, 
        default=lambda self: self.env.user.company_id,
        tracking=True
    )
    state = fields.Selection(
        selection=[
            ("draft", _("Draft")),
            ("settled", _("Settled")),
            ("invoiced", _("Invoiced"))
        ],
        string="Status",
        readonly=True,
        default="draft",
        tracking=True
    )
    date_from = fields.Date(string="Date Start", tracking=True)
    date_to = fields.Date(string="Date End", tracking=True)
    agent_id = fields.Many2one(
        string='Commercial Agent',
        comodel_name="res.users",
        domain=_commercial_agents_domain,
        tracking=True
    )
    partner_agent_id = fields.Many2one(
        string='Commercial Agent Partner',
        comodel_name="res.partner",
        related="agent_id.partner_id"
    )
    commission_type = fields.Selection(
        string="Commission Type",
        selection = [
            ('invoiced', _('Invoiced')),
            ('cashed', _('Cashed'))
        ],
        compute="_compute_commission_type",
        store=True,
        tracking=True
    )
    commission_order_ids = fields.Many2many(
        string="Commissionm Order Lines",
        comodel_name="commercial.agent.sale.commission",
        relation="settlement_commission_orders"
    ) 
    invoice_ids = fields.One2many(
        string="Invoices",
        comodel_name="account.invoice",
        inverse_name="settlement_id",
        domain=[('type','=','out_invoice')]
    )
    reverse_invoice_ids = fields.Many2many(
        string="Reverse Invoices",
        comodel_name="account.invoice",
        domain=[('type','=','out_refund')]
    )
    payment_ids = fields.One2many(
        string="Payments",
        comodel_name="account.payment",
        inverse_name="settlement_id",
    )
    reverse_payment_ids = fields.Many2many(
        string="Reverse Payments",
        comodel_name="account.payment",
    )
    
    total_commission = fields.Monetary(
        string="Total Commission",
        currency_field='currency_id',
        compute="_compute_total"
    )
    total_order_amount = fields.Monetary(
        string="Total Amount",
        currency_field='currency_id',
        compute="_compute_total"
    )
    total_amount_untaxed_signed = fields.Monetary(
        string="Total Untaxed Invoiced",
        currency_field='currency_id',
        compute="_compute_total"
    )
    total_to_settle = fields.Monetary(
        string="Total to settle",
        currency_field='currency_id'
    )
    total_to_subtract = fields.Monetary(
        string="Total to subtract",
        currency_field='currency_id',
        compute="_compute_total"
    )
    total_settle = fields.Monetary(
        string="Total to settle",
        currency_field='currency_id',
        compute="_compute_total"
    )
    
    warning_msg = fields.Html(
        string="Earning Message",
        compute="_compute_warning_msg"
    )
    forced = fields.Boolean(string="Forced",default=False,
        tracking=True)
    forced_by = fields.Many2one(
        string="Forced By",
        comodel_name="res.users",
        tracking=True
    )
    
    agent_invoice_id = fields.Many2one(
        string="Agent Invoice",
        comodel_name="account.invoice"
    )
    note = fields.Html(
        string="Note"
    )
    
    @api.depends('agent_id')
    def _compute_commission_type(self):
        for record in self:
            record.commission_type = False
            if record.agent_id and record.agent_id.partner_id.commercial_agent_commission_type:
                record.commission_type = record.agent_id.partner_id.commercial_agent_commission_type
    
    @api.depends('agent_id', 'date_from', 'date_to')
    def _compute_warning_msg(self):
        for record in self:
            record.warning_msg = ''
            agent_id = record.agent_id
            date_from = record.date_from
            date_to = record.date_to
            if agent_id and date_from and date_to:
                domain = [
                    ('agent_id', '=', agent_id.id),
                    ('date_from', '=', date_from),
                    ('date_to', '=', date_to)
                ] 
                dd = expression.OR(
                    [
                       [('date_from', '>=', date_from),('date_from', '<=', date_to)],
                       [('date_to', '>=', date_from),('date_to', '<=', date_to)],
                       [('date_from', '<=', date_from),('date_to', '>=', date_to)]
                    ]
                )
                domain = expression.AND(
                    [
                        [('agent_id', '=', agent_id.id)],
                        dd
                    ]
                )
                results = self.search(domain)
                results = results.filtered(lambda x: x.id != record.id)
                action = self.env.ref('commercial_agent_plus.commercial_agent_settlement_action').id
                if results:
                    obj = _('invoces')
                    if record.commission_type == 'cashed':
                        obj = _('payments')
                    html = _("Following settlements for <b>%s</b> overlap this one: <br/>") % agent_id.name
                    
                    html += "<ul>"
                    for res in results:
                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        base_url += '/web#action=%d&id=%d&view_type=form&model=%s' % (action, res.id, res._name)            
                        html += """
                        <li>
                            <a href="%s">%s</a> [%s, %s]
                        </li>
                        """ % (base_url, res.display_name, res.date_from, res.date_to)
                    html += "</ul>"
                    if record.state == 'draft':
                        html += _("You can force looking for unsettled %s") % obj
                    
                    record.warning_msg = html
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('commercial.agent.settlement')
        return super(CommercialAgentPlusSettlement, self).create(vals)
    
    
    def force_settle(self):
        self.write({
            'forced': True,
            'forced_by': self.env.user.id
        })
        return self.settle()
    
    def settle(self):
        """
        Get commission from orders based on commission_type
        """
        for record in self:
            commission_orders = False
            if record.commission_type == 'invoiced':
                # find invoices
                invoices = self.env['account.invoice'].search([
                    ('state','=','posted'),
                    ('commercial_agent_id','=',record.agent_id.id),
                    ('invoice_date', '>=', record.date_from),
                    ('invoice_date', '<=', record.date_to),
                    ('settlement_id', '=', False),
                    ('type','=','out_invoice')
                ]) 
                add_invoices = [
                    (4, x.id, 0) for x in invoices if x.id not in record.invoice_ids.ids
                ]
                record.invoice_ids = add_invoices
                params = 'invoice_line_ids.sale_line_ids.order_id.commercial_agent_sale_commission_id'
                commission_orders = invoices.mapped(params)
            if record.commission_type == 'cashed':
                payments = self.env['account.payment'].search([
                    ('state', '=', 'posted'),
                    ('date', '>=', record.date_from),
                    ('date', '<=', record.date_to),
                    ('commercial_agent_id','=',record.agent_id.id),
                    ('settlement_id', '=', False)
                ])
                add_payments = [
                    (4, x.id, 0) for x in payments if x.id not in record.payment_ids.ids
                ] 
                record.payment_ids = add_payments
                params = 'reconciled_invoice_ids.invoice_line_ids.sale_line_ids.order_id.commercial_agent_sale_commission_id'
                commission_orders = payments.mapped(params)
            
            if commission_orders:
                # get commission orders with remaining_commission > 0   
                commission_orders = commission_orders.filtered(lambda r: r.remaining_commission > 0)
                
                add_comm_orders = [
                    (4, x.id, 0) for x in commission_orders if x.id not in record.commission_order_ids.ids
                ]
                record.commission_order_ids = add_comm_orders
            
                record._calculate_total_to_settle()
                record.write({
                    'state': 'settled'
                })
        
    def _calculate_total_to_settle(self):
        for record in self:    
            total = 0
            if record.commission_type == 'invoiced':
                for invoice in record.invoice_ids:
                    # get commission orders associated to invoice
                    line = record.commission_order_ids.filtered(
                        lambda x: invoice.id in x.sale_order_id.invoice_ids.ids
                    )
                    percentage = 0
                    if len(line) == 0:
                        continue
                    if invoice.amount_untaxed_signed > 0:
                        total_order = sum(line.mapped('total_order_amount'))
                        total_commission = sum(line.mapped('total_commission'))
                        percentage = (invoice.amount_untaxed_signed * 100) / total_order
                        to_sum = round((total_commission * percentage ) / 100, 2)
                        # to manage rounding
                        settlement_commission = 0
                        for l in line:
                            if l.remaining_commission >= to_sum:
                                settlement_commission += to_sum
                                l.paid_commission = l.paid_commission + to_sum
                                to_sum = 0
                            else:
                                settlement_commission += l.remaining_commission
                                l.paid_commission = l.paid_commission + l.remaining_commission
                                to_sum -= l.remaining_commission
                        invoice.settlement_commission = settlement_commission
                        total += settlement_commission
                            
            if record.commission_type == 'cashed':
                for payment in record.payment_ids:
                    payment_invoice = set(payment.reconciled_invoice_ids.ids)
                    line = record.commission_order_ids.filtered(
                        lambda x: len(payment_invoice.intersection(x.sale_order_id.invoice_ids.ids)) > 0
                    )
                    if len(line) == 0:
                        continue
                    percentage = 0
                    total_order = sum(line.mapped('total_order_amount_taxed'))
                    total_commission = sum(line.mapped('total_commission'))
                    percentage = (payment.amount * 100) / total_order  
                    to_sum = round((total_commission * percentage ) / 100, 2)
                    # to manage rounding
                    settlement_commission = 0
                    for l in line:
                        if l.remaining_commission >= to_sum:
                            settlement_commission += to_sum
                            l.paid_commission = l.paid_commission + to_sum
                            to_sum = 0
                        else:
                            settlement_commission += l.remaining_commission
                            l.paid_commission = l.paid_commission + l.remaining_commission
                            to_sum -= l.remaining_commission
                    payment.settlement_commission = settlement_commission
                    total += settlement_commission
            record.total_to_settle = total 
    
    @api.constrains('agent_invoice_id')
    def _constrains_agent_invoice_id(self):
        for record in self:
            if record.agent_invoice_id:
                record.state = 'invoiced'
    
    def get_reverse_payments(self):
        """
        Check if there are any reversed payments to be deducted
        from the total settled
        """
        for record in self:
            payments = self.env['account.payment'].search([
                ('agent_reverse', '=', True),
                ('agent_reversed', '=', False),
                ('commercial_agent_id','=', record.agent_id.id)
            ])
            if payments:
                record.write({
                    'reverse_payment_ids': [(6, 0, payments.ids)]
                })
                payments.write({
                    'agent_reversed': True
                })
    
    def get_reverse_invoices(self):
        """
        Check if there are any reversed invoices to be deducted
        from the total settled
        """
        for record in self:
            invoices = self.env['account.invoice'].search([
                ('agent_reverse', '=', True),
                ('agent_reversed', '=', False),
                ('commercial_agent_id', '=', record.agent_id.id),
                ('type','=','out_refund')
            ])
            if invoices:
                for invoice in invoices:
                    percentage = (invoice.amount_untaxed * 100) / invoice.reversed_entry_id.amount_total
                    invoice.settlement_commission = round((invoice.settlement_commission * percentage ) / 100, 2)
                record.write({
                    'reverse_invoice_ids': [(6, 0, invoices.ids)]
                })
                invoices.write({
                    'agent_reversed': True
                })
    
    @api.depends('commission_order_ids', 'invoice_ids', 'payment_ids')
    def _compute_total(self):
        for record in self:
            record.total_commission = sum(record.commission_order_ids.mapped('total_commission'))
            record.total_order_amount = sum(record.commission_order_ids.mapped('total_order_amount'))
            record.total_amount_untaxed_signed = sum(record.invoice_ids.mapped('amount_untaxed_signed'))
            
            subtract = 0
            for line in record.sudo().reverse_payment_ids:
                subtract -= line.settlement_commission
            for line in record.sudo().reverse_invoice_ids:
                subtract -= line.settlement_commission
            record.total_to_subtract = subtract
            record.total_settle = record.total_to_settle + record.total_to_subtract