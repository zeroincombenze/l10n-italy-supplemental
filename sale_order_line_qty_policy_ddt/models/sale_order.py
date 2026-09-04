# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
import odoo.addons.decimal_precision as dp

from odoo import api, fields, models
from odoo.tools import float_compare, float_is_zero


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    ddt_line_ids = fields.One2many(
        "stock.picking.package.preparation.line",
        "sale_line_id",
        string="Delivery note lines",
        readonly=True,
        help="The delivery note lines which delivered this order line.",
    )
    qty_ddt_declared = fields.Float(
        string="Declared invoiced on delivery notes",
        compute="_compute_qty_ddt_declared",
        store=True,
        readonly=True,
        digits=dp.get_precision("Product Unit of Measure"),
        help="Technical field: the quantity this order line delivered with"
             " delivery note lines which were declared invoiced, and which"
             " therefore will never produce an invoice line.\n"
             "It is counted beside the invoiced quantity, so that the order"
             " is not invoiced again for goods a delivery note already"
             " settled.",
    )

    @api.multi
    def _ddt_declared_lines(self):
        """Return the delivery note lines settled by a declaration of theirs.

        Only ``force_invoiced`` is looked at, and only when the line carries
        no invoice line. Every other way a delivery note line can be closed
        is already known to the order:

        * an invoice line is counted by ``qty_invoiced``, because
          l10n_it_ddt links it to this order line;
        * ``product_id.auto_line_invoiced`` and the declaration of the order
          line itself are read by _is_line_invoiced() of
          sale_order_line_qty_policy, which already zeroes what is left to
          invoice here.

        Counting those again would take the same quantity off twice.
        """
        self.ensure_one()
        return self.ddt_line_ids.filtered(
            lambda line: line.force_invoiced and not line.invoice_line_id)

    @api.depends("ddt_line_ids.force_invoiced",
                 "ddt_line_ids.invoice_line_id",
                 "ddt_line_ids.product_uom_qty",
                 "ddt_line_ids.product_uom_id")
    def _compute_qty_ddt_declared(self):
        for line in self:
            qty = 0.0
            for ddt_line in line._ddt_declared_lines():
                if ddt_line.product_uom_id and line.product_uom:
                    qty += ddt_line.product_uom_id._compute_quantity(
                        ddt_line.product_uom_qty, line.product_uom)
                else:
                    qty += ddt_line.product_uom_qty
            line.qty_ddt_declared = qty

    @api.depends("qty_ddt_declared")
    def _get_to_invoice_qty(self):
        """Take off what the delivery notes declared invoiced.

        A quantity, deliberately, and not a flag: one delivery note is one
        of several possible deliveries of this order line, so declaring it
        settled must close exactly what it delivered and leave the rest of
        the line to be invoiced. This is the only thing the delivery note is
        allowed to say about the order - see _ddt_declared_lines().
        """
        super(SaleOrderLine, self)._get_to_invoice_qty()
        precision = self._qty_precision()
        for line in self:
            if float_is_zero(line.qty_ddt_declared,
                             precision_digits=precision):
                continue
            line.qty_to_invoice = max(
                0.0, line.qty_to_invoice - line.qty_ddt_declared)

    @api.depends("qty_ddt_declared")
    def _compute_invoice_status(self):
        """Report the line invoiced once nothing is left of it to bill.

        Zeroing the quantity to invoice is not enough: standard Odoo reads a
        line with nothing to invoice and less invoiced than ordered as
        *Nothing to invoice*, which would hide the line from the invoicing
        list without ever declaring it done.
        """
        super(SaleOrderLine, self)._compute_invoice_status()
        precision = self._qty_precision()
        for line in self:
            if line.state not in ("sale", "done"):
                continue
            if line.invoice_status == "to invoice":
                # Something is still left of this line to invoice
                continue
            if float_is_zero(line.qty_ddt_declared,
                             precision_digits=precision):
                continue
            if line.product_id.invoice_policy == "order":
                target = line.product_uom_qty
            elif line._is_line_delivered():
                target = line.qty_delivered
            else:
                # Still being delivered: what is settled so far says nothing
                continue
            if float_compare(line.qty_invoiced + line.qty_ddt_declared,
                             target, precision_digits=precision) >= 0:
                line.invoice_status = "invoiced"
