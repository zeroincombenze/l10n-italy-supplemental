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
