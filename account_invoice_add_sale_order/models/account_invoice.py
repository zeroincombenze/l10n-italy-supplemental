# -*- coding: utf-8 -*-
# Copyright 2018 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from odoo.tools.float_utils import float_compare


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sale_id = fields.Many2one('sale.order', string='Add Sale Order',
        help='When selected, the associated sale order lines are added.')

    def _prepare_invoice_line_from_so_line(self, line):
        if line.qty_delivered:
            qty = line.qty_delivered - line.qty_invoiced
        else:
            qty = line.product_qty - line.qty_invoiced
        if float_compare(qty,
                         0.0,
                         precision_rounding=line.product_uom.rounding) <= 0:
            qty = 0.0
        invoice_line = self.env['account.invoice.line']
        taxes = line.tax_id
        invoice_line_tax_ids = line.order_id.fiscal_position_id.map_tax(taxes)
        account_id = line.product_id.property_account_income_id.id or \
                  line.product_id.categ_id.property_account_income_categ_id.id or \
                  invoice_line.with_context(
                      {
                          'journal_id': self.journal_id.id,
                          'type': 'out_invoice'
                      }
                  )._default_account(),
        data = {
            'sale_line_ids': [(6, 0, [line.id])],
            'name': line.name,
            'origin': line.order_id.name or line.order_id.origin,
            'uom_id': line.product_uom.id,
            'product_id': line.product_id.id or False,
            'account_id': account_id,
            'price_unit': line.order_id.currency_id.with_context(
                date=self.date_invoice).compute(
                    line.price_unit, self.currency_id, round=False),
            'quantity': qty,
            'discount': line.discount,
            'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
            'invoice_line_tax_ids': invoice_line_tax_ids.ids,
            'account_analytic_id': line.order_id.project_id.id,
            'sequence': line.sequence,
            'layout_category_id': line.layout_category_id and \
                                  line.layout_category_id.id or False,
        }
        return data

    # Load all SO lines
    @api.onchange('sale_id')
    def sale_order_change(self):
        if not self.sale_id:
            return {}
        if not self.partner_id:
            self.partner_id = self.sale_id.partner_id.id
        if not self.origin:
            self.origin = self.sale_id.name
        elif self.origin.find(self.sale_id.name) < 0:
            self.origin += ', %s' % self.sale_id.name

        new_lines = self.env['account.invoice.line']
        for line in self.sale_id.order_line - self.invoice_line_ids.mapped(
                'sale_line_ids'):
            data = self._prepare_invoice_line_from_so_line(line)
            new_line = new_lines.new(data)
            new_line._set_additional_fields(self)
            new_lines += new_line

        self.invoice_line_ids += new_lines
        self.sale_id = False
        return {}