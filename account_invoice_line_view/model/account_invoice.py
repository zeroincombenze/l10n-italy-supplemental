# -*- coding: utf-8 -*-
# Copyright (C) 2014 Rooms For Limited T/A OSCG <https://www.odoo-asia.com>
# Copyright (C) 2016-22 SHS-AV s.r.l. <https://zeroincombenze.it>
#

from odoo import fields, models


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'
    _order = 'id desc'

    date_invoice = fields.Date(related='account.invoice.date_invoice',
                               string='Invoice Date')
    number = fields.Char(related='invoice_id.number', string=u'Number')
    date_invoice = fields.Date(related='invoice_id.date_invoice',
                               string=u'Invoice Date', store=True)
    state = fields.Selection(related='invoice_id.state',
                             string=u'Status', store=True)