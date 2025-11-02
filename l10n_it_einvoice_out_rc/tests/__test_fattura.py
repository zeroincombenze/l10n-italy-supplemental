# -*- coding: utf-8 -*-
# import os
import re
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)

TEST_ACCOUNT_JOURNAL = {
    "external.CG": {
        "code": "CG",
        "type": "general",
        "update_posted": True,
        "name": "Giroconti tecnici",
        "default_debit_account_id": "z0bug.coa_gc_rc",
        "default_credit_account_id": "z0bug.coa_gc_rc",
        "sequence": 100,
    },
}

TEST_ACCOUNT_RC_TYPE = {
    "l10n_it_reverse_charge.account_rc_type_1": {
        "name": "Intra-EU",
        "method": "selfinvoice",
        "partner_type": "supplier",
        "journal_id": "external.INV",
        "payment_journal_id": "external.CG",
        "transitory_account_id": "z0bug.coa_gc_rc",
        "fiscal_document_type_id": "l10n_it_ade.fatturapa_TD18"
    },
}

TEST_ACCOUNT_RC_TYPE_TAX = {
    "l10n_it_reverse_charge.account_rc_type_1_tax_a41a": {
        "rc_type_id": "l10n_it_reverse_charge.account_rc_type_1",
        "purchase_tax_id": "z0bug.tax_a41a",
        "sale_tax_id": "z0bug.tax_aa41v",
    },
}

TEST_ACCOUNT_INVOICE = {
    "z0bug.invoice_Z0_1": {
        "type": "in_invoice",
        "journal_id": "external.BILL",
        "date_invoice": "####-##-<#",
        "date": "####-##-##",
        "partner_id": "z0bug.res_partner_12",
        "fiscal_position_id": "z0bug.fiscalpos_eu",
    },
}

TEST_ACCOUNT_INVOICE_LINE = {
    "z0bug.invoice_Z0_1_1": {
        "product_id": "z0bug.product_product_1",
        "invoice_id": "z0bug.invoice_Z0_1",
        "price_unit": 0.42,
        "account_id": "l10n_generic_coa.conf_cog",
        "name": "Prodotto Alpha",
        "invoice_line_tax_ids": "z0bug.tax_a41a",
        "quantity": 100,
        "rc": True,
    },
}

TEST_RES_COMPANY = {
    "z0bug.mycompany": {
        "fatturapa_fiscal_position_id": "l10n_it_einvoice_base.fatturapa_RF01",
        "fatturapa_sequence_id": "l10n_it_einvoice_base.seq_fatturapa",
        "fatturapa_rea_office": "base.state_it_mi",
        "fatturapa_rea_number": "123456",
        "fatturapa_rea_capital": 10000,
        "fatturapa_rea_partner": "SU",
    }
}


TEST_SETUP_LIST = [
    "account.account",
    "account.journal",
    "account.tax",
    "account.rc.type",
    "account.rc.type.tax",
    "account.fiscal.position",
    "res.partner",
    "res.company",
    "account.invoice",
    "account.invoice.line",
]


class AccountInvoice(SingleTransactionCase):

    def setUp(self):
        super(AccountInvoice, self).setUp()
        self.debug_level = 0
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
        super(AccountInvoice, self).tearDown()

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

            "CodiceDestinatario": self.default_company().partner_id.codice_destinatario,

            "CessionarioCommittente/DatiAnagrafici/IdFiscaleIVA/IdPaese":
                self.default_company().vat[: 2],
            "CessionarioCommittente/DatiAnagrafici/IdFiscaleIVA/IdCodice":
                self.default_company().vat[2:],
            "CessionarioCommittente/Sede/CAP": self.default_company().zip,
            "CessionarioCommittente/Sede/Provincia":
                self.default_company().state_id.code,

            "DatiGenerali/DatiGeneraliDocumento/Data": invoice.date_invoice,
            "ImportoTotaleDocumento": "%1.2f" % invoice.amount_total,
            "TipoDocumento": "TD18",
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

    def test_account_invoice(self):
        model = "account.invoice"
        for xref in TEST_ACCOUNT_INVOICE.keys():
            self.log_lvl_1(u"🎺 Testing %s[%s]" % (model, xref))
            invoice = self.resource_browse(xref=xref)
            self.resource_edit(resource=invoice, actions="action_invoice_open")
            invoice = self.resource_browse(xref=xref)
            self.assertEqual(
                invoice.state,
                "open",
                msg="action_invoice_open() FAILED: no state changed!"
            )
            self.assertEqual(
                invoice.amount_total,
                51.24,
            )
            self.assertEqual(
                invoice.residual,
                42.0,
            )
            self_invoice = invoice.rc_self_invoice_id
            self.assertTrue(self_invoice)
            self.assertEqual(
                self_invoice.state,
                "paid",
                msg="Invalid self-invoice status"
            )
            self.wizard(module="l10n_it_einvoice_out",
                        action_name="action_wizard_export_fatturapa",
                        records=self_invoice,
                        button_name="exportFatturaPA")
            xml = self.field_download(self_invoice.fatturapa_attachment_out_id,
                                      "datas")
            self._validate_xml_self(invoice, xml, zip="00000", state_code="EE")
