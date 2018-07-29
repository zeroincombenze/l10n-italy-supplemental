# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class CrmPhonecall(models.Model):
    _inherit = 'crm.phonecall'

    crm_lead_id = fields.Many2one(
        'crm.lead', string='Leads/Opportunity')
