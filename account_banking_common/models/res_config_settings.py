# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    rebate_active = fields.Many2one(
        related="company_id.rebate_active",
        string="Abbuono attivo",
        readonly=False,
    )

    rebate_passive = fields.Many2one(
        related="company_id.rebate_passive",
        string="Abbuono passivo",
        readonly=False,
    )

    rebate_delta = fields.Float(
        related="company_id.rebate_delta",
        string="Delta abbuono",
        readonly=False,
    )
