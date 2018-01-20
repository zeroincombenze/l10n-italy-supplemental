# -*- coding: utf-8 -*-
#
# Copyright 2017-2018, Didotech srl (http://www.didotech.com).
# Copyright 2017-2018, Andrei Levin <andrei.levin@didotech.com>
# Copyright 2018, Associazione Odoo Italia <https://odoo-italia.org>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from openerp import _, api, fields, models
from openerp.tools.float_utils import float_round


class StockMove(models.Model):
    _inherit = 'stock.move'

    new_picking = fields.Boolean(
        'New DDT',
        help='Create new DdT (if necessary) on quantity diminishing',
        default=True)
    new_qty = fields.Float(default=0)

    @api.one
    def change_quantity(self, new_qty):
        new_pickings = self.env['stock.picking'].search([
            ('state', '=', 'draft'),
            ('group_id', '=', self.picking_id.group_id.id),
            ('origin', '!=', 'False'),
            ('id', '!=', self.id)
        ])
        if new_pickings and not new_pickings[0] == self.picking_id:
            new_picking = new_pickings[0]
        else:
            new_picking = self.picking_id.copy(default={
                'move_lines': []
            })

        self.copy(default={
            'product_uom_qty': new_qty,
            'picking_id': new_picking.id
        })

        # return new_move
        return True

    # Using old API here, because I need to be able to use warning returned
    # by the function
    def onchange_quantity(
            self, cr, uid, ids, product_id, product_qty, product_uom,
            product_uos, new_picking=False):
        """ On change of product quantity finds UoM and UoS quantities
        @param product_id: Product id
        @param product_qty: Changed Quantity of product
        @param product_uom: Unit of measure of product
        @param product_uos: Unit of sale of product
        @return: Dictionary of values
        """
        result = {
            'product_uos_qty': 0.00
        }
        warning = {}

        # if (not product_id) or (product_qty <= 0.0):
        if not product_id:
            result['product_qty'] = 0.0
            return {'value': result}

        uos_coeff = self.pool['product.product'].browse(cr, uid, product_id)

        # Warn if the quantity was decreased
        if len(ids) == 1:
            for move in self.browse(cr, uid, ids):
                if product_qty < move.product_qty and new_picking:
                    # move.change_quantity(move.product_qty - product_qty)
                    result['new_qty'] = move.product_qty - product_qty
                elif product_qty < move.product_qty:
                    warning.update({
                        'title': _('Information'),
                        'message': _(
                            "By changing this quantity here, you accept the "
                            "new quantity as complete: Odoo will not "
                            "automatically generate a back order.")})
                break

        if product_uos and product_uom and (product_uom != product_uos):
            precision = self.pool['decimal.precision'].precision_get(
                cr, uid, 'Product UoS')
            result['product_uos_qty'] = float_round(
                product_qty * uos_coeff.uos_coeff, precision_digits=precision)
        else:
            result['product_uos_qty'] = product_qty

        result['picking_id'] = move.picking_id.id

        return {'value': result, 'warning': warning}

    @api.multi
    def unlink(self):
        for move in self:
            if move.product_qty == 0:
                move.state = 'draft'
        return super(StockMove, self).unlink()


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def write(self, values):
        if 'move_lines' in values:
            for line in values['move_lines']:
                if line[0] == 1 and 'new_qty' in line[2] and line[2][
                        'new_qty']:
                    move = self.env['stock.move'].browse(line[1])
                    if ('new_picking' in line[2] and
                        line[2]['new_picking']) or \
                            ('new_picking' not in line[
                                2] and move.new_picking):
                        move.change_quantity(line[2]['new_qty'])
                    line[2]['new_qty'] = 0

        return super(StockPicking, self).write(values)
