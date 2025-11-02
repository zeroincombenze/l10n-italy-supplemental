# -*- coding: utf-8 -*-
import logging
import re
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)


# Record data for base models


TEST_SETUP_LIST = [
    "account.account",
    "account.tax",
    "account.journal",
    "account.rc.type",
    "account.rc.type.tax",
    "account.fiscal.position",
    "account.payment.term",
    "account.payment.term.line",
    "product.template",
    "res.partner",
    "res.company",
    "account.invoice",
    "account.invoice.line",
]


class TestReverseCharge(SingleTransactionCase):
    def setUp(self):
        super(TestReverseCharge, self).setUp()
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
            },
        )
        self.setup_env()  # Create test environment

    def tearDown(self):
        super(TestReverseCharge, self).tearDown()

    def _test_file_xml(self, xml, values):
        xml = xml.replace("\n", "")
        for key, val in values.items():
            keys = key.split("/")
            begkey = ""
            for kk in keys[: -1]:
                begkey += "<%s>.*" % kk
            begkey += "<%s>" % keys[-1]
            endkey = "</%s>" % keys[-1]
            pattern = "".join([begkey, val, endkey])
            self.assertTrue(re.search(pattern, xml),
                            "Pattern %s not found in XML" % pattern)

    def _get_self_invoice_test_items(self, invoice):
        return {
            "DatiTrasmissione/IdTrasmittente/IdPaese":
                self.default_company().vat[: 2],
            "DatiTrasmissione/IdTrasmittente/IdCodice":
                self.default_company().vat[2:],

            # "CodiceDestinatario": self.default_company().partner_id.codice_destinatario,

            # "CessionarioCommittente/DatiAnagrafici/IdFiscaleIVA/IdPaese":
            #     self.default_company().vat[: 2],
            # "CessionarioCommittente/DatiAnagrafici/IdFiscaleIVA/IdCodice":
            #     self.default_company().vat[2:],
            # "CessionarioCommittente/Sede/CAP": self.default_company().zip,
            # "CessionarioCommittente/Sede/Provincia":
            #     self.default_company().state_id.code,

            "DatiGenerali/DatiGeneraliDocumento/Data": invoice.date_invoice,
            "ImportoTotaleDocumento": "%1.2f" % invoice.amount_total,
            # "TipoDocumento": "TD18",
        }

    def _validate_xml_self(self, invoice, xml, vat=None, zip=None, state_code=None):
        test_vals = self._get_self_invoice_test_items(invoice)
        vat = vat or invoice.partner_id.vat
        zip = zip or invoice.partner_id.zip
        state_code = state_code or invoice.partner_id.state_id.code
        test_vals.update({
            "DatiTrasmissione/FormatoTrasmissione": "FPR12",
            "CedentePrestatore/DatiAnagrafici/IdFiscaleIVA/IdPaese": vat[: 2],
            "CedentePrestatore/DatiAnagrafici/IdFiscaleIVA/IdCodice": vat[2:],
            "CedentePrestatore/Sede/CAP": zip,
            "CedentePrestatore/Sede/Provincia": state_code,
        })
        self._test_file_xml(xml, test_vals)

    def _test_rc_1_purchase(self):
        xref = "z0bug.invoice_ZI_9"
        invoice = self.resource_browse(xref=xref)
        self.resource_edit(resource=invoice, actions="action_invoice_open")
        invoice = self.resource_browse(xref=xref)
        self.assertEqual(
            invoice.state,
            "open",
            msg="action_invoice_open() FAILED: no state changed!"
        )
        self.assertEqual(round(invoice.amount_tax, 2), 75.57)
        self.assertEqual(invoice.amount_total, 419.07)
        self.assertEqual(invoice.amount_net_pay, 343.50)
        self.assertEqual(invoice.residual, 343.50)
        self.assertEqual(round(invoice.amount_rc, 2), -75.57)
        self_invoice = invoice.rc_self_invoice_id
        self.assertTrue(self_invoice)
        self.assertEqual(
            self_invoice.state,
            "paid",
            msg="Invalid self-invoice status"
        )
        self.assertEqual(round(self_invoice.amount_tax, 2), 75.57)
        self.assertEqual(self_invoice.amount_total, 419.07)

        self.wizard(module="l10n_it_einvoice_out",
                    action_name="action_wizard_export_fatturapa",
                    records=self_invoice,
                    button_name="exportFatturaPA")
        xml = self.field_download(self_invoice.fatturapa_attachment_out_id,
                                  "datas")
        self._validate_xml_self(invoice, xml, zip="00000", state_code="EE")

    def _test_rc_1_sale(self):
        xref = "z0bug.invoice_Z0_9"
        invoice = self.resource_browse(xref=xref)
        # Avoid error
        invoice.payment_term_id = False
        self.resource_edit(
            resource=invoice,
            actions="action_invoice_open")
        invoice = self.resource_browse(xref=xref)
        self.assertEqual(
            invoice.state,
            "open",
            msg="action_invoice_open() FAILED: no state changed!"
        )
        self.assertEqual(round(invoice.amount_tax, 2), 32.91)
        self.assertEqual(invoice.amount_total, 182.50)
        self.assertEqual(invoice.amount_net_pay, 160.50)
        self.assertEqual(invoice.residual, 160.50)
        self.assertEqual(invoice.amount_rc, -22.0)

        template = []
        tmpl_move = []
        vals = {
            "account_id": invoice.account_id.id,
            "debit": 182.50,
            "credit": 0.0,
            "tax_line_id": False,
            "tax_ids": [],
        }
        tmpl_move.append(vals)
        vals = {
            "account_id": invoice.account_id.id,
            "debit": 0.0,
            "credit": 22.0,
            "tax_line_id": self.env.ref("z0bug.tax_a17c6cv"),
            "tax_ids": [],
        }
        tmpl_move.append(vals)
        template.append({"line_ids": tmpl_move})
        self.validate_records(template, invoice.move_id)

        self.wizard(module="l10n_it_einvoice_out",
                    action_name="action_wizard_export_fatturapa",
                    records=invoice,
                    button_name="exportFatturaPA")
        xml = self.field_download(invoice.fatturapa_attachment_out_id,
                                  "datas")
        self._validate_xml_self(invoice, xml, zip="15010", state_code="AL")

    def test_rc(self):
        _logger.info("🎺 Testing Reverse Charge")
        self._test_rc_1_purchase()
        self._test_rc_1_sale()

