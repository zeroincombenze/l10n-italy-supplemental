# -*- coding: utf-8 -*-
from odoo import api, models, fields
# from odoo.exceptions import UserError
# from odoo.tools.float_utils import float_compare, float_is_zero


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line')
    def _with_espresso(self):
        for order in self:
            order.espresso = any(line.espresso for line in order.order_line)

    espresso = fields.Boolean(
        string="Documento con prodotti espresso",
        compute="_with_espresso",
        stored=True,
    )

    @api.multi
    def _delivery_unset(self):
        self.mark_real_delivery_lines()
        return super(SaleOrder, self)._delivery_unset()

    @api.multi
    def generate_ddt_espresso(self, validate=None, to_send_mail=None):

        def exec_wizard(action):
            res_model = action['res_model']
            ctx = action['context'] or {}
            wiz = self.env[res_model].browse(action['res_id']).with_context(ctx)
            fct = 'process'
            if hasattr(wiz, fct):
                return getattr(wiz, fct)()
            return False

        ddt_model = self.env["stock.picking.package.preparation"]
        orders = []
        ddts = {}
        default_carrier = False
        for order in self:
            if (
                order.state != "sale" or
                not order.order_line.filtered(
                    lambda ln: ln.line_with_product_espresso()
                )
            ):
                # Sale Order without espresso products
                continue
            if not default_carrier and order.carrier_id:
                default_carrier = order.carrier_id
            hash_key = '%d|%d|%d' % (
                order.partner_id.id,
                order.partner_shipping_id.id,
                order.payment_term_id.id)
            for picking in order.picking_ids:
                if len(picking.ddt_ids) or not picking.move_lines.filtered(
                    lambda ln: ln.line_with_product_espresso()
                ):
                    # Picking without espresso products
                    continue
                nro_lines = 0
                if picking.state in ("draft",
                                     "waiting",
                                     "partially_available",
                                     "confirmed"):
                    picking.action_assign()
                if picking.state != "assigned":
                    picking.force_assign()
                if picking.state == "assigned":
                    for pack in picking.pack_operation_ids:
                        if not default_carrier and pack.product_id.is_delivery:
                            default_carrier = self.env["delivery.carrier"].search(
                                [("product_id", "=", pack.product_id.id)])
                        if (
                            not pack.product_id.is_delivery
                            and pack.product_id.espresso
                            and pack.product_qty > 0
                        ):
                            pack.write({'qty_done': pack.product_qty})
                            nro_lines += 1
                        else:
                            pack.unlink()
                if nro_lines:
                    action = picking.do_new_transfer()
                    if isinstance(action, dict):
                        exec_wizard(action)
                    if hash_key not in ddts:
                        ddts[hash_key] = self.env["stock.picking"]
                    ddts[hash_key] += picking
                    if picking.sale_id not in orders:
                        orders.append(picking.sale_id)
        ddt_ids = []
        for hash_key in ddts.keys():
            ddt = ddt_model.create(
                ddt_model.preparare_ddt_data(
                    ddts[hash_key],
                    defaults={
                        "transportation_reason_id": self.env.ref(
                            "l10n_it_ddt.transportation_reason_VEN").id,
                        "goods_description_id":
                            self.env.ref("l10n_it_ddt.goods_description_CAR"),
                        "carrier_id": default_carrier.id if default_carrier else False,
                    }
                )
            )
            # Workaround?
            ddt._amount_all()
            ddt.to_send_mail = to_send_mail or True
            if validate:
                ddt.set_done()
            ddt_ids.append(ddt.id)
        return ddt_ids


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    espresso = fields.Boolean(
        string="Prodotto espresso",
        related="product_id.espresso",
    )

    @api.model
    def line_with_product_espresso(self):
        return (self.product_id.espresso and not self.product_id.is_delivery)


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def line_with_product_espresso(self):
        return (self.product_id.espresso and not self.product_id.is_delivery)
