# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from .record_rules_plus import agent_group, agent_manager, agent_all

class CommercialAgentPlusProductTemplate(models.Model):
    _inherit = "product.template"
    
    commercial_agent_salable = fields.Boolean(
        string="Salable by agent",
        default=False,
        tracking=True
    )
    commercial_agent_commission_free = fields.Boolean(
        string="Commission Free",
        default=False,
        tracking=True
    )
    product_commission_ids = fields.One2many(
        string="Commissions",
        comodel_name="product.commission",
        inverse_name="product_tmpl_id"
    )
    qty_available = fields.Float(compute_sudo=True)
    virtual_available = fields.Float(compute_sudo=True)
    
    @api.constrains('commercial_agent_salable', 'commercial_agent_commission_free')
    def _constrains_agent_fields(self):
        for record in self:
            if record.product_variant_ids:
                record.product_variant_ids.write({
                    'commercial_agent_salable': record.commercial_agent_salable,
                    'commercial_agent_commission_free': record.commercial_agent_commission_free,
                })
                    
            if record.product_variant_id:
                record.product_variant_id.write({
                    'commercial_agent_salable': record.commercial_agent_salable,
                    'commercial_agent_commission_free': record.commercial_agent_commission_free,
                })
    
    @api.constrains('product_commission_ids')
    def _constrains_product_commission_ids(self):
        for record in self:
            for line in record.product_variant_ids:
                line.product_commission_ids.write({
                    'active': False
                })
                line.product_commission_ids = [
                    (0,0, {
                        'commission_type': x.commission_type,
                        'commission': x.commission,
                        'date_start': x.date_start,
                        'date_end': x.date_end
                    }) for x in record.product_commission_ids
                ]
            if record.product_variant_id:
                record.product_variant_id.product_commission_ids.write({
                    'active': False
                })
                record.product_variant_id.product_commission_ids = [
                    (0,0, {
                        'commission_type': x.commission_type,
                        'commission': x.commission,
                        'date_start': x.date_start,
                        'date_end': x.date_end
                    }) for x in record.product_commission_ids
                ]
    
    def no_action(self):
        pass

    @api.model
    def create(self, vals):
        product = super(CommercialAgentPlusProductTemplate, self).create(vals)
        attrs = {
            'commercial_agent_salable': product.commercial_agent_salable,
            'commercial_agent_commission_free': product.commercial_agent_commission_free
        }
        if product.product_commission_ids:
            attrs['product_commission_ids'] = [(6, 0, product.product_commission_ids.ids)]
        for variant in product.product_variant_ids:
            variant.write(attrs)
        return product

class CommercialAgentPlusProductProduct(models.Model):
    _inherit = "product.product"
    
    commercial_agent_salable = fields.Boolean(
        string="Salable by agent",
        default=False,
        tracking=True
    )
    commercial_agent_commission_free = fields.Boolean(
        string="Commission Free",
        default=False,
        tracking=True
    )
    product_commission_ids = fields.One2many(
        string="Commissions",
        comodel_name="product.commission",
        inverse_name="product_id"
    )
    
   
    
