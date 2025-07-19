# -*- coding: utf-8 -*-
import os
import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)

TEST_ITALY_ADE_SENDER = {
    "l10n_it_einvoice_base.einvoice_json": {
        "max_invoices_ctr": 1000,
    },
}
TEST_SETUP_LIST = ["italy.ade.sender", ]


class TestSdi(SingleTransactionCase):

    def setUp(self):
        super(TestSdi, self).setUp()
        # Add following statement just for get debug information
        self.debug_level = 0
        data = {"TEST_SETUP_LIST": TEST_SETUP_LIST}
        for resource in TEST_SETUP_LIST:
            item = "TEST_%s" % resource.upper().replace(".", "_")
            data[item] = globals()[item]
        self.declare_all_data(data)  # TestEnv swallows the data
        self.setup_env()  # Create test environment

    def tearDown(self):
        super(TestSdi, self).tearDown()
        if os.environ.get("ODOO_COMMIT_TEST", ""):  # pragma: no cover
            # Save test environment, so it is available to dump
            self.env.cr.commit()  # pylint: disable=invalid-commit
            _logger.info("✨ Test data committed")

    def test_mytest(self):
        _logger.info(
            "🎺 Testing test_mytest"  # Use unicode char to best log reading
        )
        channel = self.resource_browse("l10n_it_einvoice_base.einvoice_json")
        channel._compute_available()
        self.assertEqual(990, channel.avail_invoices_ctr)
