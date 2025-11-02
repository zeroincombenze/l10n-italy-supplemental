# -*- coding: utf-8 -*-
# import os
import re
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)

TEST_ACCOUNT_FISCAL_POSITION = {
    "z0bug.fiscalpos_it": {
        "name": "Italia",
    },
    "z0bug.fiscalpos_eu": {
        "name": "EU",
    },
    "z0bug.fiscalpos_xx": {
        "name": "xx",
    },
}

TEST_ACCOUNT_JOURNAL = {
    "external.INV": {
        "code": "INV",
        "type": "sale",
        "update_posted": True,
        "name": "Fatture di vendita",
    },
}

TEST_ACCOUNT_PAYMENT_TERM = {
    "z0bug.payment_term_1": {
        "name": "RiBA 30 GG",
    },
    "z0bug.payment_term_2": {
        "name": "Bonifico",
    },
}

TEST_ACCOUNT_PAYMENT_TERM_LINE = {
    "z0bug.payment_term_1_1": {
        "payment_id": "z0bug.payment_term_1",
        "sequence": 1,
        "days": 30,
        "value": "balance",
    },
    "z0bug.payment_term_2_1": {
        "payment_id": "z0bug.payment_term_2",
        "sequence": 1,
        "days": 0,
        "value": "balance",
    },
}

# Record data for models to test
TEST_ACCOUNT_INVOICE = {
    "z0bug.invoice_Z0_1": {
        "origin": "SO123",
        "reference": "SO123",
        "type": "out_invoice",
        "payment_term_id": "z0bug.payment_1",
        "journal_id": "external.INV",
        "date_invoice": "####-<#-99",
        "partner_bank_id": "z0bug.bank_company_1",
        "partner_id": "z0bug.res_partner_1",
        "fiscal_position_id": "z0bug.fiscalpos_it",
        "comment": "l10n_it_einvoice_out test\nItaly",
    },
    "z0bug.invoice_Z0_2": {
        "origin": "23011214",
        "reference": "23011214",
        "type": "out_invoice",
        "payment_term_id": "z0bug.payment_2",
        "journal_id": "external.INV",
        "date_invoice": "####-<#-99",
        "partner_id": "z0bug.res_partner_13",
        "fiscal_position_id": "z0bug.fiscalpos_eu",
        "comment": "l10n_it_einvoice_out test: EU partner invoice",
    },
    "z0bug.invoice_Z0_3": {
        "origin": "mail",
        "reference": "mail",
        "type": "out_invoice",
        "journal_id": "external.INV",
        "date_invoice": "####-<#-99",
        "partner_id": "z0bug.res_partner_17",
        "fiscal_position_id": "z0bug.fiscalpos_xx",
        "comment": "l10n_it_einvoice_out test\nextra EU partner",
    },
    "z0bug.invoice_Z0_4": {
        "origin": "CUP 123456",
        "reference": "CUP 123456",
        "type": "out_invoice",
        "payment_term_id": "z0bug.payment_2",
        "journal_id": "external.INV",
        "date_invoice": "####-<#-99",
        "partner_id": "z0bug.res_partner_15",
        "fiscal_position_id": "z0bug.fiscalpos_it",
        "comment": "l10n_it_einvoice_out test: PA invoice",
    },
    "z0bug.invoice_Z0_5": {
        "origin": "Supplier",
        "reference": "EXJ-240123",
        "type": "out_invoice",
        "payment_term_id": "z0bug.payment_1",
        "journal_id": "external.INV",
        "date_invoice": "####-<#-99",
        "partner_bank_id": "z0bug.bank_company_1",
        "partner_id": "z0bug.res_partner_3",
        "fiscal_position_id": "z0bug.fiscalpos_it",
        "comment": "l10n_it_einvoice_out test\nSelf Invoice",
        "fiscal_document_type_id": "l10n_it_ade.fatturapa_TD20",
        "sender": "CC",
    },
}

TEST_ACCOUNT_INVOICE_LINE = {
    "z0bug.invoice_Z0_1_1": {
        "product_id": "z0bug.product_product_1",
        "invoice_id": "z0bug.invoice_Z0_1",
        "price_unit": 0.84,
        "account_id": "l10n_generic_coa.conf_a_sale",
        "name": "Prodotto Alpha",
        "invoice_line_tax_ids": "z0bug.tax_22v",
        "quantity": 100,
    },
    "z0bug.invoice_Z0_1_2": {
        "product_id": "z0bug.product_product_2",
        "invoice_id": "z0bug.invoice_Z0_1",
        "price_unit": 1.69,
        "account_id": "l10n_generic_coa.conf_a_sale",
        "name": "Prodotto Beta",
        "invoice_line_tax_ids": "z0bug.tax_22v",
        "quantity": 10,
    },
    "z0bug.invoice_Z0_2_1": {
        "product_id": "z0bug.product_product_2",
        "invoice_id": "z0bug.invoice_Z0_2",
        "price_unit": 1.69,
        "account_id": "l10n_generic_coa.conf_a_sale",
        "name": "Prodotto Beta",
        "invoice_line_tax_ids": "z0bug.tax_a41v",
        "quantity": 50,
    },
    "z0bug.invoice_Z0_3_1": {
        "product_id": "z0bug.product_product_2",
        "invoice_id": "z0bug.invoice_Z0_3",
        "price_unit": 1.80,
        "account_id": "l10n_generic_coa.conf_a_sale",
        "name": "Prodotto Beta",
        "invoice_line_tax_ids": "z0bug.tax_a7tv",
        "quantity": 20,
    },
    "z0bug.invoice_Z0_4_1": {
        "product_id": "z0bug.product_product_2",
        "invoice_id": "z0bug.invoice_Z0_4",
        "price_unit": 1.80,
        "account_id": "l10n_generic_coa.conf_a_sale",
        "name": "Prodotto Beta",
        "invoice_line_tax_ids": "z0bug.tax_22v",
        "quantity": 40,
    },
    "z0bug.invoice_Z0_5_1": {
        "product_id": "z0bug.product_product_2",
        "invoice_id": "z0bug.invoice_Z0_6",
        "price_unit": 1.80,
        "account_id": "l10n_generic_coa.conf_a_sale",
        "name": "Prodotto Beta",
        "invoice_line_tax_ids": "z0bug.tax_22v",
        "quantity": 1,
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

TEST_RES_PARTNER_BANK = {
    "z0bug.bank_company_1": {
        "acc_number": "IT15A0123412345100000123456",
        "partner_id": "base.main_partner",
        # "acc_type": "iban",
    },
}

TEST_SETUP_LIST = [
    "account.account",
    "account.fiscal.position",
    "account.journal",
    "account.tax",
    "account.payment.term",
    "account.payment.term.line",
    "res.partner",
    "res.partner.bank",
    "product.template",
    "res.company",
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
            "DatiGenerali/DatiGeneraliDocumento/Numero": invoice.number,
            "ImportoTotaleDocumento": "%1.2f" % invoice.amount_total,
            "TipoDocumento": "TD20",
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
            "CessionarioCommittente/SoggettoEmittente": "CC",
        })
        self._test_file_xml(xml, test_vals)

    def _get_invoice_test_items(self, invoice):
        return {
            "DatiTrasmissione/IdTrasmittente/IdPaese":
                self.default_company().vat[: 2],
            "DatiTrasmissione/IdTrasmittente/IdCodice":
                self.default_company().vat[2:],

            "CedentePrestatore/DatiAnagrafici/IdFiscaleIVA/IdPaese":
                self.default_company().vat[: 2],
            "CedentePrestatore/DatiAnagrafici/IdFiscaleIVA/IdCodice":
                self.default_company().vat[2:],
            "CedentePrestatore/Sede/CAP": self.default_company().zip,
            "CedentePrestatore/Sede/Provincia": self.default_company().state_id.code,

            "DatiGenerali/DatiGeneraliDocumento/Data": invoice.date_invoice,
            "DatiGenerali/DatiGeneraliDocumento/Numero": invoice.number,
            "ImportoTotaleDocumento": "%1.2f" % invoice.amount_total,
            "TipoDocumento": "TD01",
        }

    def _validate_xml_pa(self, invoice, xml, vat=None, zip=None, state_code=None):
        test_vals = self._get_invoice_test_items(invoice)
        vat = vat or invoice.partner_id.vat
        zip = zip or invoice.partner_id.zip
        state_code = state_code or invoice.partner_id.state_id.code
        test_vals.update({
            "DatiTrasmissione/FormatoTrasmissione": "FPA12",
            "CodiceDestinatario": invoice.partner_id.ipa_code,
            "CessionarioCommittente/DatiAnagrafici/IdFiscaleIVA/IdPaese": vat[: 2],
            "CessionarioCommittente/DatiAnagrafici/IdFiscaleIVA/IdCodice": vat[2:],
            "CessionarioCommittente/Sede/CAP": zip,
            "CessionarioCommittente/Sede/Provincia": state_code,
        })
        self._test_file_xml(xml, test_vals)

    def _validate_xml_biz(self, invoice, xml, vat=None, zip=None, state_code=None):
        test_vals = self._get_invoice_test_items(invoice)
        vat = vat or invoice.partner_id.vat
        zip = zip or invoice.partner_id.zip
        state_code = state_code or invoice.partner_id.state_id.code
        test_vals.update({
            "DatiTrasmissione/FormatoTrasmissione": "FPR12",
            "CodiceDestinatario": invoice.partner_id.codice_destinatario,
            "CessionarioCommittente/DatiAnagrafici/IdFiscaleIVA/IdPaese": vat[: 2],
            "CessionarioCommittente/DatiAnagrafici/IdFiscaleIVA/IdCodice": vat[2:],
            "CessionarioCommittente/Sede/CAP": zip,
            "CessionarioCommittente/Sede/Provincia": state_code,
        })
        self._test_file_xml(xml, test_vals)

    def test_account_invoice(self):
        model = "account.invoice"
        for xref in TEST_ACCOUNT_INVOICE.keys():
            self.log_lvl_1(u"🎺 Testing %s[%s]" % (model, xref))
            invoice = self.resource_browse(xref=xref)
            self.resource_edit(resource=invoice, actions="action_invoice_open")
            self.assertEqual(
                invoice.state, "open", "action_invoice_open() FAILED: no state changed!"
            )
            self.wizard(module=".",
                        action_name="action_wizard_export_fatturapa",
                        records=invoice,
                        button_name="exportFatturaPA")
            xml = self.field_download(invoice.fatturapa_attachment_out_id, "datas")
            if xref == "z0bug.invoice_Z0_5":
                # Self invoice
                self._validate_xml_self(invoice, xml)
            elif xref == "z0bug.invoice_Z0_4":
                # PA invoice
                self._validate_xml_pa(invoice, xml)
            elif xref == "z0bug.invoice_Z0_3":
                # Business invoice xUE
                self._validate_xml_biz(invoice,
                                       xml,
                                       vat="CH99999999999",
                                       zip="00000",
                                       state_code="EE")
            elif xref == "z0bug.invoice_Z0_2":
                # Business invoice UE
                self._validate_xml_biz(invoice,
                                       xml,
                                       zip="00000",
                                       state_code="EE")
            else:
                # Business invoice
                self._validate_xml_biz(invoice, xml)
        attachments = self.env["fatturapa.attachment.out"]
        for xref in TEST_ACCOUNT_INVOICE.keys():
            attachments |= self.resource_browse(xref=xref).fatturapa_attachment_out_id
        self.assertEqual(len(attachments), 5)
        self.wizard(
            action_name="action_refresh_attachment_out",
            records=attachments,
            button_name="refresh_info"
        )
