# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta

from odoo.addons.l10n_it_delivery_note.tests.delivery_note_common import (
    StockDeliveryNoteCommon,
)


class TestDdtInvoicingGroup(StockDeliveryNoteCommon):
    def _make_note(self, method, line):
        order = self.create_sales_order([line])
        order.ddt_invoicing_group = method
        order.action_confirm()
        picking = order.picking_ids
        for move in picking.move_ids:
            move.quantity = move.product_uom_qty
        picking.with_context(skip_backorder=True, skip_immediate=True).button_validate()
        self.assertEqual(picking.state, "done")
        note = self.create_delivery_note()
        note.transport_datetime = datetime.now() + timedelta(days=1)
        note.picking_ids = picking
        note.action_confirm()
        return note

    def _invoice_two(self, method):
        notes = self._make_note(method, self.desk_combination_line)
        notes |= self._make_note(method, self.right_corner_desk_line)
        notes.action_invoice()
        return notes

    def test_default_from_partner(self):
        self.recipient.commercial_partner_id.ddt_invoicing_group = "shipping_partner"
        order = self.create_sales_order([self.desk_combination_line])
        self.assertEqual(order.ddt_invoicing_group, "shipping_partner")

    def test_billing_partner_one_invoice(self):
        notes = self._invoice_two("billing_partner")
        self.assertEqual(len(notes.invoice_ids), 1)

    def test_nothing_one_invoice_each(self):
        notes = self._invoice_two("nothing")
        self.assertEqual(len(notes.invoice_ids), 2)
        for note in notes:
            self.assertEqual(len(note.invoice_ids), 1)

    def test_sale_order_one_invoice_each(self):
        notes = self._invoice_two("sale_order")
        self.assertEqual(len(notes.invoice_ids), 2)

    def test_code_group(self):
        self.recipient.ddt_code_group = "A"
        notes = self._invoice_two("code_group")
        self.assertEqual(len(notes.invoice_ids), 1)
