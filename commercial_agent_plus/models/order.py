# -*- coding: utf-8 -*-
from locale import currency
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from .record_rules_plus import agent_group, agent_manager, agent_all


class CommercialAgentPlusSaleOrder(models.Model):
    _inherit = "sale.order"
    
    state = fields.Selection(selection_add=[
        ('waiting', _('Waiting Commission'))])
    
    def _commercial_agents_domain(self):
        """
        get users who are part of the agent_group or agent_manager group
        """
        if self._check_if_agent():
            agents = self._get_agents_params()
            return [('id','in',agents)]
        return [
            ('groups_id', 'in', 
            [self.env.ref(agent_group).id,
            self.env.ref(agent_manager).id])
        ] 
    
    def _default_commercial_agent(self):
        """
        When sale.order is created add current agent.
        """
        if self.env.user.has_group(agent_group):
            return self.env.user.id
        return False
    
    # domain: get users who are part of the commercial agent groups
    commercial_agent_id = fields.Many2one(
        string='Commercial Agent',
        comodel_name="res.users",
        domain=_commercial_agents_domain,
        default=_default_commercial_agent    
    )
    
    # related to the commissions container
    commercial_agent_sale_commission_id = fields.Many2one(
        string="Commission Order",
        comodel_name="commercial.agent.sale.commission",
        compute="_get_commission_order"
    )
    
    # field for the agents: get data from invoices, payments and shipping
    # because agent can't access invoice,payment,shipping models
    agent_msg = fields.Html(
        string="Message",
        compute="_compute_agent_message"
    )
    
    @api.constrains('state')
    def _constrains_state(self):
        """
        An agent can change state field only if there is "allow_agent" = True
        in context 
        """
        if self._check_if_agent() and not self.env.context.get('allow_agent'):
            raise ValidationError(
                _("Sorry! You are not allowed to change order state"))
            
    def agent_confirm_order(self):
        """
        Change order state to 'waiting' (only for agents)
        """
        for record in self:
            if record.state not in ['done', 'sale', 'cancel']:
                record.with_context({'allow_agent': True}).state = 'waiting'
    
    def action_quotation_sent(self):
        for order in self:
            order.message_subscribe(partner_ids=order.partner_id.ids)
        self.write({'state': 'sent'})
    
    def _get_commission_order(self):
        for order in self:
            order.commercial_agent_sale_commission_id = False
            res = self.env['commercial.agent.sale.commission'].search([
                ('sale_order_id','=',order.id)
            ])
            if res:
               order.commercial_agent_sale_commission_id = res[0].id 
    
    def action_confirm(self):
        for order in self:
            if order.commercial_agent_id:
                order.calculate_commission()
        return super(CommercialAgentPlusSaleOrder, self).action_confirm()
        
    def calculate_commission(self):
        """
        Calculate or Recalculate potential commissions from current order.
        
        Generate a Commission Order (commercial.agent.sale.commission) linked
        to current sale.order.
        """
        for order in self:
            commission_order = order.commercial_agent_sale_commission_id
            # calculate only if there's an agent
            if order.commercial_agent_id and not commission_order:
                # create the commission order
                attrs = {
                    'sale_order_id': order.id
                }
                commission_order = self.env[
                    'commercial.agent.sale.commission'].create(attrs)
            
            for line in order.order_line:
                if line.product_id:
                    # create single commission line and link it
                    # to the commission
                    # order created before.
                    line_attrs = {
                        'sale_order_line_id': line.id,
                        'order_commission_id': commission_order.id
                    }
                    caslc = self.env['commercial.agent.sale.line.commission']
                    commission_line = (
                        line.commercial_agent_sale_line_commission_id)
                    if not commission_line:
                        commission_line = caslc.create(line_attrs)
                    # calculcate single commission
                    commission_line.calculate_commission()
                
    def _compute_agent_message(self):
        lang = self.env.context.get('lang')
        lang_objs = False
        if lang:
            lang_objs = self.env['res.lang'].search([('code', '=', lang)])
        for record in self:
            msg = ""
            invoices = record.sudo().invoice_ids
            pickings = record.sudo().picking_ids
            if invoices:
                msg += _("<b>INVOICES</b><br/><br/>")
                msg += '<table class="table table-sm table-hover table-striped">'
                for invoice in invoices:
                    amount = invoice.amount_untaxed_signed
                    date = invoice.date
                    if lang_objs:
                        amount = lang_objs[0].format(
                            '%.' + str(2) + 'f', amount,
                            grouping=True, monetary=True)
                        currency_obj = invoice.currency_id
                        if currency_obj and currency_obj.symbol:
                            if currency_obj.position == 'after':
                                amount = '%s %s' % (amount, currency_obj.symbol)
                            elif currency_obj and currency_obj.position == 'before':
                                amount = '%s %s' % (currency_obj.symbol, amount)
                        date = date.strftime(lang_objs[0].date_format)
                    msg += '<tr>'
                    msg += "<td class='col-3'><b>%s</b></td><td class='col-3'>%s</td><td class='col-2'>%s</td><td class='col-2'><b>%s</b></td>" % (
                        invoice.name,
                        date,
                        amount,
                        dict(invoice._fields['state']._description_selection(self.env)).get(invoice.state),
                    )
                    msg += '</tr>'
                msg += '</tbody></table>'
            if pickings:
                msg += _("<b>PICKINGS</b><br/><br/>")
                msg += '<table class="table table-sm table-hover table-striped">'
                for pick in pickings:
                    scheduled = pick.scheduled_date
                    date_done = pick.date_done
                    if lang_objs:
                        scheduled = scheduled.strftime(lang_objs[0].date_format)
                        if date_done:
                            date_done = date_done.strftime(lang_objs[0].date_format)
                    msg += '<tr>'
                    msg += "<td class='col-3'><b>%s</b></td><td class='col-3'>%s</td><td class='col-2'>%s</td><td class='col-2'><b>%s</b></td><td class='col-2'><b>%s</b></td>" % (
                        pick.name,
                        scheduled,
                        date_done,
                        '',
                        dict(pick._fields['state']._description_selection(self.env)).get(pick.state),
                    )
                    msg += '</tr>'
                msg += '</tbody></table>'
            record.agent_msg = msg


class CommercialAgentPlusSaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('state')
    def _compute_product_uom_readonly(self):
        for line in self:
            line.product_uom_readonly = line.state in ['sale', 'done', 'cancel']

    # related to the commissions container line
    commercial_agent_sale_line_commission_id = fields.Many2one(
        string="Commission Order Line",
        comodel_name="commercial.agent.sale.line.commission",
        compute="_get_commission_order_line"
    )

    product_uom_readonly = fields.Boolean(
        compute='_compute_product_uom_readonly')

    product_uom = fields.Many2one(
        'uom.uom', string='Unit of Measure',
        domain="[('category_id', '=', product_id.uom_id.category_id)]"
    )

    product_template_id = fields.Many2one(
        'product.template', string='Product Template',
        related="product_id.product_tmpl_id", domain=[('sale_ok', '=', True)])

    def _get_commission_order_line(self):
        for line in self:
            line.commercial_agent_sale_line_commission_id = False
            res = self.env['commercial.agent.sale.line.commission'].search([
                ('sale_order_line_id','=',line.id)
            ])
            if res:
                line.commercial_agent_sale_line_commission_id = res[0].id


class SaleReport(models.Model):
    _inherit = "sale.report"

    commercial_agent_id = fields.Many2one(
        string='Commercial Agent',
        comodel_name="res.users"  
    )
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['commercial_agent_id'] = ", s.commercial_agent_id as commercial_agent_id"
        groupby += ', s.commercial_agent_id'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
