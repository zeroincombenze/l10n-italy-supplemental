# Copyright (c) 2021
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

from ..utils import ventilazione_costi


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

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

    total_delivery_from_lines = fields.Boolean(string='delivery',
                                               compute='_compute_delivery')
    total_packaging_from_lines = fields.Boolean(string='packaging',
                                                compute='_compute_packaging')
    total_payment_from_lines = fields.Boolean(string='payment',
                                              compute='_compute_payment')
    total_other_from_lines = fields.Boolean(string='other',
                                            compute='_compute_other')
    total_discount_from_lines = fields.Boolean(string='discount',
                                               compute='_compute_discount')

    @api.depends('invoice_line_ids')
    def _compute_delivery(self):
        for item in self:
            has_delivery = False
            for line in item.invoice_line_ids:
                if line.cost_delivery_amount > 0:
                    has_delivery = True
            item.total_delivery_from_lines = has_delivery

    @api.depends('invoice_line_ids')
    def _compute_packaging(self):
        for item in self:
            has_packaging = False
            for line in item.invoice_line_ids:
                if line.cost_packaging_amount > 0:
                    has_packaging = True
            item.total_packaging_from_lines = has_packaging

    @api.depends('invoice_line_ids')
    def _compute_payment(self):
        for item in self:
            has_payment = False
            for line in item.invoice_line_ids:
                if line.cost_payment_amount > 0:
                    has_payment = True
            item.total_payment_from_lines = has_payment

    @api.depends('invoice_line_ids')
    def _compute_other(self):
        for item in self:
            has_other = False
            for line in item.invoice_line_ids:
                if line.cost_other_amount > 0:
                    has_other = True
            item.total_other_from_lines = has_other

    @api.depends('invoice_line_ids')
    def _compute_discount(self):
        for item in self:
            has_discount = False
            for line in item.invoice_line_ids:
                if line.cost_discount_amount != 0:
                    has_discount = True
            item.total_discount_from_lines = has_discount

    @api.model
    def create(self, vals):

        inv = super().create(vals)

        ventilazione_costi(inv, inv.invoice_line_ids)

        return inv
    # end create

    @api.multi
    def write(self, values):

        result = super().write(values)

        # Check costs spreading recompute conditions:
        #  - stop recursion is not active
        #  - invoice lines were changed
        stop_recursion = self.env.context.get('StopRecursion', False)
        lines_updates = 'invoice_line_ids' in values

        if not stop_recursion and lines_updates:

            # Enable stop recursion
            self = self.with_context(StopRecursion=True)

            # Compute costs spreading for each invoice
            for invoice in self:
                ventilazione_costi(invoice, invoice.invoice_line_ids)
            # end for

        # end if

        return result

    # end write
