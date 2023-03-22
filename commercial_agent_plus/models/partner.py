# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from .record_rules_plus import agent_group, agent_manager, agent_all

class CommercialAgentPlusResPartner(models.Model):
    _inherit = "res.partner"
    
    def _default_commercial_agent(self):
        """
        When res.partner is created add current agent.
        """
        if self.env.user.has_group(agent_group) \
        and self.env.user.id not in self.user_ids.ids:
            return [(4, self.env.user.id, 0)]
        return False

    user_id = fields.Many2one(default=lambda self: self.env.user.id)
    
    commercial_agent_ids = fields.Many2many(
        string='Commercial Agents',
        comodel_name="res.users",
        default=_default_commercial_agent   
    )
    # AGENT FIELDS
    commercial_agent = fields.Boolean(
        string="Is Agent?",
        default=False,
        compute="_compute_is_agent",
        search="_search_agents",
        tracking=True
    )
    commercial_agent_area_manager = fields.Boolean(
        string="Is Manager?",
        default=False,
        compute="_compute_is_agent",
        tracking=True
    )
    commercial_agent_manager_id = fields.Many2one(
        string="Manager",
        comodel_name="res.users",
    )
    commercial_agent_commission_type = fields.Selection(
        string="Commission Type",
        selection = [
            ('invoiced', _('Invoiced')),
            ('cashed', _('Cashed'))
        ]
    )
    # commercial_agent_area_ids used for both agent and customer areas
    # logic depends on commercial_agent field
    commercial_agent_area_ids = fields.Many2many(
        string="Areas",
        comodel_name="commercial.agent.area"
    )
    
    commercial_agent_commission_ids = fields.One2many(
        string="Commissions",
        comodel_name="commercial.agent.commission",
        inverse_name="agent_id"
    )
    
    def _compute_is_agent(self):
        for record in self:
            record.commercial_agent = False
            record.commercial_agent_area_manager = False
            for user in record.user_ids:
                if user.has_group(agent_group):
                    record.commercial_agent = True
                if user.has_group(agent_manager):
                    record.commercial_agent_area_manager = True 
    
    def _search_agents(self, operator, value):
        agent = self.env.ref(agent_group).id
        domain = [('user_ids.groups_id', operator, agent)]
        return domain    

    def go_to_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'target': 'current',
            'domain': [('partner_id', 'in', self.ids)]
        }
        
class CommercialAgentPlusResUsers(models.Model):
    _inherit = "res.users"
    
    commercial_agent_employee_ids = fields.One2many(
        string="Own Employees",
        comodel_name="res.users",
        inverse_name="commercial_agent_manager_id"
    )
    
    def name_get(self):
        show_agent = self.env.context.get('show_agent')
        if not show_agent:
            return super(CommercialAgentPlusResUsers, self).name_get()
        names = []
        for record in self:
            name = record.name
            if record.has_group(agent_manager):
                name += _(' (Manager)')
            else:
                if record.has_group(agent_group):
                    name += _(' (Agent)')
            names.append((record.id, name))
        return names
     
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """
        name_search for searching only manager or manager and agent based on context
        context must be: 
            show_agent: show both agent and manager
            only_manager: show only manager
        for only manager you should use both variables.
        """
        show_agent = self.env.context.get('show_agent')
        only_manager = self.env.context.get('only_manager')
        if not show_agent and not only_manager:
            return super(CommercialAgentPlusResUsers, self).name_search(
                name=name,
                args=args,
                operator=operator,
                limit=limit)
        new_domain = [('groups_id', 'in', [
            self.env.ref(agent_group).id,
            self.env.ref(agent_manager).id,
            ]
        )] 
        if only_manager:
            new_domain = [('groups_id', '=', self.env.ref(agent_manager).id)]
        args = expression.AND([
            args,
            new_domain
        ])
        records = self.search(args, limit=limit)
        return records.name_get()