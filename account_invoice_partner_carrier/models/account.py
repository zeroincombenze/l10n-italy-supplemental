# -*- coding: utf-8 -*-
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    partner_carrier_id = fields.Many2one(
        "res.partner",
        string="Carrier",
        oldname="carrier_id",
    )
