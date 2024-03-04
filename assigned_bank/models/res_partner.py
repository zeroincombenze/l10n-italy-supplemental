# -*- coding: utf-8 -*-
#
# Copyright 2019-24 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    assigned_bank = fields.Many2one(
        "res.partner.bank",
        string="Assigned Bank",
        domain=lambda self: [
            ("partner_id", "=", self.env.user.company_id.partner_id.id)
        ],
    )
