# -*- coding: utf-8 -*-
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# Copyright 2019 Aleph Objects, Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    force_invoiced = fields.Boolean(
        string="Force invoiced",
        help="When you set this field, the purchase order will be "
        "considered as fully billed, even when there may be ordered "
        "or delivered quantities pending to bill.",
        readonly=True,
        states={"done": [("readonly", False)]},
        copy=False,
    )

    @api.depends("force_invoiced")
    def _get_invoiced(self):
        super(PurchaseOrder, self)._get_invoiced()
        for order in self.filtered(
            lambda po: po.force_invoiced and po.invoice_status == "to invoice"
        ):
            order.invoice_status = "invoiced"
