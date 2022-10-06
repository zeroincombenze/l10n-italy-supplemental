# -*- coding: utf-8 -*-
# Copyright (C) 2014 Rooms For Limited T/A OSCG <https://www.odoo-asia.com>
# Copyright (C) 2016-22 SHS-AV s.r.l. <https://zeroincombenze.it>
#
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    # _order = 'id desc'

    @api.depends('quantity')
    def _compute_quantity(self):
        for ln in self:
            ln.quantity_signed = (
                ln.quantity if "refund" not in ln.invoice_id.type else -ln.quantity
            )

    date_invoice = fields.Date(related='account.invoice.date_invoice',
                               string='Invoice Date')
    number = fields.Char(related='invoice_id.number', string=u'Number')
    date_invoice = fields.Date(related='invoice_id.date_invoice',
                               string=u'Invoice Date', store=True)
    state = fields.Selection(related='invoice_id.state',
                             string=u'Status', store=True)
    type = fields.Selection(related='invoice_id.type',
                             string=u'Type', store=True)
    quantity_signed = fields.Float(
        string="Quantity",
        digits=dp.get_precision("Product Unit of Measure"),
        compute="_compute_quantity")

    @api.model
    def fields_view_get(
        self, view_id=None, view_type='form', toolbar=False, submenu=False
    ):
        res = super(AccountInvoiceLine, self).fields_view_get(view_id=view_id,
                                                              view_type=view_type,
                                                              toolbar=toolbar,
                                                              submenu=submenu)
        return res
