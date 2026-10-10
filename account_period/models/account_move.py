# -*- coding: utf-8 -*-
# Copyright 2017 Jarvis (www.odoomod.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    period_id = fields.Many2one(
        "account.period",
        "Period",
        required=False,
        states={"posted": [("readonly", True)]},
    )


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    period_id = fields.Many2one(
        "account.period",
        string="Period",
        related="move_id.period_id",
        required=False,
        index=True,
        store=True,
    )
