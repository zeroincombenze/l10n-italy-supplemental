# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, _


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    end_user_id = fields.Many2one(
        'res.partner', string='End user',
        index=True)
    ref_user_id = fields.Many2one(
        'res.partner', string='Reference user')