# -*- coding: utf-8 -*-
#
# Copyright 2018-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    def _default_rc_type(self):
        kind_N3 = self.kind_id and self.kind_id.code.startswith("N3")
        kind_N6 = self.kind_id and self.kind_id.code.startswith("N6")
        if self.rc_purchase_tax_id:
            kind = ""
        elif (
                self.type_tax_use == "purchase"
                and kind_N3 and self.kind_id.code != "N3.5"
        ):
            kind = "self"
        elif kind_N6:
            kind = "self"
        else:
            kind = ""
        return kind

    kind_id = fields.Many2one(
        "italy.ade.tax.nature",
        string="Nature",
        oldname="nature_id",
        help="Nature of tax code: may be taxable, out of scope, etc ...",
    )
    payability = fields.Selection(
        [
            ("I", "Immediate payability"),
            ("D", "Deferred payability"),
            ("S", "Split payment"),
        ],
        string="VAT payability",
        default="I",
    )
    law_reference = fields.Char("Law reference", size=128)
    assosoftware_id = fields.Many2one(
        "italy.ade.tax.assosoftware",
        string="Assosoftware Code",
        help="Tax Assosoftware classification",
    )
    rc_type = fields.Selection(
        selection=[
            ("", "No RC"),
            # ("local", "RC domestic"),
            ("self", "RC with self.invoice"),
        ],
        string="Reverse Charge Policy",
        default=_default_rc_type,
    )
    rc_sale_tax_id = fields.Many2one(
        comodel_name="account.tax",
        string="Mapped Sale Tax Code",
        domain=[("type_tax_use", "=", "sale")],
    )
    rc_purchase_tax_id = fields.Many2one(
        comodel_name="account.tax",
        string="Mapped Purchase Tax Code",
        domain=[("type_tax_use", "=", "purchase")],
        readonly=True,
    )
