# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    def _get_default_delta(self):
        return 1.0

    rebate_active = fields.Many2one(
        "account.account",
        string="Abbuono attivo",
        domain=[("nature", "in", ["C", "R"])],
    )

    rebate_passive = fields.Many2one(
        "account.account",
        string="Abbuono passivo",
        domain=[("nature", "in", ["R", "C"])],
    )

    rebate_delta = fields.Float(
        string="Delta abbuono",
        default=_get_default_delta,
    )
