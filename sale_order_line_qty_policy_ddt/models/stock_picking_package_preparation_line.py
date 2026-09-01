# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from odoo import api, fields, models


class StockPickingPackagePreparationLine(models.Model):
    _inherit = "stock.picking.package.preparation.line"

    force_invoiced = fields.Boolean(
        string="Declared invoiced",
        copy=False,
        help="When set, this delivery note line is considered fully invoiced"
             " even if no invoice line was ever created from it; the line is"
             " no more selected to create an invoice from the delivery note.\n"
             "It is the very same declaration of the sale order line, taken"
             " at delivery note level: use it when the goods of this line"
             " must not be billed, i.e. a free replacement.",
    )
    line_invoiced = fields.Boolean(
        string="Invoiced",
        compute="_compute_line_invoiced",
        store=True,
        readonly=True,
        help="Technical field: the line is invoiced, either because an"
             " invoice line was created from it, or because it was declared"
             " invoiced, or because the quantity policy of its product"
             " declares it invoiced, or because its sale order line was"
             " declared invoiced.",
    )

    @api.multi
    def _is_line_invoiced(self):
        """Return True when the line has to be considered invoiced.

        The three declarations of sale_order_line_qty_policy are honoured
        here, so that a decision taken on the order is never contradicted by
        the delivery note: invoicing again what the order declared invoiced
        would bill the customer twice.
        """
        self.ensure_one()
        if self.invoice_line_id:
            return True
        if self.force_invoiced:
            return True
        if self.product_id.auto_line_invoiced:
            return True
        return (bool(self.sale_line_id)
                and self.sale_line_id._is_line_invoiced())

    @api.depends("invoice_line_id", "force_invoiced",
                 "product_id.auto_line_invoiced",
                 "sale_line_id.force_invoiced",
                 "sale_line_id.product_id.auto_line_invoiced")
    def _compute_line_invoiced(self):
        for line in self:
            line.line_invoiced = line._is_line_invoiced()

    @api.multi
    def _resync_invoiced(self):
        """Recompute the invoicing state after the database dropped a link.

        Deleting an invoice, or one of its lines, drops invoice_line_id here
        and invoice_id on the delivery note: both are foreign keys the
        database nulls on its own, so the ORM never learns that the stored
        line_invoiced and invoice_status have to be computed again. Without
        this, a delivery note line would stay invoiced forever - it could no
        more be billed - and its delivery note would keep showing as fully
        invoiced while carrying no invoice at all.
        """
        if not self:
            return
        ddt = self.mapped("package_preparation_id")
        self.invalidate_cache()
        ddt.invalidate_cache()
        self.modified(["invoice_line_id"])
        ddt.modified(["invoice_id"])
        self.recompute()
        ddt._update_invoice_reference()

    @api.multi
    def allow_invoice_line(self):
        """Keep out of the invoice every line the policy declares invoiced.

        This is the hook the standard module documents for such purposes; the
        caller skips the line and, doing so, leaves the delivery note without
        its invoice reference: see _update_invoice_reference().
        """
        res = super(
            StockPickingPackagePreparationLine, self).allow_invoice_line()
        return res and not self._is_line_invoiced()

    @api.multi
    def write(self, vals):
        """Keep the invoice reference of the delivery note up to date.

        Declaring the last open line invoiced closes the document, exactly as
        invoicing it would: the reference has to follow, whichever of the two
        happened last.
        """
        res = super(StockPickingPackagePreparationLine, self).write(vals)
        if "force_invoiced" in vals:
            self.mapped("package_preparation_id")._update_invoice_reference()
        return res

    @api.multi
    def action_line_invoice_create(self):
        res = super(StockPickingPackagePreparationLine,
                    self).action_line_invoice_create()
        self.mapped("package_preparation_id")._update_invoice_reference()
        return res

    @api.multi
    def action_declare_invoiced(self):
        return self.write({"force_invoiced": True})

    @api.multi
    def action_undeclare_invoiced(self):
        return self.write({"force_invoiced": False})
