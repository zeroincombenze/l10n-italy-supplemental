# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from odoo import api, fields, models
from odoo.tools import float_compare, float_is_zero


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Declared with the very same definition used by sale_delivery_state_z0:
    # when both modules are installed Odoo keeps one single field, so neither
    # module has to depend on the other one.
    force_delivery_state = fields.Boolean(
        string="Force delivery state",
        help=(
            "Allow to enforce done state of delivery, for instance if some"
            " quantities were cancelled"
        ),
    )
    force_delivery_state_manual = fields.Boolean(
        string="Delivery state forced by hand",
        copy=False,
        readonly=True,
        help="Technical field: force_delivery_state was written by a user, so"
             " the quantity policy will no more manage it.\n"
             "When it is not set, the flag belongs to the quantity policy,"
             " which sets and clears it following the delivered quantities."
             " An unknown value therefore never strands the flag: the policy"
             " simply takes it back.",
    )

    @api.multi
    def write(self, vals):
        # Any direct write of force_delivery_state takes the flag over: from
        # now on the quantity policy will no more manage it.
        if ("force_delivery_state" in vals
                and "force_delivery_state_manual" not in vals):
            vals = dict(vals, force_delivery_state_manual=True)
        return super(SaleOrder, self).write(vals)

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self._update_force_delivery_state()
        return res

    @api.multi
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        self._update_force_delivery_state()
        return res

    @api.multi
    def action_draft(self):
        """Resync the delivered quantities when the order goes back to draft.

        Standard action_draft detaches every procurement from its order line
        (``procurement_ids.write({'sale_line_id': False})``), so the line can
        no more account for its past stock moves: qty_delivered would keep
        forever the value written by the last delivery, even when the goods
        were returned. The real value is written back here, which for a
        detached line means zero, coherently with the fact that Odoo will
        count from now on the new procurements only.

        Services are left alone: their delivered quantity is entered by hand
        and _get_delivered_qty() would simply wipe it.
        """
        orders = self.filtered(lambda order: order.state in ("cancel", "sent"))
        res = super(SaleOrder, self).action_draft()
        lines = orders.mapped("order_line").filtered(
            lambda line: line.product_id.type in ("consu", "product"))
        for line in lines:
            qty = line._get_delivered_qty()
            if float_compare(qty, line.qty_delivered,
                             precision_digits=line._qty_precision()) != 0:
                line.qty_delivered = qty
        return res

    @api.multi
    def _update_force_delivery_state(self):
        """Keep force_delivery_state aligned with the quantity policy.

        The flag is set when every relevant line of the order is delivered
        and cleared when it is not. Orders whose flag was written by hand are
        left alone, so a decision taken by a user is never lost.
        """
        for order in self:
            if order.force_delivery_state_manual:
                continue
            if order.state in ("sale", "done"):
                lines = order.order_line.filtered(
                    lambda line: line._is_qty_policy_line())
                delivered = bool(lines) and all(
                    line.line_delivered for line in lines)
            else:
                delivered = False
            if delivered != order.force_delivery_state:
                order.write({
                    "force_delivery_state": delivered,
                    "force_delivery_state_manual": False,
                })


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Line fields whose change may alter the delivery state of the order
    QTY_POLICY_TRIGGERS = (
        "force_delivered",
        "product_id",
        "product_uom_qty",
        "qty_delivered",
        "state",
    )

    force_delivered = fields.Boolean(
        string="Declared delivered",
        copy=False,
        help="When set, this line is considered fully delivered even if the"
             " delivered quantity is less than the ordered one.\n"
             "Delivered quantity is not altered by this flag.",
    )
    force_invoiced = fields.Boolean(
        string="Declared invoiced",
        copy=False,
        help="When set, this line is considered fully invoiced even if there"
             " are ordered or delivered quantities still to invoice; the line"
             " is no more selected to create an invoice.",
    )
    line_delivered = fields.Boolean(
        string="Fully delivered",
        compute="_compute_line_delivered",
        store=True,
        readonly=True,
        help="Technical field: the line is delivered, either because the"
             " delivered quantity reached the ordered one, or because the"
             " deviation is within the product threshold, or because the line"
             " was manually declared delivered.",
    )

    @api.model
    def _qty_precision(self):
        return self.env["decimal.precision"].precision_get(
            "Product Unit of Measure")

    @api.multi
    def _is_qty_policy_line(self):
        """Return True when the line takes part in the delivery evaluation.

        Delivery cost lines and services are skipped, the same way
        sale_delivery_state_z0 does, so that both modules agree.
        """
        self.ensure_one()
        if not self.product_id:
            return False
        if getattr(self.product_id, "is_delivery", False):
            return False
        return self.product_id.type != "service"

    @api.model
    def create(self, vals):
        line = super(SaleOrderLine, self).create(vals)
        line.order_id._update_force_delivery_state()
        return line

    @api.multi
    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        if any(name in vals for name in self.QTY_POLICY_TRIGGERS):
            self.mapped("order_id")._update_force_delivery_state()
        return res

    @api.multi
    def _get_delivered_threshold(self):
        """Return the delivered threshold which applies to this line.

        The threshold declared on the product wins; when the product does not
        declare its own, the one of its category is used.
        """
        self.ensure_one()
        return (self.product_id.delivered_threshold
                or self.product_id.categ_id.delivered_threshold)

    @api.multi
    def _delivered_deviation_ok(self):
        """Return True when the absolute deviation between ordered and
        delivered quantity is within the applicable threshold.

        Both under and over delivery are evaluated. A line with nothing
        delivered is never within the threshold.
        """
        self.ensure_one()
        threshold = self._get_delivered_threshold()
        if not threshold:
            return False
        precision = self._qty_precision()
        if float_is_zero(self.product_uom_qty, precision_digits=precision):
            return False
        if float_is_zero(self.qty_delivered, precision_digits=precision):
            return False
        deviation = (abs(self.product_uom_qty - self.qty_delivered)
                     * 100.0 / abs(self.product_uom_qty))
        return float_compare(deviation, threshold, precision_digits=2) <= 0

    @api.multi
    def _is_line_delivered(self):
        """Return True when the line has to be considered fully delivered."""
        self.ensure_one()
        if self.state not in ("sale", "done"):
            return False
        if self.force_delivered:
            return True
        precision = self._qty_precision()
        if float_compare(self.qty_delivered, self.product_uom_qty,
                         precision_digits=precision) >= 0:
            return True
        return self._delivered_deviation_ok()

    @api.multi
    def _is_line_invoiced(self):
        """Return True when the line has to be considered fully invoiced."""
        self.ensure_one()
        return bool(self.force_invoiced or self.product_id.auto_line_invoiced)

    @api.depends("force_delivered", "qty_delivered", "product_uom_qty",
                 "state", "product_id.delivered_threshold",
                 "product_id.categ_id.delivered_threshold")
    def _compute_line_delivered(self):
        for line in self:
            line.line_delivered = line._is_line_delivered()

    @api.depends("force_invoiced", "product_id.auto_line_invoiced")
    def _get_to_invoice_qty(self):
        super(SaleOrderLine, self)._get_to_invoice_qty()
        for line in self:
            if line._is_line_invoiced():
                line.qty_to_invoice = 0.0

    @api.depends("force_invoiced", "force_delivered",
                 "product_id.auto_line_invoiced",
                 "product_id.delivered_threshold",
                 "product_id.categ_id.delivered_threshold")
    def _compute_invoice_status(self):
        super(SaleOrderLine, self)._compute_invoice_status()
        precision = self._qty_precision()
        for line in self:
            if line.state not in ("sale", "done"):
                continue
            if line._is_line_invoiced():
                # Nothing else has to be invoiced for this line
                line.invoice_status = "invoiced"
            elif (line.invoice_status == "upselling"
                  and line._delivered_deviation_ok()):
                # Over delivery within threshold is not an upselling occasion
                line.invoice_status = "invoiced"
            elif (line.invoice_status != "to invoice"
                  and line._is_line_delivered()
                  and not float_is_zero(line.qty_invoiced,
                                        precision_digits=precision)
                  and float_compare(line.qty_invoiced, line.qty_delivered,
                                    precision_digits=precision) >= 0):
                # Line delivered by threshold and fully invoiced for what has
                # been really delivered: standard Odoo would leave it 'no'
                line.invoice_status = "invoiced"

    @api.multi
    def action_declare_delivered(self):
        return self.write({"force_delivered": True})

    @api.multi
    def action_undeclare_delivered(self):
        return self.write({"force_delivered": False})

    @api.multi
    def action_declare_invoiced(self):
        return self.write({"force_invoiced": True})

    @api.multi
    def action_undeclare_invoiced(self):
        return self.write({"force_invoiced": False})
