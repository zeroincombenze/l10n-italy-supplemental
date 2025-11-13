# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    rc_fiscal_document_type_id = fields.Many2one(
        "italy.ade.invoice.type",
        string="Self Invoice Fiscal Document Type",
    )
