#
# Copyright 2019-23 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    conai_exemption_id = fields.Many2one(
        "italy.conai.partner.category", string="CONAI Category"
    )
