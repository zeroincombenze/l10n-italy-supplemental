# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountRCType(models.Model):
    _inherit = "account.rc.type"

    fiscal_document_type_id = fields.Many2one(
        "italy.ade.invoice.type",
        string="Fiscal Document Type",
        oldname="invoice_type_id",
        help="To be used when sending self invoices to the exchange system"
    )
