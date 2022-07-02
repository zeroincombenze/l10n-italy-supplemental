# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.model
    def _get_advance_payment_method(self):
        res = super(SaleAdvancePaymentInv, self)._get_advance_payment_method()
        if self._count() > 1:
            sale_model = self.env["sale.order"]
            order_policy = True
            for order in sale_model.browse(self._context.get("active_ids")):
                if (not all([line.product_id.invoice_policy == 'order'
                             for line in order.order_line])
                        and not order.invoice_count):
                    order_policy = False
                    break
            if order_policy:
                res = "all"
        return res

    advance_payment_method = fields.Selection(default=_get_advance_payment_method)

    @api.multi
    def create_invoices(self):
        return super(SaleAdvancePaymentInv, self).create_invoices()
