#
# Copyright 2020-24 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_assigned_bank_id = fields.Many2one(
        "res.partner.bank",
        string="Assigned Bank for Payment",
        config_parameter="res.partner.assigned_bank_id",
        domain=lambda self: [
            ("partner_id", "=", self.env.user.company_id.partner_id.id)
        ],
    )
    partner_assigned_income_bank_id = fields.Many2one(
        "res.partner.bank",
        string="Assigned Bank for Incoming",
        config_parameter="res.partner.assigned_income_bank_id",
        domain=lambda self: [
            ("partner_id", "=", self.env.user.company_id.partner_id.id)
        ],
    )

    def _assigned_bank_get(self):
        entity_type = self.env["res.partner.bank"]
        tmp_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("res.partner.assigned_bank_id")
            or "0"
        )
        return entity_type.browse(int(tmp_id))

    def _assigned_income_bank_get(self):
        entity_type = self.env["res.partner.bank"]
        tmp_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("res.partner.assigned_income_bank_id")
            or "0"
        )
        return entity_type.browse(int(tmp_id))
