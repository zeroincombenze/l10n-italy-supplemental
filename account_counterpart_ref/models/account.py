# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    counterpart_ref = fields.Char(
        "Counterpart Reference",
        size=12,
        help=("Add or select counterpart journal item.\n"
              "Numeric reference are aligned to right"))

    @api.onchange("counterpart_ref")
    def onchange_counterpart_ref(self):
        if self.name and self.name.isdigit():
            self.counterpart_ref = "%12.12s" % self.counterpart_ref
