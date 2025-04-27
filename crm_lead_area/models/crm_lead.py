# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmLead(models.Model):

    _inherit = "crm.lead"

    area_id = fields.Many2one("res.partner.area", "Area")
