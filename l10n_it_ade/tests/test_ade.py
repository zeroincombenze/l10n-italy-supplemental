# -*- coding: utf-8 -*-
#
# Copyright 2018-23 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#

import os
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)

TEST_ITALY_ADE_CODICE_CARICA = {
    "z0bug.ade_CC99": {
        "code": "99",
        "name": "Please, do not use this record!",
    },
}

TEST_ITALY_ADE_TAX_NATURE = {
    "z0bug.ade_TN99": {
        "code": "N9.9",
        "name": "Please, do not use this record!",
    },
}

TEST_ITALY_ADE_INVOICE_TYPE = {
    "z0bug.ade_TD99": {
        "code": "TD99",
        "name": "Please, do not use this record!",
    },
}

CODICE_NAME2 = u"Please, delete this record!"

TEST_SETUP_LIST = [
    "italy.ade.codice.carica",
    "italy.ade.tax.nature",
    "italy.ade.invoice.type",
]


class TestAde(SingleTransactionCase):

    def setUp(self):
        super(TestAde, self).setUp()
        # Add following statement just for get debug information
        self.debug_level = 0
        data = {"TEST_SETUP_LIST": TEST_SETUP_LIST}
        for resource in TEST_SETUP_LIST:
            item = "TEST_%s" % resource.upper().replace(".", "_")
            data[item] = globals()[item]
        self.declare_all_data(data)  # TestEnv swallows the data
        self.setup_env()  # Create test environment

    def tearDown(self):
        super(TestAde, self).tearDown()
        if os.environ.get("ODOO_COMMIT_TEST", ""):  # pragma: no cover
            # Save test environment, so it is available to dump
            self.env.cr.commit()  # pylint: disable=invalid-commit
            _logger.info("✨ Test data committed")

    def test_00_mix(self):
        _logger.info(
            u"🎺 Testing test_00_mix"
        )
        Invoice = self.env["account.invoice"]
        text = Invoice.wep_text("© 2018-2023 Zeroincombenze® - 1€ ße")
        self.assertEqual(
            text,
            "(C) 2018-2023 Zeroincombenze(R) - 1EUR sse",
        )

        rec = self.resource_browse(xref="z0bug.ade_CC99")
        text = rec.name_get()
        self.assertEqual(
            text,
            [(rec.id, "[99] Please, do not use this record!")]
        )

        rec = self.resource_browse(xref="z0bug.ade_TN99")
        text = rec.name_get()
        self.assertEqual(
            text,
            [(rec.id, "[N9.9] Please, do not use this record!")]
        )
        rec = self.env["italy.ade.tax.nature"].name_search(name="Please")
        self.assertEqual(
            text,
            rec,
        )

        rec = self.resource_browse(xref="z0bug.ade_TD99")
        text = rec.name_get()
        self.assertEqual(
            text,
            [(rec.id, "[TD99] Please, do not use this record!")]
        )

    def test_01_codice_carica(self):
        _logger.info(
            u"🎺 Testing test_01_codice_carica"
        )
        self.resource_write("italy.ade.codice.carica",
                            xref="z0bug.ade_CC99",
                            values={"name": CODICE_NAME2})
        rec = self.resource_browse(xref="z0bug.ade_CC99")
        self.assertEqual(rec.name, CODICE_NAME2)

    def test_02_natura(self):
        _logger.info(
            u"🎺 Testing test_02_natura"
        )
        self.resource_write("italy.ade.tax.nature",
                            xref="z0bug.ade_TN99",
                            values={"name": CODICE_NAME2})
        rec = self.resource_browse(xref="z0bug.ade_TN99")
        self.assertEqual(rec.name, CODICE_NAME2)

    def test_03_invoice_type(self):
        _logger.info(
            u"🎺 Testing test_03_invoice_type"
        )
        self.resource_write("italy.ade.invoice.type",
                            xref="z0bug.ade_TD99",
                            values={"name": CODICE_NAME2})
        rec = self.resource_browse(xref="z0bug.ade_TD99")
        self.assertEqual(rec.name, CODICE_NAME2)
