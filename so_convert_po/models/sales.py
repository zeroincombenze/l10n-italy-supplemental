# -*- coding: utf-8 -*-

from datetime import date
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp


class ResCurrency(models.Model):
    _inherit = "res.currency"

    @api.multi
    def return_current_rate(self, currency_id, exchange_date=None):
        exchange_date = exchange_date or date.today()
        # Std Odoo core has a bug, so query is done here
        query = """select r.rate
                   from res_currency c,res_currency_rate r
                   where r.currency_id = c.id and r.name <= %s and c.id=%s
                   order by r.name desc limit 1"""
        self._cr.execute(query, (exchange_date, currency_id))
        rates = self._cr.fetchall()
        if not rates:
            return 1.0
        return rates[0][0]


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    allow_convert = fields.Boolean(
        "Allow convert SO to Purchase Order",
        compute='_compute_allow_convert',
    )
    margin = fields.Float(
        string='Margin',
        digits=dp.get_precision('Product Price'),
        default=0.0,
        readonly=True,
        store=True,
        help='Margin amount when converted into PO',
        compute='_compute_margin',
    )

    @api.one
    @api.depends('state')
    def _compute_allow_convert(self):
        # Generate field name to search value from settings,
        # if there's no field with generated name, will return False.
        self.allow_convert = self.env['ir.values'].get_default(
            'sale.config.settings',
            self.state + '_allow_convert',
        )

    @api.multi
    @api.depends('order_line.product_margin')
    def _compute_margin(self):
        for order in self:
            margin = 0.0
            for line in order.order_line:
                if line.state != 'cancel':
                    margin += line.product_margin
            order.update({
                'margin': margin
            })

    @api.multi
    def action_recompute_margin(self):
        for order in self:
            margin = 0.0
            for line in order.order_line:
                if line.purchase_order_line_id:
                    copy_sale_price = line.purchase_order_line_id.order_id.\
                        partner_id.copy_sale_price
                elif line.product_id:
                    copy_sale_price = line._get_purchase_partner(
                        line.product_id)
                    if copy_sale_price:
                        copy_sale_price = copy_sale_price.copy_sale_price
                else:
                    copy_sale_price = False
                vals = line._get_po_price(copy_sale_price)
                line.write(vals)
                margin += line.product_margin
            order.update({
                'margin': margin
            })

    @api.multi
    def action_convert_to_purchase_order(self):
        # import pdb
        # pdb.set_trace()
        default_state = self.env['ir.values'].get_default(
            'sale.config.settings',
            'state',
        )
        for order in self:
            vals = {
                'state': default_state,
                'sale_order_id': order.id,
                'origin': order.name,
            }
            valid_lines = 0
            for line in order.order_line:
                if not line.purchase_order_line_id and line.product_id:
                    valid_lines += 1
                    if 'currency_id' in vals and \
                            line.po_currency_id.id != vals['currency_id']:
                        continue
                    if 'partner_id' not in vals:
                        partner = line._get_purchase_partner(
                            line.product_id)
                        if partner:
                            vals['partner_id'] = partner.id
                    if 'reseller_id' not in vals and \
                            'reseller_id' in self.env['purchase.order']:
                        vals['reseller_id'] = order.partner_id.id
                    if 'end_user_id' not in vals and \
                            'end_user_id' in line and \
                            'end_user_id' in self.env['purchase.order']:
                        vals['end_user_id'] = line.end_user_id.id
                    if 'ref_user_id' not in vals and \
                            'ref_user_id' in line and \
                            'ref_user_id' in self.env['purchase.order']:
                        vals['ref_user_id'] = line.ref_user_id.id
                    if 'currency_id' not in vals:
                        vals['currency_id'] = line.po_currency_id.id
            if not valid_lines:
                continue
            if 'partner_id' in vals:
                partner = self.env['res.partner'].browse(vals['partner_id'])
                payment_id = partner.property_supplier_payment_term_id.id
                fiscal_position_id = partner.property_account_position_id.id
            else:
                vals['partner_id'] = order.partner_id.id
                payment_id = False
                fiscal_position_id = False
            if payment_id:
                vals['payment_term_id'] = payment_id
            if fiscal_position_id:
                vals['fiscal_position_id'] = fiscal_position_id
            purchase_order_id = self.env['purchase.order'].create(vals)
            for line in order.order_line:
                if line.purchase_order_line_id or not line.product_id:
                    continue
                if not line._get_purchase_partner(
                            line.product_id, partner_id=partner.id):
                    continue
                vals = {
                    'order_id': purchase_order_id.id,
                    'name': line.name,
                    'date_planned': fields.Datetime.now(),
                    'product_id': line.product_id.id,
                    'product_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.po_price_unit_ccy,
                    'discount': line.po_discount,
                    'sale_order_line_id': line.id,
                }
                purchase_line = self.env['purchase.order.line'].create(vals)
                if not line.po_price_unit:
                    purchase_line.onchange_product_id()
                    purchase_line.write(vals)
                    purchase_line._onchange_quantity()
                if not purchase_line.taxes_id:
                    purchase_line.taxes_id = [(
                        6, 0, [line.product_id.supplier_taxes_id.id])]
                line.write({'purchase_order_line_id': purchase_line.id})


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    po_price_unit = fields.Float(
        string='Purchase Unit Price',
        digits=dp.get_precision('Product Price'))
    po_discount = fields.Float(
        string='Purchase Discount (%)', digits=dp.get_precision('Discount'),
    )
    po_price_unit_ccy = fields.Float(
        string='Purchase Currency Unit Price',
        digits=dp.get_precision('Product Price'))
    po_currency_id = fields.Many2one(
        'res.currency',
        "Purchase Order Currency",
    )
    product_margin = fields.Float(
        string='Product Margin',
        digits=dp.get_precision('Product Price'),
        default=0.0,
        store=True,
        help='Margin amount when converted into PO',
        compute='_product_margin',
    )
    purchase_order_line_id = fields.Many2one(
        'purchase.order.line',
        "Purchase Order Line",
        help="Reference to Purchase Order Line",
        copy=False,
    )
    purchase_order_id = fields.Many2one(
        'purchase.order',
        related='purchase_order_line_id.order_id',
        string='Purchase Order',
        copy=False
    )

    def _get_purchase_partner(self, product, partner_id=None):
        partner = False
        for info in product.seller_ids:
            if partner_id and partner_id != info.name.id:
                continue
            partner = info.name
            break
        return partner

    @api.depends('product_id', 'product_uom_qty', 'discount', 'price_unit',
                 'po_price_unit', 'po_discount',  'price_subtotal')
    def _product_margin(self):
        for line in self:
            subtotal = line.po_price_unit * (1 - (
                line.po_discount or 0.0) / 100.0) * line.product_uom_qty
            line.product_margin = line.price_subtotal - subtotal

    @api.model
    def _get_po_price(self, copy_sale_price=None, supplier_id=None):
        po_price_unit = 0.0
        po_price_unit_ccy = 0.0
        po_currency_id = self.order_id.pricelist_id.currency_id.id
        po_discount = 0.0
        if self.product_id:
            if copy_sale_price is None:
                copy_sale_price = self._get_purchase_partner(
                    self.product_id)
                if copy_sale_price:
                    copy_sale_price = copy_sale_price.copy_sale_price
            product_supplierinfo = self.product_id._select_seller(
                    quantity=abs(self.product_uom_qty),
                    uom_id=self.product_uom,
                    partner_id=supplier_id)
            if self.purchase_order_line_id:
                po_discount = self.purchase_order_line_id.discount
            elif product_supplierinfo:
                po_discount = product_supplierinfo.discount
            else:
                po_discount = 0.0
            if self.purchase_order_line_id:
                po_price_unit = self.purchase_order_line_id.price_unit
                po_price_unit_ccy = po_price_unit
                currency = self.order_id.pricelist_id.currency_id
                po_currency_id = \
                    self.purchase_order_line_id.order_id.currency_id.id
                if po_currency_id != currency.id:
                    rate = self.env['res.currency'].return_current_rate(
                        po_currency_id,
                        exchange_date=self.order_id.date_order)
                    po_price_unit = po_price_unit / rate
            elif copy_sale_price:
                po_price_unit = self.price_unit
                po_price_unit_ccy = po_price_unit
                po_currency_id = self.order_id.pricelist_id.currency_id.id
            elif product_supplierinfo:
                po_price_unit = product_supplierinfo.price or self.price_unit
                po_price_unit_ccy = po_price_unit
                currency = self.order_id.pricelist_id.currency_id
                po_currency_id = currency.id
                if product_supplierinfo.currency_id.id != po_currency_id:
                    rate = self.env['res.currency'].return_current_rate(
                        product_supplierinfo.currency_id.id,
                        exchange_date=self.order_id.date_order)
                    po_price_unit = po_price_unit / rate
                    po_currency_id = product_supplierinfo.currency_id.id
        return {'po_price_unit': po_price_unit,
                'po_discount': po_discount,
                'po_price_unit_ccy': po_price_unit_ccy,
                'po_currency_id': po_currency_id,
                }

    @api.onchange('product_id')
    def product_id_change(self):
        res = {}
        if self.product_id:
            res = super(SaleOrderLine, self).product_id_change()
            res2 = self._get_po_price(copy_sale_price=None)
            for p in ('po_price_unit', 'po_discount',
                      'po_price_unit_ccy', 'po_currency_id'):
                self[p] = res2[p]
        return res

    @api.onchange('product_uom_qty', 'discount', 'price_unit', 'price_subtotal')
    def onchange_product_uom_qty(self):
        if self.product_id:
            res = self._get_po_price(copy_sale_price=None)
            for p in ('po_price_unit', 'po_discount',
                      'po_price_unit_ccy', 'po_currency_id'):
                self[p] = res[p]
