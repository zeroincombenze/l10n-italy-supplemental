# -*- coding: utf-8 -*-
#    Odoo, Open Source Management Solution
#    Copyright (C) 2014 Rooms For (Hong Kong) Limited T/A OSCG
#    <https://www.odoo-asia.com>

from odoo import api, fields, models
from datetime import datetime
from odoo.tools.translate import _

import odoo.addons.decimal_precision as dp


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    date_invoice = fields.Date(related='account.invoice.date_invoice',
                               string='Invoice Date')

    def _get_base_amt(self, field_names, args, context=None):
        res = {}
        for invoice_line in self.browse(cr, uid, ids, context=context):
            curr_amt = invoice_line.price_subtotal
            # set the rate 1.0 if the transaction currency is the same as the base currency
            if invoice_line.company_id.currency_id == invoice_line.currency_id:
                rate = 1.0
            else:
                invoice_obj = self.pool.get('account.invoice')
                invoice_date = invoice_obj.read(cr, uid, invoice_line.invoice_id.id, ['date_invoice'])['date_invoice']
                if invoice_date:
                    invoice_date_datetime = datetime.strptime(invoice_date, '%Y-%m-%d')
                else:
                    today = context.get('date', datetime.today().strftime('%Y-%m-%d'))
                    invoice_date_datetime = datetime.strptime(today, '%Y-%m-%d')

                rate_obj = self.pool['res.currency.rate']
                rate_rec = rate_obj.search(cr, uid, [
                    ('currency_id', '=', invoice_line.currency_id.id),
                    ('name', '<=', invoice_date_datetime),
                    # not sure for what purpose 'currency_rate_type_id' field exists in the table, but keep this line just in case
                    ('currency_rate_type_id', '=', None)
                ], order='name desc', limit=1, context=context)
                if rate_rec:
                    rate = rate_obj.read(cr, uid, rate_rec[0], ['rate'], context=context)['rate']
                else:
                    rate = 1.0
            res[invoice_line.id] = {
                'rate': rate,
                'base_amt': curr_amt / rate,
            }
        return res

    """ return all the invoice lines for the updated invoice """

    def _get_invoice_lines(self, ids, context=None):
        invoice_line_ids = []
        for invoice in self.browse(cr, uid, ids, context=context):
            invoice_line_ids += self.pool.get('account.invoice.line').search(cr, uid, [('invoice_id.id', '=', invoice.id)], context=context)
        return invoice_line_ids

    _order = 'id desc'
    """ some fields are defined with 'store' for grouping purpose """

    ## user_id = fields.related('invoice_id', 'user_id', type='many2one', relation='res.users', string=u'Salesperson')
    number = fields.Char(related='invoice_id.number', string=u'Number')
    state = fields.Selection(related='invoice_id.state', string=u'Status',
                        compute='_get_invoice_lines', store=True)
    date_invoice = fields.Date(related='invoice_id.date_invoice', string=u'Invoice Date', store=True)
    ## reference = fields.related('invoice_id', 'reference', type='char', string=u'Invoice Ref')
    ## date_due = fields.related('invoice_id', 'date_due', type='date', string=u'Due Date')
    ## currency_id = fields.related('invoice_id', 'currency_id', relation='res.currency', type='many2one', string=u'Currency')
    ## rate = fields.function(_get_base_amt, type='float', string=u'Rate', multi='base_amt')
    ## base_amt = fields.function(_get_base_amt, type='float', digits_compute=dp.get_precision('Account'), string=u'Base Amount', multi="base_amt")

    # def init(self, cr, uid):
    #     # to be executed only when installing the module.  update "stored" fields
    #     cr.execute(
    #         "update account_invoice_line line \
    #                 set state = inv.state, date_invoice = inv.date_invoice, partner_id = inv.partner_id \
    #                 from account_invoice inv \
    #                 where line.invoice_id = inv.id")
