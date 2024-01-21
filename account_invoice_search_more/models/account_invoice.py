# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    product_id = fields.Many2one(
        'product.product',
        related='invoice_line_ids.product_id',
        string='Product')
    account_line_id = fields.Many2one(
        'account.account',
        related='invoice_line_ids.account_id',
        string='Line Account')
