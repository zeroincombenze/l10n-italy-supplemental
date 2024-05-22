# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class BaseConfigSettings(models.TransientModel):
    _inherit = "base.config.settings"

    microsoft_outlook_client_identifier = fields.Char(
        "Outlook Client Id", config_parameter="microsoft_outlook_client_id"
    )
    microsoft_outlook_client_secret = fields.Char(
        "Outlook Client Secret", config_parameter="microsoft_outlook_client_secret"
    )

    @api.model
    def get_default_all(self, fields):
        Config = self.env["ir.config_parameter"]
        return {
            "microsoft_outlook_client_identifier":
                Config.get_param("microsoft_outlook_client_id", default=None),
            "microsoft_outlook_client_secret":
                Config.get_param("microsoft_outlook_client_secret", default=None),
        }

    @api.multi
    def set_client_identifier_n_secret(self):
        Config = self.env["ir.config_parameter"]
        for record in self:
            Config.set_param("microsoft_outlook_client_id",
                             record.microsoft_outlook_client_identifier or "")
            Config.set_param("microsoft_outlook_client_secret",
                             record.microsoft_outlook_client_secret or "")
