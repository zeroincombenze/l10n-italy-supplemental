# -*- coding: utf-8 -*-
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)


TEST_SETUP_LIST = [
    "account.account",
    "account.tax",
    "account.journal",
    "product.template",
    "res.partner",
    "sale.order",
    "sale.order.line",
    "purchase.order",
    "purchase.order.line",
    "account.invoice",
    "account.invoice.line",
]


class TestInvoiceRound(SingleTransactionCase):
    def setUp(self):
        super(TestInvoiceRound, self).setUp()
        # Add following statement just for get debug information
        self.debug_level = 0
        self.odoo_commit_test = True
        self.setup_company(
            self.default_company(),
            xref="z0bug.mycompany",
            partner_xref="z0bug.partner_mycompany",
            recv_xref="z0bug.coa_recv",
            values={
                "name": "Test Company",
                "vat": "IT05111810015",
                "country_id": "base.it",
                "report_model_style": "base.multi_report.mr_style_odoo",
            },
        )
        self.setup_env()

    def tearDown(self):
        super(TestInvoiceRound, self).tearDown()

    def _test_1_sale(self):
        _logger.info("🎺 Test print sale order")
        xref = "z0bug.sale_Z0_9"
        sale = self.resource_browse(xref=xref)
        action = self.resource_edit(sale, actions=["print_quotation"])
        self.assertEqual(
            "ir.actions.report.xml",
            action.get("type")
        )
        # Warning: for weird reason follow test fails inside pycharm debug
        self.assertEqual(
            "base_multireport.report_saleorder",
            action.get("reportname")
        )
        rpt_text = self.env["ir.actions.report.xml"].render_report(
            sale.ids,
            action.get("reportname", action.get("report_name")),
            action.get("data") or {}
        )
        self.assertIn(
            "<!DOCTYPE html>",
            unicode(rpt_text,)
        )

    def _test_1_picking(self):
        _logger.info("🎺 Test print picking order")
        xref = "z0bug.sale_Z0_9"
        sale = self.resource_browse(xref=xref)
        sale.action_confirm()
        for picking in sale.picking_ids:
            if picking.state not in ("cancel", "done"):
                break
        action = self.resource_edit(picking, actions=["do_print_picking"])
        self.assertEqual(
            "ir.actions.report.xml",
            action.get("type")
        )
        rpt_text = self.env["ir.actions.report.xml"].render_report(
            picking.ids,
            action.get("reportname", action.get("report_name")),
            action.get("data") or {}
        )
        self.assertIn(
            "<!DOCTYPE html>",
            unicode(rpt_text,)
        )

    def _test_1_delivery_note(self):
        _logger.info("🎺 Test print delivery note")
        xref = "z0bug.sale_Z0_9"
        sale = self.resource_browse(xref=xref)
        self.resource_edit(sale, actions=["action_create_ddt"])
        ddt = sale.ddt_ids[0]
        self.resource_edit(
            ddt,
            web_changes=[
                ("carriage_condition_id", "l10n_it_ddt.carriage_condition_PA"),
                ("goods_description_id", "l10n_it_ddt.goods_description_CAR"),
                ("transportation_reason_id", "l10n_it_ddt.transportation_reason_VEN"),
                ("transportation_method_id", "l10n_it_ddt.transportation_method_MIT"),
            ],
            actions=["save", "set_done"]
        )
        rpt_text = self.env["ir.actions.report.xml"].render_report(
            ddt.ids,
            "base_multireport.report_ddt_main",
            {}
        )
        self.assertIn(
            "<!DOCTYPE html>",
            unicode(rpt_text,)
        )

    def _test_1_purchase(self):
        _logger.info("🎺 Test print purchase order")
        xref = "z0bug.purchase_order_Z0_1"
        order = self.resource_browse(xref=xref)
        action = self.resource_edit(order, actions=["print_quotation"])
        self.assertEqual(
            "ir.actions.report.xml",
            action.get("type")
        )
        rpt_text = self.env["ir.actions.report.xml"].render_report(
            order.ids,
            action.get("reportname", action.get("report_name")),
            action.get("data") or {}
        )
        self.assertIn(
            "<!DOCTYPE html>",
            unicode(rpt_text,)
        )

    def _test_1_invoice(self):
        _logger.info("🎺 Test print invoice")
        xref = "z0bug.invoice_Z0_9"
        invoice = self.resource_browse(xref=xref)
        action = self.resource_edit(
            invoice, actions=["action_invoice_open", "invoice_print"])
        self.assertEqual(
            "ir.actions.report.xml",
            action.get("type")
        )
        rpt_text = self.env["ir.actions.report.xml"].render_report(
            invoice.ids,
            action.get("reportname", action.get("report_name")),
            action.get("data") or {}
        )
        self.assertIn(
            "<!DOCTYPE html>",
            unicode(rpt_text,)
        )

    def _test_2_invoice(self):
        _logger.info("🎺 Test print invoice")
        xref = "z0bug.sale_Z0_9"
        sale = self.resource_browse(xref=xref)
        ddt = sale.ddt_ids[0]
        inv_ids = ddt.action_invoice_create()
        invoice = self.env["account.invoice"].browse(inv_ids[0])
        action = self.resource_edit(
            invoice, actions=["action_invoice_open", "invoice_print"])
        self.assertEqual(
            "ir.actions.report.xml",
            action.get("type")
        )
        rpt_text = self.env["ir.actions.report.xml"].render_report(
            invoice.ids,
            action.get("reportname", action.get("report_name")),
            action.get("data") or {}
        )
        self.assertIn(
            "<!DOCTYPE html>",
            unicode(rpt_text,)
        )

    def _test_1_overdue(self):
        _logger.info("🎺 Test print overdue")
        xref = "z0bug.invoice_Z0_9"
        invoice = self.resource_browse(xref=xref)
        partner = invoice.partner_id
        rpt_text = self.env["ir.actions.report.xml"].render_report(
            partner.ids,
            "base_multireport.report_overdue",
            {}
        )
        self.assertIn(
            "<!DOCTYPE html>",
            unicode(rpt_text,)
        )

    def test_print(self):
        _logger.info("🎺🎺 Testing Document Print")
        self._test_1_sale()
        self._test_1_purchase()
        self._test_1_picking()
        self._test_1_delivery_note()
        self._test_1_invoice()
        self._test_2_invoice()
        self._test_1_overdue()
