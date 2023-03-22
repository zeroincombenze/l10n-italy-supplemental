# -*- coding: utf-8 -*-
from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from .record_rules_plus import agent_group, agent_manager, agent_all

COMMISSION_TYPE_ORDER = [
        'product_customer', 
        'product', 
        'product_category', 
        'customer',
        'pricelist', 
        'area', 
        'default_product', 
        'default_agent'
]


class CommercialAgentPlusCommission(models.Model):
    _name = "commercial.agent.commission"
    _inherit = ['mail.thread']
    _description = "Agent Commission"
    
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True
    )
    commission_type = fields.Selection(
        string="Type",
        selection=[
            ('product_customer', _('Product + Customer')),
            ('product', _('Product')),
            ('product_category', _('Product Category')),
            ('customer', _('Customer')),
            ('pricelist', _('Price List')),
            ('area', _('Area')),
            ('default_agent', _('Default Agent'))
        ],
        tracking=True
    )
    agent_id = fields.Many2one(
        string="Agent",
        comodel_name="res.partner",
        tracking=True
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        domain=[('commercial_agent_salable', '=', True)],
        tracking=True
    )
    product_category = fields.Many2one(
        string="Product Category",
        comodel_name='product.category',
        tracking=True
    )
    customer_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        tracking=True
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        tracking=True
    )
    area_id = fields.Many2one(
        string="Area",
        comodel_name="commercial.agent.area",
        tracking=True
    )
    commission = fields.Float(
        string="Commission %",
        default=0,
        tracking=True
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="agent_id.company_id"
    )
    date_start = fields.Date(
        string="Date Start",
        tracking=True
    )
    date_end = fields.Date(
        string="Date End",
        tracking=True
    )
    
    @api.onchange('commission_type', 'agent_id')
    def _onchange_commission_type(self):
        """
        Used for set the customer domain based on default_agent_id
        passed on context
        """
        if self.env.context.get('default_agent_id', False):
            self.with_context({'standard_write': True}).write(
                {
                    'agent_id': self.env.context.get('default_agent_id'),
                    'product_id': False,
                    'product_category': False,
                    'customer_id': False,
                    'pricelist_id': False,
                    'area_id': False
                }
            )
            return {
                'domain': {'customer_id': [
                    ('commercial_agent_ids', 'in', self.agent_id.user_ids.ids)
                    ]}
            }
    
    def name_get(self):
        result = []
        for line in self:
            name = '%s - %s' % (
                line.agent_id.name,
                line.commission_type
            )
            result.append((line.id, name))
        return result
    
    def write(self, vals):
        """
        Perserve the historical
        """
        if 'active' in vals:
            return super(CommercialAgentPlusCommission, self).write(vals)
        if self.env.context.get('standard_write'):
            return super(CommercialAgentPlusCommission, self).write(vals)
        for record in self:
            record.copy(vals)
            record.with_context({'standard_write': True}).active = False


class CommercialAgentProductCommission(models.Model):
    _name = "product.commission"
    _inherit = ['mail.thread']
    _description = "Agent Commission"
    
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True
    )
    commission_type = fields.Selection(
        string="Type",
        selection=[
            ('default_product', _('Default Product')),
        ],
        tracking=True,
        default="default_product"
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        tracking=True
    )
    product_tmpl_id = fields.Many2one(
        string="Product Template",
        comodel_name="product.template",
        tracking=True
    )
    commission = fields.Float(
        string="Commission %",
        default=0,
        tracking=True
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="product_id.company_id"
    )
    date_start = fields.Date(
        string="Date Start",
        tracking=True
    )
    date_end = fields.Date(
        string="Date End",
        tracking=True
    )
    
    def name_get(self):
        result = []
        for line in self:
            name = '%s - %s' % (
                line.product_id.name,
                line.commission_type
            )
            result.append((line.id, name))
        return result
    
    def write(self, vals):
        """
        Perserve the historical
        """
        if 'active' in vals:
            return super(CommercialAgentProductCommission, self).write(vals)
        if self.env.context.get('standard_write'):
            return super(CommercialAgentProductCommission, self).write(vals)
        for record in self:
            record.copy(vals)
            record.with_context({'standard_write': True}).active = False


class CommercialAgentPlusOrderCommission(models.Model):
    _name = "commercial.agent.sale.commission"
    _inherit = ['mail.thread']
    _description = "Commission Order"
    
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True
    )
    sale_order_id = fields.Many2one(
        string="Sale Order",
        comodel_name="sale.order",
        tracking=True
    )
    agent_id = fields.Many2one(
        string="Agent",
        comodel_name="res.users",
        related="sale_order_id.commercial_agent_id"
    )
    date_order = fields.Datetime(
        string="Order Date",
        related="sale_order_id.date_order"
    )
    commission_lines = fields.One2many(
        string="Commission Lines",
        comodel_name="commercial.agent.sale.line.commission",
        inverse_name="order_commission_id"
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True, 
        related="sale_order_id.company_id"
    )
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency', 
        related="sale_order_id.currency_id"
    )
    total_commission = fields.Monetary(
        string="Total Commission",
        currency_field='currency_id',
        compute="_compute_commission"
    )
    paid_commission = fields.Monetary(
        string="Paid Commission",
        currency_field='currency_id'
    )
    remaining_commission = fields.Monetary(
        string="Remaining Commission",
        currency_field='currency_id',
        compute="_compute_commission"
    )
    total_order_amount = fields.Monetary(
        string="Total Amount",
        currency_field='currency_id',
        compute="_compute_commission"
    )
    total_order_amount_taxed = fields.Monetary(
        string="Total Amount Taxed",
        currency_field='currency_id',
        compute="_compute_commission"
    )
    
    def name_get(self):
        result = []
        for order in self:
            name = '%s - %s' % (order.sale_order_id.name, order.agent_id.name)
            result.append((order.id, name))
        return result
    
    @api.depends('commission_lines')
    def _compute_commission(self):
        for record in self:
            record.total_commission = sum(record.commission_lines.mapped('commission_value'))
            record.remaining_commission = record.total_commission - record.paid_commission 
            record.total_order_amount = record.sale_order_id.amount_untaxed
            record.total_order_amount_taxed = record.sale_order_id.amount_total


class CommercialAgentPlusOrderLineCommission(models.Model):
    _name = "commercial.agent.sale.line.commission"
    _inherit = ['mail.thread']
    _description = "Commission order line"
    
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True
    )
    sale_order_line_id = fields.Many2one(
        string="Sale Order Line",
        comodel_name="sale.order.line",
        tracking=True
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True, 
        related="order_commission_id.company_id"
    )
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency', 
        related="sale_order_line_id.currency_id")
    commission_value = fields.Monetary(
        string="Commission",
        currency_field='currency_id',
        tracking=True
    )
    commission_percentage = fields.Float(
        string="Commission %",
        default=0,
        tracking=True
    )
    line_amount = fields.Monetary(
        string="Amount",
        related='sale_order_line_id.price_subtotal'
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        related='sale_order_line_id.product_id'
    )
    commission_type = fields.Selection(
        string="Type",
        selection=[
            ('product_customer', _('Product + Customer')),
            ('product', _('Product')),
            ('product_category', _('Product Category')),
            ('customer', _('Customer')),
            ('pricelist', _('Price List')),
            ('area', _('Area')),
            ('default_product', _('Default Product')),
            ('default_agent', _('Default Agent')),
            ('free', _('Free')),
            ('manual', _('Manual'))
        ],
        tracking=True
    )
    order_commission_id = fields.Many2one(
        string="Order Commission",
        comodel_name="commercial.agent.sale.commission",
        tracking=True
    )
    commercial_agent_commission_id = fields.Many2one(
        string="Commission line",
        comodel_name="commercial.agent.commission"
    )
    
    def write(self, vals):
        if 'commission_value' in vals.keys() and 'commission_type' not in vals.keys():
            for record in self:
                if record.commission_value != vals.get('commission_value'):
                    record.commission_type = 'manual'
        return super(CommercialAgentPlusOrderLineCommission, self).write(vals)
    
    @api.onchange('commission_percentage')
    def _onchange_commission_percentage(self):
        for record in self:
            if record.order_commission_id.remaining_commission <=0:
                continue
            if self.env.context.get('changed', False):
                continue
            record.commission_type = 'manual'
            record.with_context({'changed':True}).commission_value = (record.line_amount * record.commission_percentage) / 100
    
    @api.onchange('commission_value')
    def _onchange_commission_value(self):
        for record in self:
            if record.order_commission_id.remaining_commission <=0:
                continue
            if self.env.context.get('changed', False):
                continue
            record.commission_type = 'manual'
            record.with_context({'changed':True}).commission_percentage = (record.commission_value * 100) / record.line_amount    
    
    def _get_commission_filtered(self, commissions, commission_type):
        """
        Find the commission from the agent's
        
        commissions: agent commission lines
        commisstion_type: string representing the type of commission. Must be in  
                          COMMISSION_TYPE_ORDER variable
        
        return commission line or False. 
                          
        Override is possible: add new type of commission.
        """
        self.ensure_one()
        if commission_type not in COMMISSION_TYPE_ORDER:
            return False
        # filter by date
        today = self.order_commission_id.date_order.date()
        commissions = commissions.filtered(
            lambda x: x.date_start <= today and x.date_end >= today
        )
       
        commission = False
        if commission_type == 'product_customer':
            commission = commissions.filtered(
                lambda x: x.product_id.id == self.product_id.id and \
                          x.customer_id.id == self.sale_order_line_id.order_partner_id.id and \
                          x.commission_type == 'product_customer'
            )
        if commission_type == 'product':
            commission = commissions.filtered(
                lambda x: x.commission_type == 'product' and \
                          x.product_id.id == self.product_id.id
            )
        if commission_type == 'product_category':
            commission = commissions.filtered(
                lambda x: x.commission_type == 'product_category' and \
                          x.product_category.id == self.product_id.categ_id.id
            )
        if commission_type == 'customer':
            commission = commissions.filtered(
                lambda x: x.commission_type == 'customer' and \
                          x.customer_id.id == self.sale_order_line_id.order_partner_id.id
            )
        if commission_type == 'pricelist':
            commission = commissions.filtered(
                lambda x: x.commission_type == 'pricelist' and \
                          x.pricelist_id.id == self.order_commission_id.sale_order_id.pricelist_id.id
            )
        if commission_type == 'area':
            commission = commissions.filtered(
                lambda x: x.commission_type == 'customer' and \
                          x.area_id.id in self.sale_order_line_id.order_partner_id.commercial_agent_area_ids.ids
            )
        if commission_type == 'default_agent':
            commission = commissions.filtered(
                lambda x: x.commission_type == 'default_agent' and \
                          x.agent_id.id == self.order_commission_id.agent_id.partner_id.id
            )
        if commission_type == 'default_product':
            def_product = self.product_id.product_commission_ids.filtered(
                lambda x: x.commission_type == 'default_product' and \
                          x.date_start <= today and x.date_end >= today
            )
            if def_product:
                self.write({
                    'commission_type': 'default_product',
                    'commission_percentage': def_product[0].commission,
                    'commission_value': (self.line_amount * def_product[0].commission) / 100,
                    'commercial_agent_commission_id': False
                })
                return True
            
        if not commission:
            self.write({
                'commission_type': 'free',
                'commission_percentage': 0,
                'commission_value': 0,
                'commercial_agent_commission_id': False
            })
            return False
        # return only one commission
        return commission[0]
    
    def calculate_commission(self, commission_type_order=COMMISSION_TYPE_ORDER):
        """
        Calculate commission for the sale order.
        
        The order to searching commission is in COMMISSION_TYPE_ORDER .
        Commission type in COMMISSION_TYPE_ORDER must be all in self.commission_type
        field.
        
        Override is possible changing COMMISSION_TYPE_ORDER and self.commission_type 
        selection field.
        """
        for record in self:
            if record.product_id and record.product_id.commercial_agent_commission_free:
                record.write({
                    'commission_type': 'free',
                    'commission_percentage': 0,
                    'commission_value': 0,
                    'commercial_agent_commission_id': False
                })
                continue
            if record.order_commission_id and record.order_commission_id.agent_id \
            and record.order_commission_id.agent_id.partner_id:
                agent = record.order_commission_id.agent_id.partner_id
                # get all agent commission
                commissions = agent.commercial_agent_commission_ids
                commission = False
                for commission_type in commission_type_order:
                    commission = record._get_commission_filtered(commissions, commission_type)
                    if commission:
                        break
                if isinstance(commission, (int, float)):
                    if commission:
                        continue
                if commission:
                    record.write({
                        'commission_type': commission_type,
                        'commission_percentage': commission.commission,
                        'commission_value': (record.line_amount * commission.commission) / 100,
                        'commercial_agent_commission_id': commission.id
                    })
                
