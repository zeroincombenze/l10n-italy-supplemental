# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestSaleOrderLineQtyPolicyDdt(TransactionCase):

    # Sale orders and pickings need the whole registry: run post install
    at_install = False
    post_install = True

    def setUp(self):
        super(TestSaleOrderLineQtyPolicyDdt, self).setUp()
        self.ddt_model = self.env["stock.picking.package.preparation"]
        self.customer = self.env["res.partner"].create({
            "name": "Test DdT Qty Policy Customer",
            "customer": True,
        })
        self.ddt_type = self.env.ref("l10n_it_ddt.ddt_type_ddt")
        self.carriage_condition = self.env.ref(
            "l10n_it_ddt.carriage_condition_PF")
        self.goods_description = self.env.ref(
            "l10n_it_ddt.goods_description_CAR")
        # Vendita: the only reason which declares the DdT to be invoiced
        self.reason_to_invoice = self.env.ref(
            "l10n_it_ddt.transportation_reason_VEN")
        self.reason_not_to_invoice = self.env.ref(
            "l10n_it_ddt.transportation_reason_VIS")
        self.method = self.env.ref("l10n_it_ddt.transportation_method_MIT")

        self.product = self._create_product("Test DdT product", {})
        self.other_product = self._create_product("Test DdT other product", {})
        # Product recomputed at invoice level, i.e. CONAI contribution
        self.tax_product = self._create_product("Test DdT CONAI product", {
            "auto_line_invoiced": True,
        })

    def _create_product(self, name, vals):
        values = {
            "name": name,
            "type": "consu",
            "invoice_policy": "delivery",
        }
        values.update(vals)
        return self.env["product.product"].create(values)

    def _ddt_values(self, products, reason=None):
        lines = []
        for product in products:
            lines.append((0, 0, {
                "name": product.name,
                "product_id": product.id,
                "product_uom_qty": 10.0,
                "product_uom_id": product.uom_id.id,
                "price_unit": 5.0,
            }))
        return {
            "partner_id": self.customer.id,
            "ddt_type_id": self.ddt_type.id,
            "carriage_condition_id": self.carriage_condition.id,
            "goods_description_id": self.goods_description.id,
            "transportation_reason_id": (
                reason or self.reason_to_invoice).id,
            "transportation_method_id": self.method.id,
            "line_ids": lines,
        }

    def _create_ddt(self, products, reason=None):
        return self.ddt_model.create(self._ddt_values(products, reason=reason))

    def _create_order(self, product, qty=10.0):
        order = self.env["sale.order"].create({
            "partner_id": self.customer.id,
            "order_line": [(0, 0, {
                "product_id": product.id,
                "name": product.name,
                "product_uom_qty": qty,
                "product_uom": product.uom_id.id,
                "price_unit": 5.0,
            })],
        })
        order.action_confirm()
        return order

    def _line_of(self, ddt, product):
        return ddt.line_ids.filtered(lambda line: line.product_id == product)

    def _ddt_from_pickings(self, pickings, reason=None):
        """Build a DdT from pickings: the only way sale_line_id is set."""
        return self.ddt_model.create(dict(
            self._ddt_values([], reason=reason),
            picking_ids=[(6, 0, pickings.ids)]))

    def _deliver(self, order, qty):
        """Deliver part of the order, and return that picking and its rest.

        The move is really split, so the order line ends up with several
        delivery notes each carrying its own quantity - which is the whole
        point of counting a quantity rather than raising a flag.

        do_new_transfer() does not transfer anything by itself when the
        quantities do not match the demand: it returns the action of a
        wizard - a backorder confirmation here, an immediate transfer when
        no quantity was entered at all - and the transfer happens when that
        wizard is processed.
        """
        picking = order.picking_ids.filtered(
            lambda pick: pick.state not in ("done", "cancel"))[:1]
        self.assertTrue(picking, "no picking left to deliver")
        picking.force_assign()
        if not picking.pack_operation_ids:
            picking.do_prepare_partial()
        picking.pack_operation_product_ids.write({"qty_done": qty})
        action = picking.do_new_transfer()
        if isinstance(action, dict) and action.get("res_id"):
            self.env[action["res_model"]].browse(action["res_id"]).process()
        self.assertEqual(picking.state, "done")
        backorder = self.env["stock.picking"].search(
            [("backorder_id", "=", picking.id)])
        return picking, backorder

    def _assert_product_cannot_be_reinvoiced(self, order, product):
        """The order may no more bill this product, whatever else is left.

        Transferring a picking makes the delivery module add a carriage
        charge line to the order, so the order as a whole can still be
        invoiceable; what must never happen again is an invoice line for the
        goods a delivery note already settled.
        """
        try:
            invoice = self.env["account.invoice"].browse(
                order.action_invoice_create())
        except UserError:
            # Nothing invoiceable at all, which is stronger still
            return
        self.assertNotIn(
            product, invoice.invoice_line_ids.mapped("product_id"))

    def _order_line_of(self, order, product):
        return order.order_line.filtered(
            lambda line: line.product_id == product)

    def test_01_auto_line_invoiced(self):
        """A product flagged auto_line_invoiced closes the DdT line at once."""
        ddt = self._create_ddt([self.tax_product])
        line = ddt.line_ids
        self.assertTrue(line.line_invoiced)
        self.assertFalse(line.allow_invoice_line())
        self.assertFalse(line.invoice_line_id)

    def test_02_force_invoiced(self):
        """A DdT line declared invoiced is no more invoiceable."""
        ddt = self._create_ddt([self.product])
        line = ddt.line_ids
        self.assertFalse(line.line_invoiced)
        self.assertTrue(line.allow_invoice_line())

        line.action_declare_invoiced()
        self.assertTrue(line.line_invoiced)
        self.assertFalse(line.allow_invoice_line())

        line.action_undeclare_invoiced()
        self.assertFalse(line.line_invoiced)
        self.assertTrue(line.allow_invoice_line())

    def test_03_invoice_status(self):
        """The DdT carries the same invoice status of a sale order."""
        ddt = self._create_ddt([self.product])
        self.assertEqual(ddt.invoice_status, "no")

        ddt.set_done()
        self.assertEqual(ddt.invoice_status, "to invoice")

        ddt.line_ids.action_declare_invoiced()
        self.assertEqual(ddt.invoice_status, "invoiced")
        # Nothing was really invoiced: no invoice is linked to the DdT
        self.assertFalse(ddt.invoice_id)

        ddt.line_ids.action_undeclare_invoiced()
        self.assertEqual(ddt.invoice_status, "to invoice")

    def test_04_not_to_be_invoiced(self):
        """A DdT which is not to be invoiced has nothing to invoice."""
        ddt = self._create_ddt(
            [self.product], reason=self.reason_not_to_invoice)
        ddt.set_done()
        self.assertFalse(ddt.to_be_invoiced)
        self.assertEqual(ddt.invoice_status, "no")

    def test_05_declared_line_does_not_hold_the_ddt(self):
        """The DdT is closed even if one line was not invoiced.

        Standard action_invoice_create only sets invoice_id when every line
        was invoiced during the run, so a line declared invoiced would leave
        the DdT open forever.
        """
        ddt = self._create_ddt([self.product, self.tax_product])
        ddt.set_done()
        self.assertEqual(ddt.invoice_status, "to invoice")

        invoice_ids = ddt.action_invoice_create()
        invoice = self.env["account.invoice"].browse(invoice_ids)
        # Only the line which is not declared invoiced reached the invoice
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        self.assertEqual(
            invoice.invoice_line_ids.product_id, self.product)
        self.assertFalse(self._line_of(ddt, self.tax_product).invoice_line_id)

        self.assertEqual(ddt.invoice_id, invoice)
        self.assertEqual(ddt.invoice_status, "invoiced")

    def test_06_declared_ddt_is_skipped(self):
        """A DdT with nothing to invoice does not stop the other ones."""
        declared = self._create_ddt([self.product])
        declared.set_done()
        declared.line_ids.action_declare_invoiced()
        to_invoice = self._create_ddt([self.other_product])
        to_invoice.set_done()

        invoice_ids = (declared | to_invoice).action_invoice_create()
        invoice = self.env["account.invoice"].browse(invoice_ids)
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        self.assertEqual(
            invoice.invoice_line_ids.product_id, self.other_product)

        self.assertEqual(to_invoice.invoice_id, invoice)
        self.assertFalse(declared.invoice_id)
        self.assertEqual(declared.invoice_status, "invoiced")

    def test_07_declared_ddt_alone_raises(self):
        """Invoicing a DdT which has nothing to invoice is an error."""
        ddt = self._create_ddt([self.product])
        ddt.set_done()
        ddt.line_ids.action_declare_invoiced()
        with self.assertRaises(UserError):
            ddt.action_invoice_create()

    def test_08_line_invoicing_closes_the_ddt(self):
        """Invoicing line by line closes the DdT as well."""
        ddt = self._create_ddt([self.product, self.other_product])
        ddt.set_done()

        self._line_of(ddt, self.product).action_line_invoice_create()
        self.assertEqual(ddt.invoice_status, "to invoice")
        self.assertFalse(ddt.invoice_id)

        # The remaining line will never be invoiced: declaring it closes the
        # DdT, which keeps the invoice created for the first line
        self._line_of(ddt, self.other_product).action_declare_invoiced()
        self.assertEqual(ddt.invoice_status, "invoiced")
        self.assertEqual(
            ddt.invoice_id,
            self._line_of(ddt, self.product).invoice_line_id.invoice_id)

    def test_09_order_declaration_is_honoured(self):
        """A sale order line declared invoiced is not invoiced from the DdT."""
        order = self._create_order(self.product)
        self.assertTrue(order.picking_ids)
        ddt = self.ddt_model.create(dict(
            self._ddt_values([]),
            picking_ids=[(6, 0, order.picking_ids.ids)]))
        line = ddt.line_ids
        self.assertEqual(line.sale_line_id, order.order_line)
        self.assertTrue(line.allow_invoice_line())

        order.order_line.action_declare_invoiced()
        self.assertTrue(line.line_invoiced)
        self.assertFalse(line.allow_invoice_line())

        order.order_line.action_undeclare_invoiced()
        self.assertFalse(line.line_invoiced)
        self.assertTrue(line.allow_invoice_line())

    def test_10_order_auto_line_invoiced_is_honoured(self):
        """The product policy of the order is honoured on the DdT too."""
        order = self._create_order(self.tax_product)
        ddt = self.ddt_model.create(dict(
            self._ddt_values([]),
            picking_ids=[(6, 0, order.picking_ids.ids)]))
        line = ddt.line_ids
        self.assertEqual(line.sale_line_id, order.order_line)
        self.assertTrue(line.line_invoiced)
        self.assertFalse(line.allow_invoice_line())

    def test_11_invoice_line_wins_over_declarations(self):
        """A line carrying an invoice line is invoiced, whatever is declared.

        The money was billed: no declaration, and no withdrawal of one, can
        undo it.
        """
        ddt = self._create_ddt([self.product])
        ddt.set_done()
        ddt.action_invoice_create()
        line = ddt.line_ids
        self.assertTrue(line.invoice_line_id)
        self.assertTrue(line.line_invoiced)
        self.assertFalse(line.allow_invoice_line())

        # Withdrawing a declaration which was never given must not reopen it
        line.action_undeclare_invoiced()
        self.assertTrue(line.line_invoiced)
        self.assertFalse(line.allow_invoice_line())

    def test_12_deleted_invoice_reopens_the_line(self):
        """Deleting the invoice gives the line back to be invoiced.

        The reference is dropped by the database, so line_invoiced has to
        follow it: a line stuck invoiced could never be billed again.
        """
        ddt = self._create_ddt([self.product])
        ddt.set_done()
        invoice_ids = ddt.action_invoice_create()
        invoice = self.env["account.invoice"].browse(invoice_ids)
        line = ddt.line_ids
        self.assertTrue(line.line_invoiced)
        self.assertEqual(ddt.invoice_status, "invoiced")

        invoice.unlink()
        self.assertFalse(line.invoice_line_id)
        self.assertFalse(line.line_invoiced)
        self.assertFalse(ddt.invoice_id)
        self.assertEqual(ddt.invoice_status, "to invoice")
        self.assertTrue(line.allow_invoice_line())

    def test_13_deleted_invoice_line_reopens_its_line(self):
        """Deleting one invoice line reopens the DdT line which held it.

        The invoice itself survives, so it is its own unlink() which has to
        give the delivery note line back: the other line keeps its invoice
        and the delivery note goes back to be invoiced.
        """
        ddt = self._create_ddt([self.product, self.other_product])
        ddt.set_done()
        ddt.action_invoice_create()
        line = self._line_of(ddt, self.product)
        other = self._line_of(ddt, self.other_product)
        self.assertEqual(ddt.invoice_status, "invoiced")
        self.assertTrue(ddt.invoice_id)

        line.invoice_line_id.unlink()
        self.assertFalse(line.invoice_line_id)
        self.assertFalse(line.line_invoiced)
        self.assertTrue(other.invoice_line_id)
        self.assertTrue(other.line_invoiced)
        self.assertFalse(ddt.invoice_id)
        self.assertEqual(ddt.invoice_status, "to invoice")

    def test_14_invoiced_ddt_lowers_to_be_invoiced(self):
        """Invoicing the delivery note lowers the compatibility flag."""
        ddt = self._create_ddt([self.product])
        ddt.set_done()
        self.assertTrue(ddt.to_be_invoiced)

        ddt.action_invoice_create()
        self.assertEqual(ddt.invoice_status, "invoiced")
        self.assertFalse(ddt.to_be_invoiced)

    def test_15_declared_ddt_lowers_to_be_invoiced(self):
        """A delivery note closed by a declaration lowers the flag too.

        There is no invoice at all here, so the flag is the only thing which
        can keep the mass invoicing wizard away from the document.
        """
        ddt = self._create_ddt([self.product])
        ddt.set_done()
        self.assertTrue(ddt.to_be_invoiced)

        ddt.line_ids.action_declare_invoiced()
        self.assertEqual(ddt.invoice_status, "invoiced")
        self.assertFalse(ddt.to_be_invoiced)
        # This is the domain of the mass invoicing wizard
        self.assertNotIn(ddt, self.ddt_model.search([
            ("to_be_invoiced", "=", True),
            ("invoice_id", "=", False),
            ("state", "=", "done"),
        ]))

        ddt.line_ids.action_undeclare_invoiced()
        self.assertEqual(ddt.invoice_status, "to invoice")
        self.assertTrue(ddt.to_be_invoiced)

    def test_16_deleted_invoice_raises_to_be_invoiced(self):
        """Deleting the invoice gives the delivery note back to be invoiced."""
        ddt = self._create_ddt([self.product])
        ddt.set_done()
        invoice_ids = ddt.action_invoice_create()
        invoice = self.env["account.invoice"].browse(invoice_ids)
        self.assertFalse(ddt.to_be_invoiced)

        invoice.unlink()
        self.assertEqual(ddt.invoice_status, "to invoice")
        self.assertTrue(ddt.to_be_invoiced)

    def test_17_partially_invoiced_keeps_to_be_invoiced(self):
        """The flag stays raised while one line is still to be invoiced."""
        ddt = self._create_ddt([self.product, self.other_product])
        ddt.set_done()

        self._line_of(ddt, self.product).action_line_invoice_create()
        self.assertEqual(ddt.invoice_status, "to invoice")
        self.assertTrue(ddt.to_be_invoiced)

        self._line_of(ddt, self.other_product).action_line_invoice_create()
        self.assertEqual(ddt.invoice_status, "invoiced")
        self.assertFalse(ddt.to_be_invoiced)

    def test_18_ddt_declaration_closes_the_order_line(self):
        """Declaring a DdT line invoiced settles that much of the order.

        Without this the order kept the whole quantity to invoice, and
        invoicing it billed the customer for goods the delivery note had
        declared not to be billed.
        """
        order = self._create_order(self.product)
        ddt = self._ddt_from_pickings(order.picking_ids)
        ddt.set_done()
        line = ddt.line_ids
        sol = self._order_line_of(order, self.product)
        self.assertEqual(line.sale_line_id, sol)
        self.assertEqual(sol.invoice_status, "to invoice")
        self.assertEqual(sol.qty_to_invoice, 10.0)

        line.action_declare_invoiced()
        self.assertEqual(sol.qty_ddt_declared, 10.0)
        self.assertEqual(sol.qty_to_invoice, 0.0)
        self.assertEqual(sol.invoice_status, "invoiced")
        self._assert_product_cannot_be_reinvoiced(order, self.product)

    def test_19_withdrawing_the_declaration_reopens_the_order_line(self):
        """The order line goes back to be invoiced with the declaration."""
        order = self._create_order(self.product)
        ddt = self._ddt_from_pickings(order.picking_ids)
        ddt.set_done()
        sol = self._order_line_of(order, self.product)

        ddt.line_ids.action_declare_invoiced()
        self.assertEqual(sol.invoice_status, "invoiced")

        ddt.line_ids.action_undeclare_invoiced()
        self.assertEqual(sol.qty_ddt_declared, 0.0)
        self.assertEqual(sol.qty_to_invoice, 10.0)
        self.assertEqual(sol.invoice_status, "to invoice")

    def test_20_partial_declaration_leaves_the_rest_to_invoice(self):
        """One declared delivery closes its own quantity and no more.

        Two delivery notes of 4 and 6 on one order line of 10: declaring the
        first invoiced must leave 6 to invoice, which a flag on the order
        line could never express.
        """
        order = self._create_order(self.product)
        sol = self._order_line_of(order, self.product)
        first, backorder = self._deliver(order, 4.0)
        ddt_first = self._ddt_from_pickings(first)
        ddt_first.set_done()
        self.assertEqual(ddt_first.line_ids.product_uom_qty, 4.0)

        ddt_first.line_ids.action_declare_invoiced()
        self.assertEqual(sol.qty_ddt_declared, 4.0)
        self.assertEqual(sol.qty_delivered, 4.0)
        # Everything delivered so far is settled, and the rest of the line
        # is not delivered yet: standard Odoo calls that nothing to invoice
        self.assertEqual(sol.qty_to_invoice, 0.0)
        self.assertEqual(sol.invoice_status, "no")

        self._deliver(order, 6.0)
        ddt_second = self._ddt_from_pickings(backorder)
        ddt_second.set_done()
        self.assertEqual(ddt_second.line_ids.product_uom_qty, 6.0)
        self.assertEqual(sol.qty_delivered, 10.0)
        self.assertEqual(sol.qty_ddt_declared, 4.0)
        self.assertEqual(sol.qty_to_invoice, 6.0)
        self.assertEqual(sol.invoice_status, "to invoice")

    def test_21_partial_declaration_and_partial_invoice(self):
        """A declared delivery and an invoiced one together close the line.

        4 declared on the first delivery note, 6 invoiced on the second: the
        order line is settled, and nothing of it may be invoiced again.
        """
        order = self._create_order(self.product)
        sol = self._order_line_of(order, self.product)
        first, backorder = self._deliver(order, 4.0)
        ddt_first = self._ddt_from_pickings(first)
        ddt_first.set_done()
        ddt_first.line_ids.action_declare_invoiced()

        self._deliver(order, 6.0)
        ddt_second = self._ddt_from_pickings(backorder)
        ddt_second.set_done()
        ddt_second.action_invoice_create()

        self.assertEqual(sol.qty_ddt_declared, 4.0)
        self.assertEqual(sol.qty_invoiced, 6.0)
        self.assertEqual(sol.qty_to_invoice, 0.0)
        self.assertEqual(sol.invoice_status, "invoiced")
        self._assert_product_cannot_be_reinvoiced(order, self.product)

    def test_22_invoiced_ddt_line_is_not_counted_twice(self):
        """A line which reached the invoice is counted by qty_invoiced only.

        force_invoiced set on a line which was invoiced anyway must not take
        its quantity off a second time: _is_line_invoiced() checks the
        invoice line first, and the declared quantity has to agree.
        """
        order = self._create_order(self.product)
        sol = self._order_line_of(order, self.product)
        ddt = self._ddt_from_pickings(order.picking_ids)
        ddt.set_done()
        ddt.action_invoice_create()
        self.assertEqual(sol.qty_invoiced, 10.0)

        ddt.line_ids.write({"force_invoiced": True})
        self.assertEqual(sol.qty_ddt_declared, 0.0)
        self.assertEqual(sol.qty_invoiced, 10.0)
        self.assertEqual(sol.qty_to_invoice, 0.0)

    def test_23_order_declaration_is_not_counted_twice(self):
        """A DdT line closed by the order itself adds no declared quantity.

        The order line already zeroes what is left to invoice, so counting
        the delivery note again would take the same goods off twice.
        """
        order = self._create_order(self.product)
        sol = self._order_line_of(order, self.product)
        ddt = self._ddt_from_pickings(order.picking_ids)
        ddt.set_done()

        sol.action_declare_invoiced()
        self.assertTrue(ddt.line_ids.line_invoiced)
        self.assertEqual(sol.qty_ddt_declared, 0.0)
        self.assertEqual(sol.qty_to_invoice, 0.0)
        self.assertEqual(sol.invoice_status, "invoiced")
