#
# Copyright 2020-24 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    # Ported from account.invoice's `_onchange_partner_id` override
    # (account.invoice was merged into account.move at 13.0). At 18.0
    # `partner_bank_id` is a stored compute field
    # (`_compute_partner_bank_id`, depending on `bank_partner_id`), not
    # something set from an onchange on `partner_id` anymore, so this is
    # now an extension of that compute instead: it still only takes over
    # for out_invoice/in_refund moves (the original's exact scope --
    # `is_inbound(include_receipts=False)` matches it, unlike the default
    # `is_inbound()` which would also cover out_receipt) when the
    # commercial partner has an `assigned_income_bank` configured,
    # otherwise the core behavior (first trusted bank account of
    # `bank_partner_id`) is left as-is.
    @api.depends("commercial_partner_id.assigned_income_bank")
    def _compute_partner_bank_id(self):
        super()._compute_partner_bank_id()
        for move in self:
            if (
                move.is_inbound(include_receipts=False)
                and move.commercial_partner_id
                and move.commercial_partner_id.customer_rank > 0
                and move.commercial_partner_id.assigned_income_bank
            ):
                move.partner_bank_id = move.commercial_partner_id.assigned_income_bank
