# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_grade = fields.Selection(
        [('bronze', 'Bronze Partner'),
         ('silver', 'Silver Partner'),
         ('gold', 'Gold Partner')], 'Partner Grade',
        default='')

    end_user = fields.Boolean('End User')
    assigned_reseller = fields.Many2one(
        'res.partner', string='Assigned Reseller')
