# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPickingPackagePreparation(models.Model):
    _inherit = "stock.picking.package.preparation"

    invoice_status = fields.Selection(
        [
            ("no", "Nothing to invoice"),
            ("to invoice", "To invoice"),
            ("invoiced", "Fully invoiced"),
        ],
        string="Invoice status",
        compute="_compute_invoice_status",
        store=True,
        readonly=True,
        default="no",
        help="Invoicing state of the delivery note, evaluated the same way"
             " Odoo evaluates the one of a sale order:\n"
             "* Nothing to invoice: the delivery note is not invoiceable yet,"
             " or its reason for transportation declares it is not to be"
             " invoiced;\n"
             "* To invoice: at least one line has still to be invoiced;\n"
             "* Fully invoiced: every line is invoiced or declared invoiced."
             " A delivery note may be fully invoiced without carrying any"
             " invoice, when the quantity policy declares every line"
             " invoiced.",
    )

    @api.multi
    def _is_invoiceable(self):
        """Return True when the state of the delivery note allows invoicing.

        Same rule as action_invoice_create: a delivery note is invoiceable
        when it is done, or when it is still in pack and the company prices
        the delivery on the delivery note itself.

        The reason for transportation is read here instead of to_be_invoiced,
        which mirrors it: that flag is lowered once the document is fully
        invoiced - it answers "is there still something to bill?" - while
        this method answers "is this document one to be billed at all?",
        which no invoice can change.
        """
        self.ensure_one()
        if not self.transportation_reason_id.to_be_invoiced:
            return False
        return self.state == "done" or (
            self.state == "in_pack"
            and self.company_id.delivery_price_policy == "delivery")

    @api.multi
    def _is_fully_invoiced(self):
        """Return True when no line of the delivery note is left to invoice.

        The state of the document is not looked at: this is a statement on
        its content, which is what both to_be_invoiced and invoice_status
        need before they weigh the state in.
        """
        self.ensure_one()
        if self.invoice_id:
            return True
        return bool(self.line_ids) and all(
            line.line_invoiced for line in self.line_ids)

    @api.multi
    @api.depends("transportation_reason_id.to_be_invoiced", "invoice_id",
                 "line_ids", "line_ids.line_invoiced")
    def _compute_to_be_invoiced(self):
        """Lower the flag as soon as the delivery note is fully invoiced.

        l10n_it_ddt keeps to_be_invoiced as the answer to "has this document
        still to be billed?": the mass invoicing wizard selects on it, and so
        does the standard list filter. Its compute only mirrors the reason
        for transportation, so the flag stays raised for ever, and a delivery
        note the quantity policy closed - with an invoice or without any at
        all - would keep being offered for invoicing.

        The flag is therefore lowered here once every line is invoiced, and
        raised again by this very same compute when a line goes back to be
        invoiced: a declaration withdrawn, an invoice deleted. It is kept for
        compatibility, nothing of this module reads it - invoice_status is
        the field to read.

        invoice_status is deliberately not a trigger of this compute: it is
        computed from the same facts, and depending on it would close a cycle
        between the two fields.
        """
        super(StockPickingPackagePreparation, self)._compute_to_be_invoiced()
        for ddt in self:
            if ddt.to_be_invoiced and ddt._is_fully_invoiced():
                ddt.to_be_invoiced = False

    @api.multi
    def _get_invoice_status(self):
        """Return the invoicing state of the delivery note."""
        self.ensure_one()
        if self.invoice_id:
            return "invoiced"
        if not self._is_invoiceable() or not self.line_ids:
            return "no"
        if self._is_fully_invoiced():
            return "invoiced"
        return "to invoice"

    @api.depends("state", "transportation_reason_id.to_be_invoiced",
                 "invoice_id", "company_id.delivery_price_policy",
                 "line_ids", "line_ids.line_invoiced")
    def _compute_invoice_status(self):
        for ddt in self:
            ddt.invoice_status = ddt._get_invoice_status()

    @api.multi
    def _has_invoiceable_line(self):
        """Return True when at least one line has still to be invoiced."""
        self.ensure_one()
        if not self.line_ids:
            # Nothing for the policy to say: let the standard method decide
            return True
        return any(line.allow_invoice_line() for line in self.line_ids)

    @api.multi
    def _update_invoice_reference(self):
        """Mark as invoiced the delivery notes the policy left half marked.

        Standard action_invoice_create sets ddt.invoice_id only when *every*
        line was invoiced during that very run: one single line skipped -
        because the policy declares it invoiced, or because a previous run
        invoiced it already - leaves the reference empty forever. The
        delivery note then keeps showing up as to be invoiced, and the only
        thing a further run can do is to fail with 'There is no invoicable
        line'.

        The reference is therefore written here whenever every line is
        invoiced, whatever the run which invoiced it. When the lines were
        split over several invoices, the most recent one is taken, which is
        what the standard method leaves behind in the same situation.

        The reference is cleared again when a line goes back to be invoiced,
        which happens when a declaration is withdrawn or when an invoice is
        deleted: the code owns what the code wrote, so a delivery note is
        never stranded in invoiced state. A reference written by the standard
        method is never cleared, because it implies that every line carries
        its own invoice line, which no declaration can undo.
        """
        for ddt in self:
            if not ddt.line_ids:
                continue
            if not all(line.line_invoiced for line in ddt.line_ids):
                if ddt.invoice_id:
                    ddt.invoice_id = False
                continue
            if ddt.invoice_id:
                continue
            invoices = ddt.line_ids.mapped("invoice_line_id.invoice_id")
            if not invoices:
                # Every line was declared invoiced: there is no invoice at
                # all and invoice_status is enough to close the document
                continue
            ddt.invoice_id = max(invoices, key=lambda invoice: invoice.id).id

    @api.multi
    def action_invoice_create(self):
        """Invoice the delivery notes which still have something to invoice.

        A delivery note whose every line is declared invoiced has nothing to
        hand over to the invoice: the standard method would walk it, skip
        every line and end with 'There is no invoicable line', taking down
        the invoicing of every other delivery note selected with it - which
        is exactly what the mass invoicing wizard does.
        """
        todo = self.filtered(lambda ddt: ddt._has_invoiceable_line())
        if not todo:
            raise UserError(
                _("Nothing to invoice: every line of %s is already invoiced"
                  " or declared invoiced")
                % ", ".join([ddt.ddt_number or ddt.display_name or ""
                             for ddt in self]))
        res = super(StockPickingPackagePreparation,
                    todo).action_invoice_create()
        todo._update_invoice_reference()
        return res
