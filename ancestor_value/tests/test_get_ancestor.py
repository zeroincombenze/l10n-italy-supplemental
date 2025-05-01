import logging
from .testenv import MainTest as SingleTransactionCase

_logger = logging.getLogger(__name__)


# Record data for base models


TEST_SETUP_LIST = []


class TestInvoiceRound(SingleTransactionCase):
    def setUp(self):
        super().setUp()
        # Add following statement just for get debug information
        self.debug_level = 0
        self.odoo_commit_test = True
        self.setup_env()

    def tearDown(self):
        super().tearDown()

    def test_ancestor_value(self):
        # Odoo demo data tree
        #     res_partner_1                              # parent
        #         \_ res_partner_address_1               # child address
        #
        _logger.info("🎺 Testing Ancestor Value")
        # Set parent record ref to "Valid"
        self.resource_write(
            xref="base.res_partner_1",
            resource="res.partner",
            values={"ref": "Valid", "comment": "top"},
        )
        # Set child record ref to null
        self.resource_write(
            xref="base.res_partner_address_1",
            resource="res.partner",
            values={"ref": False, "comment": "middle"},
        )
        # Create a child record of child
        self.resource_create(
            xref="z0bug.partner_11",
            resource="res.partner",
            values={
                "name": "Child",
                "parent_id": "base.res_partner_address_1",
                "comment": "bottom",
                "ref": False,
            }
        )
        record_top = self.resource_browse(
            xref="base.res_partner_1",
            resource="res.partner",
        )

        # Get ancestor value from middle record
        record_middle = self.resource_browse(
            xref="base.res_partner_address_1",
            resource="res.partner",
        )
        self.assertFalse(record_middle.ref)
        self.assertEqual(record_middle.ancestor_value("ref"), "Valid")
        self.assertEqual(record_middle.comment, "middle")
        self.assertEqual(record_middle.ancestor_value("ref", field="comment"), "top")

        # Get ancestor value from child record
        record_bottom = self.resource_browse(
            xref="z0bug.partner_11",
            resource="res.partner",
        )
        self.assertFalse(record_bottom.ref)
        self.assertEqual(record_bottom.ancestor_value("ref"), "Valid")
        self.assertEqual(record_bottom.comment, "bottom")
        self.assertEqual(record_bottom.ancestor_value("comment"), "bottom")
        self.assertEqual(
            record_bottom.ancestor_value("comment", skip_current=True), "middle")
        self.assertEqual(record_bottom.ancestor_value("ref", field="comment"), "top")
        self.assertEqual(record_bottom.ancestor_value("ref", value="Valid"), "Valid")
        self.assertEqual(
            record_bottom.ancestor_value(
                "ref", value="Valid", field="comment"), "top")
        self.assertEqual(
            record_bottom.ancestor_value("ref", field="self"), record_top)

        # Magic search: return True if record is in ancestor tree
        self.assertTrue(record_bottom.ancestor_value("self", value=record_top))
        self.assertTrue(record_bottom.ancestor_value("self", value=record_middle))

        # Search for out of tree elements
        record_none = self.resource_browse(
            xref="base.res_partner_2",
            resource="res.partner",
        )
        self.assertFalse(record_none.ancestor_value("comment"))
        self.assertFalse(record_none.ancestor_value("self", value=record_top))
