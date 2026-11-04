# -*- coding: utf-8 -*-
#
# Copyright 2026 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def _check_invoice_reference(self):
        # Replaces the upstream check, so super() is not called.
        # Italian suppliers restart their numbering every year: a reference
        # is a duplicate only within the same calendar year.
        for invoice in self:
            if invoice.type not in ("in_invoice", "in_refund") or not invoice.reference:
                continue
            year = (
                invoice.date_invoice or fields.Date.context_today(invoice)
            )[0:4]
            if self.search(
                [
                    ("type", "=", invoice.type),
                    ("reference", "=", invoice.reference),
                    ("company_id", "=", invoice.company_id.id),
                    (
                        "commercial_partner_id",
                        "=",
                        invoice.commercial_partner_id.id,
                    ),
                    ("date_invoice", ">=", "%s-01-01" % year),
                    ("date_invoice", "<=", "%s-12-31" % year),
                    ("id", "!=", invoice.id),
                ]
            ):
                raise UserError(
                    _(
                        "Duplicated vendor reference detected. You probably"
                        " encoded twice the same vendor bill/refund."
                    )
                )
