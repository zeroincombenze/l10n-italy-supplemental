# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    crm_phonecall_ids = fields.One2many(
        'crm.phonecall', 'id', string='Phones')
