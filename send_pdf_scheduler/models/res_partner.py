# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    to_send_mail = fields.Selection(
        [("enable", "Send by cron"), ("disable", "Avoid sending by cron")],
        string="Schedule sending document pdf mail",
        help="Automatically send invoice mail",
    )
