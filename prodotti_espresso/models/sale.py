from odoo import api, models, fields, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def generate_ddt(self):
        """

        """

        ids = self.env.context.get('active_ids')
        if ids:
            to_process = []
            orders = self.search([('id', 'in', ids)])

            # ordini in stato 'sale' (Ordine di Vendita)
            if orders.filtered(lambda x: x.state != 'sale'):
                raise UserError('È stato selezionato un ordine non confermato.')

            # almeno un ordine con un prodotto espresso
            # (CHE NON DEVE ESSERE UN SERVIZIO)
            for order in orders:
                if order.order_line.filtered(lambda x: (
                        x.product_espresso is True and
                        x.product_id.type != 'service')):
                    to_process.append(order)
            if not to_process:
                raise UserError('Non sono stati rilevati prodotti di tipo '
                                'espresso negli ordini selezionati.')

            picks_lines = []
            group_by_address = {}
            for order in to_process:
                # handle stock picking
                if order.picking_ids:
                    for pick in order.picking_ids:
                        if pick.state == 'assigned':
                            if not pick.delivery_note_id or (
                                    pick.delivery_note_id and
                                    pick.delivery_note_id.state == 'draft'):
                                mv_lines = pick.move_ids_without_package
                                product_line = mv_lines.filtered(
                                    lambda x: x.product_id.espresso is True
                                )
                                if product_line:
                                    if pick.id not in picks_lines:
                                        picks_lines.append(pick.id)
                                    # print(product_line)
                                    for pl in product_line:
                                        if pl.quantity_done == 0:
                                            pl.write({
                                                'quantity_done':
                                                    pl.product_uom_qty
                                            })
        if picks_lines:
            for pick_id in picks_lines:
                picking = self.env['stock.picking'].browse(pick_id)
                # same checks made by button_validate

                if not picking.move_lines and not picking.move_line_ids:
                    raise UserError(_('Please add some items to move.'))

                picking_type = picking.picking_type_id
                precision_digits = self.env[
                    'decimal.precision'].precision_get(
                    'Product Unit of Measure')
                no_quantities_done = all(float_is_zero(move_line.qty_done,
                                                       precision_digits=
                                                       precision_digits)
                                         for move_line in
                                         picking.move_line_ids.filtered(
                                             lambda m: m.state not in (
                                                 'done', 'cancel')))
                no_reserved_quantities = all(
                    float_is_zero(move_line.product_qty,
                                  precision_rounding=
                                  move_line.product_uom_id.rounding)
                    for move_line in picking.move_line_ids)
                if no_reserved_quantities and no_quantities_done:
                    raise UserError(
                        _('You cannot validate a transfer if no quantites '
                          'are reserved nor done. To force the transfer, '
                          'switch in edit more and encode the done '
                          'quantities.'))

                if picking_type.use_create_lots or (
                        picking_type.use_existing_lots):
                    lines_to_check = picking.move_line_ids
                    if not no_quantities_done:
                        lines_to_check = lines_to_check.filtered(
                            lambda l: float_compare(
                                l.qty_done, 0, precision_rounding=
                                l.product_uom_id.rounding)
                        )

                    for line in lines_to_check:
                        product = line.product_id
                        if product and product.tracking != 'none':
                            if not line.lot_name and not line.lot_id:
                                raise UserError(
                                    _('You need to supply a Lot/Serial '
                                      'number for product %s.') %
                                    product.display_name)

                # need to check overprocessed_stock_moves
                if picking._get_overprocessed_stock_moves():
                    raise UserError(
                        _('Alcuni prodotti hanno una quantità superiore a '
                          'quella prevista.\nVerificare manualmente '
                          'la consegna'))

                # jump to move validation
                # doing so we avoid ddt generation done by l10n_it_delivery_note
                moves = picking.move_lines
                moves._action_done()

                if picking.state != 'done':
                    raise UserError(
                        _('La consegna {cn} risulta in stato anomalo {st} '
                          'rispetto a quanto atteso.'.format(
                            cn=picking.name, st=picking.state)))
                # so far we had backorders and picking validated

                # now grouping by address
                shipping_address_id = picking.sale_id.partner_shipping_id.id
                if shipping_address_id not in group_by_address:
                    group_by_address[shipping_address_id] = []
                group_by_address[shipping_address_id].append(picking)

            # generate ddt
            dev_note_ids = []
            for address_id, picks in group_by_address.items():
                ids = [p.id for p in picks]
                wz = self.env['stock.delivery.note.create.wizard'].create({
                    'date': fields.Date.today(),
                    'type_id': picks[0].picking_type_id.id,
                    'partner_shipping_id': address_id,
                    'selected_picking_ids': [(6, 0, ids)]
                })
                # create delivery note
                wz.confirm()
                dev_note = picks[0].delivery_note_id
                # confirm
                dev_note.action_confirm()
                # added for display
                dev_note_ids.append(dev_note.id)

            return {
                'name': 'Ddt',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'view_id': False,
                'domain': [('id', 'in', dev_note_ids)],
                'res_model': 'stock.delivery.note',
                'type': 'ir.actions.act_window',
                'target': 'current',
            }

        else:
            raise UserError('Non sono state rilevate consegne in stato '
                            'pronto.')


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_espresso = fields.Boolean(
        string="Prodotto espresso",
        related='product_id.espresso',
    )
