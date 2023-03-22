# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from .record_rules_plus import agent_group, agent_manager, agent_all

class CommercialAgentPlusArea(models.Model):
    _name = "commercial.agent.area"
    _inherit = ['mail.thread']
    _description = "Commercial Area"
    
    active = fields.Boolean(
        string="Active",
        default=True
    )
    name = fields.Char(string="Name", tracking=True)
    description = fields.Text(string="Description", tracking=True)
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True, 
        default=lambda self: self.env.user.company_id
    )