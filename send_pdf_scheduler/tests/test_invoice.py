# -*- coding: utf-8 -*-
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)


TEST_ACCOUNT_FISCAL_POSITION = {
    "z0bug.fiscalpos_it": {
        "name": "Italia",
    },
}

TEST_ACCOUNT_INVOICE = {
    "z0bug.invoice_Z0_1": {
        "type": "out_invoice",
        "date_invoice": "####-<#-99",
        "partner_id": "base.res_partner_1",
    },
}

TEST_ACCOUNT_INVOICE_LINE = {
    "z0bug.invoice_Z0_1_1": {
        "invoice_id": "z0bug.invoice_Z0_1",
        "price_unit": 0.84,
        "account_id": "l10n_generic_coa.1_conf_a_sale",
        "name": "Prodotto Alpha",
        "invoice_line_tax_ids": "l10n_generic_coa.1_sale_tax_template",
        "quantity": 100,
    },
}

TEST_SETUP_LIST = [
    "account.fiscal.position",
    "account.invoice",
    "account.invoice.line",
]


class TestInvoice(SingleTransactionCase):

    def setUp(self):
        super(TestInvoice, self).setUp()
        self.debug_level = 0
        # self.odoo_commit_test = True
        self.setup_company(
            self.default_company(),
            xref="z0bug.mycompany",
            partner_xref="z0bug.partner_mycompany",
            recv_xref="z0bug.coa_recv",
            pay_xref="z0bug.coa_pay",
            values={
                "name": "Test Company",
                "vat": "IT05111810015",
                "country_id": "base.it",
            },
        )
        self.setup_env()                            # Create test environment

    def tearDown(self):
        super(TestInvoice, self).tearDown()

    def _test_01_invoice(self):
        self.log_lvl_1(u"🎺 Testing Default = True")
        IrConfigParameter = self.env["ir.config_parameter"]
        IrConfigParameter.set_param("default_to_send_mail", True)
        fiscalpos = self.resource_browse(xref="z0bug.fiscalpos_it")
        fiscalpos.write({"to_send_mail": False})
        partner = self.resource_browse(xref="base.res_partner_1")
        partner.write({"to_send_mail": False})
        xref = "z0bug.invoice_Z0_1"
        invoice = self.resource_browse(xref=xref)
        invoice.unlink()
        invoice = self.resource_create("account.invoice", xref=xref)
        self.resource_edit(
            invoice,
            web_changes=[("fiscal_position_id", "z0bug.fiscalpos_it")]
        )
        self.assertTrue(invoice.to_send_mail)

    def _test_02_invoice(self):
        self.log_lvl_1(u"🎺 Testing Fiscalpos = True")
        IrConfigParameter = self.env["ir.config_parameter"]
        IrConfigParameter.set_param("default_to_send_mail", False)
        fiscalpos = self.resource_browse(xref="z0bug.fiscalpos_it")
        fiscalpos.write({"to_send_mail": "enable"})
        partner = self.resource_browse(xref="base.res_partner_1")
        partner.write({"to_send_mail": False})
        xref = "z0bug.invoice_Z0_1"
        invoice = self.resource_browse(xref=xref)
        invoice.unlink()
        invoice = self.resource_create("account.invoice", xref=xref)
        self.resource_edit(
            invoice,
            web_changes=[("fiscal_position_id", "z0bug.fiscalpos_it")]
        )
        self.assertTrue(invoice.to_send_mail)

    def _test_03_invoice(self):
        self.log_lvl_1(u"🎺 Testing Partner = True")
        IrConfigParameter = self.env["ir.config_parameter"]
        IrConfigParameter.set_param("default_to_send_mail", False)
        fiscalpos = self.resource_browse(xref="z0bug.fiscalpos_it")
        fiscalpos.write({"to_send_mail": "disable"})
        partner = self.resource_browse(xref="base.res_partner_1")
        partner.write({"to_send_mail": "enable"})
        xref = "z0bug.invoice_Z0_1"
        invoice = self.resource_browse(xref=xref)
        invoice.unlink()
        invoice = self.resource_create("account.invoice", xref=xref)
        self.resource_edit(
            invoice,
            web_changes=[("fiscal_position_id", "z0bug.fiscalpos_it")]
        )
        self.assertTrue(invoice.to_send_mail)

    def _test_04_invoice(self):
        self.log_lvl_1(u"🎺 Testing Default = Falase")
        IrConfigParameter = self.env["ir.config_parameter"]
        IrConfigParameter.set_param("default_to_send_mail", False)
        fiscalpos = self.resource_browse(xref="z0bug.fiscalpos_it")
        fiscalpos.write({"to_send_mail": False})
        partner = self.resource_browse(xref="base.res_partner_1")
        partner.write({"to_send_mail": False})
        xref = "z0bug.invoice_Z0_1"
        invoice = self.resource_browse(xref=xref)
        invoice.unlink()
        invoice = self.resource_create("account.invoice", xref=xref)
        self.resource_edit(
            invoice,
            web_changes=[("fiscal_position_id", "z0bug.fiscalpos_it")]
        )
        self.assertFalse(invoice.to_send_mail)

    def _test_05_invoice(self):
        self.log_lvl_1(u"🎺 Testing Fiscalpos = False")
        IrConfigParameter = self.env["ir.config_parameter"]
        IrConfigParameter.set_param("default_to_send_mail", True)
        fiscalpos = self.resource_browse(xref="z0bug.fiscalpos_it")
        fiscalpos.write({"to_send_mail": "disable"})
        partner = self.resource_browse(xref="base.res_partner_1")
        partner.write({"to_send_mail": False})
        xref = "z0bug.invoice_Z0_1"
        invoice = self.resource_browse(xref=xref)
        invoice.unlink()
        invoice = self.resource_create("account.invoice", xref=xref)
        self.resource_edit(
            invoice,
            web_changes=[("fiscal_position_id", "z0bug.fiscalpos_it")]
        )
        self.assertFalse(invoice.to_send_mail)

    def _test_06_invoice(self):
        self.log_lvl_1(u"🎺 Testing Partner = True")
        IrConfigParameter = self.env["ir.config_parameter"]
        IrConfigParameter.set_param("default_to_send_mail", True)
        fiscalpos = self.resource_browse(xref="z0bug.fiscalpos_it")
        fiscalpos.write({"to_send_mail": "enable"})
        partner = self.resource_browse(xref="base.res_partner_1")
        partner.write({"to_send_mail": "disable"})
        xref = "z0bug.invoice_Z0_1"
        invoice = self.resource_browse(xref=xref)
        invoice.unlink()
        invoice = self.resource_create("account.invoice", xref=xref)
        self.resource_edit(
            invoice,
            web_changes=[("fiscal_position_id", "z0bug.fiscalpos_it")]
        )
        self.assertFalse(invoice.to_send_mail)

    def test_invoice(self):
        self._test_01_invoice()
        self._test_02_invoice()
        self._test_03_invoice()
        self._test_04_invoice()
        self._test_05_invoice()
        self._test_06_invoice()
