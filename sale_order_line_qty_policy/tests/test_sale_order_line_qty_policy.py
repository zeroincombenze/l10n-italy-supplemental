# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from .testenv import MainTest as SingleTransactionCase

TEST_RES_PARTNER = {
    "z0bug.customer": {
        "name": "Test Qty Policy Customer",
        "customer": True,
    },
}

TEST_PRODUCT_CATEGORY = {
    # No threshold declared on the product itself: it inherits this one
    "z0bug.threshold_categ": {
        "name": "Test threshold category",
        "delivered_threshold": 3.0,
    },
}

TEST_PRODUCT_TEMPLATE = {
    # Product recomputed at invoice level, i.e. CONAI contribution
    "z0bug.conai_template": {
        "name": "Test CONAI product",
        "type": "service",
        "track_service": "manual",
        "invoice_policy": "order",
        "auto_line_invoiced": True,
    },
    # Product without any policy
    "z0bug.plain_template": {
        "name": "Test plain product",
        "type": "service",
        "track_service": "manual",
        "invoice_policy": "delivery",
    },
    # Standard product, invoiced on delivered quantity
    "z0bug.bulk_template": {
        "name": "Test bulk product",
        "type": "service",
        "track_service": "manual",
        "invoice_policy": "delivery",
        "delivered_threshold": 2.0,
    },
    # Same threshold, but invoiced on ordered quantity
    "z0bug.ordered_template": {
        "name": "Test ordered product",
        "type": "service",
        "track_service": "manual",
        "invoice_policy": "order",
        "delivered_threshold": 2.0,
    },
    # Threshold declared on the category, not on the product
    "z0bug.categ_template": {
        "name": "Test category product",
        "type": "service",
        "track_service": "manual",
        "invoice_policy": "delivery",
        "categ_id": "z0bug.threshold_categ",
    },
    # Product overriding the threshold of its own category
    "z0bug.override_template": {
        "name": "Test override product",
        "type": "service",
        "track_service": "manual",
        "invoice_policy": "delivery",
        "categ_id": "z0bug.threshold_categ",
        "delivered_threshold": 1.0,
    },
    # Stockable product, delivered quantity comes from stock moves
    "z0bug.consu_template": {
        "name": "Test consu product",
        "type": "consu",
        "invoice_policy": "order",
        "categ_id": "z0bug.threshold_categ",
    },
}

TEST_SALE_ORDER = {
    "z0bug.order_01": {"partner_id": "z0bug.customer"},
    "z0bug.order_02": {"partner_id": "z0bug.customer"},
    "z0bug.order_03": {"partner_id": "z0bug.customer"},
    "z0bug.order_04": {"partner_id": "z0bug.customer"},
    "z0bug.order_05": {"partner_id": "z0bug.customer"},
    "z0bug.order_06": {"partner_id": "z0bug.customer"},
    "z0bug.order_07": {"partner_id": "z0bug.customer"},
    "z0bug.order_08": {"partner_id": "z0bug.customer"},
    "z0bug.order_09": {"partner_id": "z0bug.customer"},
    "z0bug.order_10": {"partner_id": "z0bug.customer"},
    "z0bug.order_11": {"partner_id": "z0bug.customer"},
    "z0bug.order_12": {"partner_id": "z0bug.customer"},
    "z0bug.order_13": {"partner_id": "z0bug.customer"},
    "z0bug.order_14": {"partner_id": "z0bug.customer"},
    "z0bug.order_15": {"partner_id": "z0bug.customer"},
    "z0bug.order_16": {"partner_id": "z0bug.customer"},
}

TEST_SALE_ORDER_LINE = {
    "z0bug.order_01_1": {
        "product_id": "z0bug.conai_product",
        "name": "Test CONAI product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_02_1": {
        "product_id": "z0bug.plain_product",
        "name": "Test plain product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_03_1": {
        "product_id": "z0bug.plain_product",
        "name": "Test plain product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_04_1": {
        "product_id": "z0bug.bulk_product",
        "name": "Test bulk product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_05_1": {
        "product_id": "z0bug.bulk_product",
        "name": "Test bulk product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_06_1": {
        "product_id": "z0bug.bulk_product",
        "name": "Test bulk product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_07_1": {
        "product_id": "z0bug.ordered_product",
        "name": "Test ordered product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_08_1": {
        "product_id": "z0bug.categ_product",
        "name": "Test category product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_09_1": {
        "product_id": "z0bug.override_product",
        "name": "Test override product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_10_1": {
        "product_id": "z0bug.consu_product",
        "name": "Test consu product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_11_1": {
        "product_id": "z0bug.consu_product",
        "name": "Test consu product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_12_1": {
        "product_id": "z0bug.consu_product",
        "name": "Test consu product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_12_2": {
        "product_id": "z0bug.plain_product",
        "name": "Test plain product",
        "product_uom_qty": 1.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 5.0,
    },
    "z0bug.order_13_1": {
        "product_id": "z0bug.consu_product",
        "name": "Test consu product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_14_1": {
        "product_id": "z0bug.consu_product",
        "name": "Test consu product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_15_1": {
        "product_id": "z0bug.plain_product",
        "name": "Test plain product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
    "z0bug.order_16_1": {
        "product_id": "z0bug.plain_product",
        "name": "Test plain product",
        "product_uom_qty": 100.0,
        "product_uom": "product.product_uom_unit",
        "price_unit": 10.0,
    },
}

TEST_SETUP_LIST = [
    "res.partner",
    "product.category",
    "product.template",
    "sale.order",
    "sale.order.line",
]


class TestSaleOrderLineQtyPolicy(SingleTransactionCase):

    # Sale order creation needs the fields declared by sale_stock, which is
    # not a dependency of this module: run once the whole registry is loaded.
    at_install = False
    post_install = True

    def setUp(self):
        super(TestSaleOrderLineQtyPolicy, self).setUp()
        self.debug_level = 0
        self.odoo_commit_test = True
        self.setup_env()  # Create test environment

    def tearDown(self):
        super(TestSaleOrderLineQtyPolicy, self).tearDown()

    def test_01_auto_line_invoiced(self):
        """A product flagged auto_line_invoiced closes the line at once."""
        order = self.resource_browse("z0bug.order_01")
        order.action_confirm()
        line = order.order_line
        self.assertTrue(line.product_id.auto_line_invoiced)
        self.assertEqual(line.qty_to_invoice, 0.0)
        self.assertEqual(line.invoice_status, "invoiced")
        self.assertEqual(order.invoice_status, "invoiced")

    def test_02_force_invoiced(self):
        """A line manually declared invoiced is no more to invoice."""
        order = self.resource_browse("z0bug.order_02")
        order.action_confirm()
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
        order = self.resource_browse("z0bug.order_03")
        order.action_confirm()
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
        order = self.resource_browse("z0bug.order_04")
        order.action_confirm()
        line = order.order_line
        # 1% less than ordered, threshold is 2%
        line.qty_delivered = 99.0
        self.assertTrue(line.line_delivered)
        # Still to invoice: nothing has been invoiced yet
        self.assertEqual(line.qty_to_invoice, 99.0)
        self.assertEqual(line.invoice_status, "to invoice")

        order.action_invoice_create()
        # Customer is invoiced for the delivered quantity, not the ordered one
        self.assertEqual(line.qty_invoiced, 99.0)
        self.assertEqual(line.qty_to_invoice, 0.0)
        self.assertEqual(line.invoice_status, "invoiced")
        self.assertEqual(order.invoice_status, "invoiced")

    def test_05_threshold_over_delivery(self):
        """Over delivery closes the line, whatever the threshold is."""
        order = self.resource_browse("z0bug.order_05")
        order.action_confirm()
        line = order.order_line
        line.qty_delivered = 101.0
        self.assertTrue(line.line_delivered)

        order.action_invoice_create()
        self.assertEqual(line.qty_invoiced, 101.0)
        self.assertEqual(line.invoice_status, "invoiced")

    def test_06_threshold_exceeded(self):
        """Deviation greater than threshold keeps standard behaviour."""
        order = self.resource_browse("z0bug.order_06")
        order.action_confirm()
        line = order.order_line
        # 5% less than ordered, threshold is 2%
        line.qty_delivered = 95.0
        self.assertFalse(line.line_delivered)

        order.action_invoice_create()
        self.assertEqual(line.qty_invoiced, 95.0)
        self.assertEqual(line.qty_to_invoice, 0.0)
        # Standard Odoo leaves the line open
        self.assertEqual(line.invoice_status, "no")

    def test_07_upselling_within_threshold(self):
        """Over delivery within threshold is not an upselling occasion."""
        order = self.resource_browse("z0bug.order_07")
        order.action_confirm()
        line = order.order_line
        order.action_invoice_create()
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
        order = self.resource_browse("z0bug.order_08")
        order.action_confirm()
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
        order = self.resource_browse("z0bug.order_09")
        order.action_confirm()
        line = order.order_line
        self.assertEqual(line._get_delivered_threshold(), 1.0)

        # Within the category threshold (3%) but out of the product one (1%)
        line.qty_delivered = 98.0
        self.assertFalse(line.line_delivered)

        line.qty_delivered = 99.5
        self.assertTrue(line.line_delivered)

    def test_10_force_delivery_state_set_by_policy(self):
        """The order flag is set when every relevant line is delivered."""
        order = self.resource_browse("z0bug.order_10")
        order.action_confirm()
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
        order = self.resource_browse("z0bug.order_11")
        order.action_confirm()
        line = order.order_line

        order.write({"force_delivery_state": True})
        self.assertTrue(order.force_delivery_state_manual)

        # Far out of threshold: the policy must not touch the manual flag
        line.qty_delivered = 10.0
        self.assertFalse(line.line_delivered)
        self.assertTrue(order.force_delivery_state)

    def test_12_service_lines_are_skipped(self):
        """Services and lines without product do not block the order."""
        order = self.resource_browse("z0bug.order_12")
        order.action_confirm()
        service_line = order.order_line.filtered(
            lambda l: l.product_id == self.resource_browse("z0bug.plain_product"))
        self.assertEqual(service_line.product_id.type, "service")
        self.assertFalse(service_line._is_qty_policy_line())

        consu_line = order.order_line.filtered(
            lambda l: l.product_id == self.resource_browse("z0bug.consu_product"))
        consu_line.qty_delivered = 99.7
        self.assertTrue(order.force_delivery_state)

    def test_13_stale_flag_is_taken_back(self):
        """A flag with no ownership marker belongs to the policy again.

        This is the situation left behind by a lost force_delivery_state_manual
        column: the flag must not stay stuck on an undelivered order.
        """
        order = self.resource_browse("z0bug.order_13")
        order.action_confirm()
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
        order = self.resource_browse("z0bug.order_14")
        order.action_confirm()
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
        order = self.resource_browse("z0bug.order_15")
        order.action_confirm()
        line = order.order_line
        line.qty_delivered = 40.0

        order.action_cancel()
        order.action_draft()
        self.assertEqual(order.state, "draft")
        self.assertEqual(line.qty_delivered, 40.0)

    def test_16_no_policy_no_change(self):
        """Without any policy the standard behaviour is untouched."""
        order = self.resource_browse("z0bug.order_16")
        order.action_confirm()
        line = order.order_line
        line.qty_delivered = 99.0
        self.assertFalse(line.line_delivered)
        self.assertEqual(line.invoice_status, "to invoice")

        order.action_invoice_create()
        self.assertEqual(line.invoice_status, "no")
