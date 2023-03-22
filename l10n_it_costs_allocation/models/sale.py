# Copyright (c) 2021
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

from ..utils import ventilazione_costi


class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_goods_n_service_amount = fields.Float(
        string='Totale beni e servizi',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    total_goods_amount = fields.Float(
        string='Totale beni',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    total_delivery_amount = fields.Float(
        string='Totale costo spedizioni',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    total_packaging_amount = fields.Float(
        string='Totale costo imballo',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    total_payment_amount = fields.Float(
        string='Totale costo pagamenti',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    total_other_amount = fields.Float(
        string='Totale costi diversi',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    total_discount_amount = fields.Float(
        string='Totale sconto',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    @api.model
    def create(self, values):
        # Apply modifications inside DB transaction
        new_sale_order = super().create(values)

        # Set default for date_effective
        ventilazione_costi(new_sale_order, new_sale_order.order_line)

        # Return the result of the write command
        return new_sale_order
    # end create

    @api.multi
    def write(self, values):

        result = super().write(values)

        if not self.env.context.get('StopRecursion'):

            self = self.with_context(StopRecursion=True)
            for so in self:
                ventilazione_costi(so, so.order_line)
            # end for

        # end if

        return result

    # end write

    def calcola_ventilazione_costi(self):
        ventilazione_costi(self, self.order_line)
    # end aggiorna_ventilazione_costi

# end SaleOrder


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    cost_delivery_amount = fields.Float(
        string='Costo spedizioni',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    cost_packaging_amount = fields.Float(
        string='Costo imballo',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    cost_payment_amount = fields.Float(
        string='Costo pagamenti',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    cost_other_amount = fields.Float(
        string='Costo diversi',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    cost_discount_amount = fields.Float(
        string='Ripartizione sconto globale',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        res = super()._prepare_invoice_line(qty)

        res.update({
            'cost_delivery_amount': self.cost_delivery_amount,
            'cost_packaging_amount': self.cost_packaging_amount,
            'cost_payment_amount': self.cost_payment_amount,
            'cost_other_amount': self.cost_other_amount,
            'cost_discount_amount': self.cost_discount_amount,
        })

        return res
    # end _prepare_invoice_line

# end SaleOrderLine
