# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.depends('invoice_line_ids')
    def _with_espresso(self):
        for inv in self:
            if inv.state != 'draft' or not inv.invoice_line_ids:
                continue
            espresso = False
            for line in inv.invoice_line_ids:
                if line.espresso:
                    espresso = True
                    break
            inv.espresso = espresso

    espresso = fields.Boolean(
        string="Documento con prodotti espresso",
        compute="_with_espresso",
        store=True,
    )


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    espresso = fields.Boolean(
        string="Prodotto espresso",
        related="product_id.espresso",
    )
