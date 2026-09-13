#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import fields, models

# NOTE: the `print_quotation()` override that used to live here (to let
# `report.select_reportname()` swap in an alternate report at print-time)
# has no direct 18.0 equivalent: sale.order no longer has a per-record
# "print" Python method to intercept the way it did pre-11.0 -- printing
# goes straight through `ir.actions.report` xmlid actions bound via
# `binding_model_id`. See models/report.py for the rest of this gap; not
# resolved here, flagged instead of guessed.


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line", "multireport.mixin"]
    _name = "sale.order.line"

    delivery_date = fields.Date(
        "Delivery Date",
        compute="_compute_delivery_date",
    )

    def _compute_delivery_date(self):
        if "requested_date" in self._fields:
            for ln in self:
                ln.delivery_date = getattr(ln, "requested_date")
        else:
            for ln in self:
                ln.delivery_date = False
