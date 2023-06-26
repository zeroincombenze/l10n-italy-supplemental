# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later
# (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    date_apply_balance = fields.Date(
        string='Data competenza bilancio',
        help="Date to apply for balance sheet",
        copy=False
    )

    @api.multi
    def post(self, invoice=False):
        for move in self:
            if not move.date_apply_balance:
                if invoice:
                    move.date_apply_balance = invoice.date_apply_balance
                else:
                    move.date_apply_balance = move.date
                # end if
            # end if
        # end for
        return super().post(invoice=invoice)
    # end post
