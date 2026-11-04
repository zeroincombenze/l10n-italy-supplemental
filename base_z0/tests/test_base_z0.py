# -*- coding: utf-8 -*-
#
# Copyright 2018-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import mock

from odoo.tests.common import TransactionCase

from ..models.res_company import Z0_FOOTER


class TestBaseZ0(TransactionCase):
    def test_new_company_footer(self):
        company = self.env["res.company"].create({"name": "Z0 test company"})
        self.assertIn(Z0_FOOTER, company.rml_header)

    def test_broken_description(self):
        module = self.env["ir.module.module"].search(
            [("name", "=", "base_z0")]
        )
        module.invalidate_cache()
        # Hide index.html, so the RST description is rendered
        with mock.patch(
            "odoo.modules.get_module_resource", return_value=False
        ), mock.patch(
            "odoo.addons.base.module.module.publish_string",
            side_effect=ValueError("broken RST"),
        ):
            html = module.description_html
        self.assertIn("Error in Description", html)
