# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountConfigSettings(models.TransientModel):
    _inherit = "account.config.settings"

    invoice_mail_template_id = fields.Many2one(
        related="company_id.invoice_mail_template_id",
        string="Invoice Mail Template",
        help="Mail template to use in order to send Invice pdf",
    )
    to_send_mail = fields.Boolean(
        string="To send mail",
        help="Default automatically send invoice mail",
    )

    @api.onchange("company_id")
    def onchange_company_id(self):
        res = super(AccountConfigSettings, self).onchange_company_id()
        if self.company_id:
            company = self.company_id
            self.invoice_mail_template_id = (
                company.invoice_mail_template_id
                and company.invoice_mail_template_id.id
                or False
            )
        else:
            self.invoice_mail_template_id = False
        return res

    @api.model
    def get_default_to_send_mail(self, fields):
        return {
            "to_send_mail": self.env["ir.config_parameter"].sudo().get_param(
                "default_to_send_mail")
        }

    @api.multi
    def set_to_send_mail(self):
        self.ensure_one()
        ICP = self.env["ir.config_parameter"]
        ICP.set_param("default_to_send_mail", self.to_send_mail)
