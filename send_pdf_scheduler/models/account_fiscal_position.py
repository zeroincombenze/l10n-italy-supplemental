# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    to_send_mail = fields.Selection(
        [("enable", "Send by cron"), ("disable", "Avoid sending by cron")],
        string="Schedule sending document pdf mail",
        help="Automatically send invoice mail",
    )
