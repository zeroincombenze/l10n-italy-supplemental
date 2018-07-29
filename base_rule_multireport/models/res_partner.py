# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
#                Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    preferred_invoice_model_id = fields.Many2one(
        'account.invoice.reportname',
        'Preferred report',
        help="Specific customer invoice model")
