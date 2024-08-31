# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    invoice_mail_template_id = fields.Many2one(
        "mail.template",
        "Invoice Mail Template",
        domain=lambda self: [
            ("model_id", "=", self.env.ref("account.model_account_invoice").id)],
        default=lambda self: self.env.ref("account.email_template_edi_invoice").id,
        help="Mail template to use in order to send Invice pdf",
    )
