# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo.tests.common import TransactionCase

TEST_NAME = "MOVE/2021/0001"


class GetActualVal(TransactionCase):
    def setUp(self):
        super(GetActualVal, self).setUp()
        self.journal = self.env["account.journal"].search([("type", "=", "general")])[0]
        journal_id = self.journal.id
        self.move_vals = {
            "name": TEST_NAME,
            "journal_id": journal_id,
        }
        self.move = self.env["account.move"].create(self.move_vals)

    def test_get_actual_value_name(self):
        name = "name"
        res = self.move.get_actual_val({}, name, layer="onchange")
        self.assertEqual(res, TEST_NAME)
        res = self.move.get_actual_val(self.move_vals, name, layer="write")
        self.assertEqual(res, TEST_NAME)
        res = self.env["account.move"].get_actual_val(
            self.move_vals, name, layer="create"
        )
        self.assertEqual(res, TEST_NAME)

    def test_get_actual_value_journal(self):
        name = "journal_id"
        res = self.move.get_actual_val({}, name, layer="onchange", ttype="many2one")
        self.assertEqual(res, self.journal)
        res = self.move.get_actual_val(
            self.move_vals, name, layer="write", ttype="many2one"
        )
        self.assertEqual(res, self.journal)
        res = self.env["account.move"].get_actual_val(
            self.move_vals, name, layer="create", ttype="many2one"
        )
        self.assertEqual(res, self.journal)

        res = self.move.get_actual_val({}, name, layer="onchange", ttype="id")
        self.assertEqual(res, self.journal.id)
        res = self.move.get_actual_val(self.move_vals, name, layer="write", ttype="id")
        self.assertEqual(res, self.journal.id)
        res = self.env["account.move"].get_actual_val(
            self.move_vals, name, layer="create", ttype="id"
        )
        self.assertEqual(res, self.journal.id)

    def test_get_actual_value_company(self):
        name = "company_id"
        res = self.move.get_actual_val({}, name, layer="onchange", ttype="company")
        self.assertEqual(res, self.env.user.company_id)
        res = self.move.get_actual_val(
            self.move_vals, name, layer="write", ttype="company"
        )
        self.assertEqual(res, self.env.user.company_id)
        res = self.env["account.move"].get_actual_val(
            self.move_vals, name, layer="create", ttype="company"
        )
        self.assertEqual(res, self.env.user.company_id)

        res = self.move.get_actual_val({}, name, layer="onchange", ttype="company_id")
        self.assertEqual(res, self.env.user.company_id.id)
        res = self.move.get_actual_val(
            self.move_vals, name, layer="write", ttype="company_id"
        )
        self.assertEqual(res, self.env.user.company_id.id)
        res = self.env["account.move"].get_actual_val(
            self.move_vals, name, layer="create", ttype="company_id"
        )
        self.assertEqual(res, self.env.user.company_id.id)
