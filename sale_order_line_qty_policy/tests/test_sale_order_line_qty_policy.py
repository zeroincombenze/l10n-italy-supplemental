# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from odoo.tests.common import TransactionCase


class TestSaleOrderLineQtyPolicy(TransactionCase):

    # Sale order creation needs the fields declared by sale_stock, which is
    # not a dependency of this module: run once the whole registry is loaded.
    at_install = False
    post_install = True

    def setUp(self):
        super(TestSaleOrderLineQtyPolicy, self).setUp()
        self.order_model = self.env["sale.order"]
        self.customer = self.env["res.partner"].create({
            "name": "Test Qty Policy Customer",
            "customer": True,
        })
        # Standard product, invoiced on delivered quantity
        self.product = self._create_product("Test bulk product", {
            "invoice_policy": "delivery",
            "delivered_threshold": 2.0,
        })
        # Product without any policy
        self.plain_product = self._create_product("Test plain product", {
            "invoice_policy": "delivery",
        })
        # Product recomputed at invoice level, i.e. CONAI contribution
        self.tax_product = self._create_product("Test CONAI product", {
            "invoice_policy": "order",
            "auto_line_invoiced": True,
        })
        # Same threshold, but invoiced on ordered quantity
        self.ordered_product = self._create_product("Test ordered product", {
            "invoice_policy": "order",
            "delivered_threshold": 2.0,
        })
        # Threshold declared on the category, not on the product
        self.categ = self.env["product.category"].create({
            "name": "Test threshold category",
            "delivered_threshold": 3.0,
        })
        self.categ_product = self._create_product("Test category product", {
            "invoice_policy": "delivery",
            "categ_id": self.categ.id,
        })
        # Product overriding the threshold of its own category
        self.override_product = self._create_product("Test override product", {
            "invoice_policy": "delivery",
            "categ_id": self.categ.id,
            "delivered_threshold": 1.0,
        })

    def _create_product(self, name, vals):
        values = {
            "name": name,
            "type": "service",
            "track_service": "manual",
        }
        values.update(vals)
        return self.env["product.product"].create(values)

    def _create_consu_product(self, name, vals):
        values = {
            "name": name,
            "type": "consu",
        }
        values.update(vals)
        return self.env["product.product"].create(values)

    def _create_order(self, product, qty=100.0):
        order = self.order_model.create({
            "partner_id": self.customer.id,
            "order_line": [(0, 0, {
                "product_id": product.id,
                "name": product.name,
                "product_uom_qty": qty,
                "product_uom": product.uom_id.id,
                "price_unit": 10.0,
            })],
        })
        order.action_confirm()
        return order

    def _invoice(self, order):
        order.action_invoice_create()
        return order.invoice_ids

    def test_01_auto_line_invoiced(self):
        """A product flagged auto_line_invoiced closes the line at once."""
        order = self._create_order(self.tax_product)
        line = order.order_line
        self.assertTrue(line.product_id.auto_line_invoiced)
        self.assertEqual(line.qty_to_invoice, 0.0)
        self.assertEqual(line.invoice_status, "invoiced")
        self.assertEqual(order.invoice_status, "invoiced")

    def test_02_force_invoiced(self):
        """A line manually declared invoiced is no more to invoice."""
        order = self._create_order(self.plain_product)
        line = order.order_line
        line.qty_delivered = 40.0
        self.assertEqual(line.qty_to_invoice, 40.0)
        self.assertEqual(line.invoice_status, "to invoice")

        line.action_declare_invoiced()
        self.assertEqual(line.qty_to_invoice, 0.0)
        self.assertEqual(line.invoice_status, "invoiced")
        self.assertEqual(order.invoice_status, "invoiced")

        line.action_undeclare_invoiced()
        self.assertEqual(line.qty_to_invoice, 40.0)
        self.assertEqual(line.invoice_status, "to invoice")

    def test_03_force_delivered(self):
        """A line manually declared delivered is flagged as such."""
        order = self._create_order(self.plain_product)
        line = order.order_line
        line.qty_delivered = 40.0
        self.assertFalse(line.line_delivered)

        line.action_declare_delivered()
        self.assertTrue(line.line_delivered)
        # Delivered quantity is never altered
        self.assertEqual(line.qty_delivered, 40.0)

        line.action_undeclare_delivered()
        self.assertFalse(line.line_delivered)

    def test_04_threshold_under_delivery(self):
        """Under delivery within threshold closes the line once invoiced."""
        order = self._create_order(self.product)
        line = order.order_line
        # 1% less than ordered, threshold is 2%
        line.qty_delivered = 99.0
        self.assertTrue(line.line_delivered)
        # Still to invoice: nothing has been invoiced yet
        self.assertEqual(line.qty_to_invoice, 99.0)
        self.assertEqual(line.invoice_status, "to invoice")

        self._invoice(order)
        # Customer is invoiced for the delivered quantity, not the ordered one
        self.assertEqual(line.qty_invoiced, 99.0)
        self.assertEqual(line.qty_to_invoice, 0.0)
        self.assertEqual(line.invoice_status, "invoiced")
        self.assertEqual(order.invoice_status, "invoiced")

    def test_05_threshold_over_delivery(self):
        """Over delivery closes the line, whatever the threshold is."""
        order = self._create_order(self.product)
        line = order.order_line
        line.qty_delivered = 101.0
        self.assertTrue(line.line_delivered)

        self._invoice(order)
        self.assertEqual(line.qty_invoiced, 101.0)
        self.assertEqual(line.invoice_status, "invoiced")

    def test_06_threshold_exceeded(self):
        """Deviation greater than threshold keeps standard behaviour."""
        order = self._create_order(self.product)
        line = order.order_line
        # 5% less than ordered, threshold is 2%
        line.qty_delivered = 95.0
        self.assertFalse(line.line_delivered)

        self._invoice(order)
        self.assertEqual(line.qty_invoiced, 95.0)
        self.assertEqual(line.qty_to_invoice, 0.0)
        # Standard Odoo leaves the line open
        self.assertEqual(line.invoice_status, "no")

    def test_07_upselling_within_threshold(self):
        """Over delivery within threshold is not an upselling occasion."""
        order = self._create_order(self.ordered_product)
        line = order.order_line
        self._invoice(order)
        self.assertEqual(line.qty_invoiced, 100.0)
        self.assertEqual(line.invoice_status, "invoiced")

        # 1% more than ordered, threshold is 2%: standard Odoo would now
        # switch the line to 'upselling'
        line.qty_delivered = 101.0
        self.assertEqual(line.invoice_status, "invoiced")

        # 5% more than ordered: out of threshold, standard behaviour applies
        line.qty_delivered = 105.0
        self.assertEqual(line.invoice_status, "upselling")

    def test_08_threshold_from_category(self):
        """A product without threshold inherits the one of its category."""
        order = self._create_order(self.categ_product)
        line = order.order_line
        self.assertEqual(line._get_delivered_threshold(), 3.0)

        # 2% less than ordered, category threshold is 3%
        line.qty_delivered = 98.0
        self.assertTrue(line.line_delivered)

        # 5% less than ordered: out of the category threshold
        line.qty_delivered = 95.0
        self.assertFalse(line.line_delivered)

    def test_09_product_overrides_category(self):
        """The threshold of the product wins over the one of its category."""
        order = self._create_order(self.override_product)
        line = order.order_line
        self.assertEqual(line._get_delivered_threshold(), 1.0)

        # Within the category threshold (3%) but out of the product one (1%)
        line.qty_delivered = 98.0
        self.assertFalse(line.line_delivered)

        line.qty_delivered = 99.5
        self.assertTrue(line.line_delivered)

    def test_10_force_delivery_state_set_by_policy(self):
        """The order flag is set when every relevant line is delivered."""
        product = self._create_consu_product("Test consu product", {
            "invoice_policy": "order",
            "categ_id": self.categ.id,
        })
        order = self._create_order(product)
        line = order.order_line
        self.assertFalse(order.force_delivery_state)

        # 0.3% less than ordered, category threshold is 3%
        line.qty_delivered = 99.7
        self.assertTrue(line.line_delivered)
        self.assertTrue(order.force_delivery_state)
        self.assertFalse(order.force_delivery_state_manual)

        # Out of threshold again: the policy clears what the policy had set
        line.qty_delivered = 50.0
        self.assertFalse(line.line_delivered)
        self.assertFalse(order.force_delivery_state)
        self.assertFalse(order.force_delivery_state_manual)

    def test_11_force_delivery_state_manual_is_kept(self):
        """A flag set by hand is never cleared by the policy."""
        product = self._create_consu_product("Test manual consu", {
            "invoice_policy": "order",
            "categ_id": self.categ.id,
        })
        order = self._create_order(product)
        line = order.order_line

        order.write({"force_delivery_state": True})
        self.assertTrue(order.force_delivery_state_manual)

        # Far out of threshold: the policy must not touch the manual flag
        line.qty_delivered = 10.0
        self.assertFalse(line.line_delivered)
        self.assertTrue(order.force_delivery_state)

    def test_12_service_lines_are_skipped(self):
        """Services and lines without product do not block the order."""
        product = self._create_consu_product("Test consu with service", {
            "invoice_policy": "order",
            "categ_id": self.categ.id,
        })
        order = self._create_order(product)
        order.write({"order_line": [(0, 0, {
            "product_id": self.plain_product.id,
            "name": self.plain_product.name,
            "product_uom_qty": 1.0,
            "product_uom": self.plain_product.uom_id.id,
            "price_unit": 5.0,
        })]})
        service_line = order.order_line.filtered(
            lambda l: l.product_id == self.plain_product)
        self.assertEqual(service_line.product_id.type, "service")
        self.assertFalse(service_line._is_qty_policy_line())

        order.order_line.filtered(
            lambda l: l.product_id == product).qty_delivered = 99.7
        self.assertTrue(order.force_delivery_state)

    def test_13_stale_flag_is_taken_back(self):
        """A flag with no ownership marker belongs to the policy again.

        This is the situation left behind by a lost force_delivery_state_manual
        column: the flag must not stay stuck on an undelivered order.
        """
        product = self._create_consu_product("Test stale consu", {
            "invoice_policy": "order",
            "categ_id": self.categ.id,
        })
        order = self._create_order(product)
        # Simulate the stale value: flag set, ownership unknown
        order.write({
            "force_delivery_state": True,
            "force_delivery_state_manual": False,
        })
        self.assertFalse(order.order_line.line_delivered)

        order._update_force_delivery_state()
        self.assertFalse(order.force_delivery_state)

    def test_14_reset_to_draft_resyncs_delivered(self):
        """Reset to draft writes back the real delivered quantity."""
        product = self._create_consu_product("Test draft consu", {
            "invoice_policy": "order",
            "categ_id": self.categ.id,
        })
        order = self._create_order(product)
        line = order.order_line
        line.qty_delivered = 99.7
        self.assertTrue(line.line_delivered)
        self.assertTrue(order.force_delivery_state)

        order.action_cancel()
        order.action_draft()
        self.assertEqual(order.state, "draft")
        # No done stock move is linked to the line any more
        self.assertEqual(line.qty_delivered, 0.0)
        self.assertFalse(line.line_delivered)
        self.assertFalse(order.force_delivery_state)

    def test_15_reset_to_draft_keeps_service_qty(self):
        """A manually entered delivered quantity is not wiped."""
        order = self._create_order(self.plain_product)
        line = order.order_line
        line.qty_delivered = 40.0

        order.action_cancel()
        order.action_draft()
        self.assertEqual(order.state, "draft")
        self.assertEqual(line.qty_delivered, 40.0)

    def test_16_no_policy_no_change(self):
        """Without any policy the standard behaviour is untouched."""
        order = self._create_order(self.plain_product)
        line = order.order_line
        line.qty_delivered = 99.0
        self.assertFalse(line.line_delivered)
        self.assertEqual(line.invoice_status, "to invoice")

        self._invoice(order)
        self.assertEqual(line.invoice_status, "no")
