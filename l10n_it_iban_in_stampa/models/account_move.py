# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import api, models, fields

from .mixins import AccountMixin

_logger = logging.getLogger(__name__)


class AccountMove(models.Model, AccountMixin):
    _inherit = 'account.move'

    @api.multi
    def post(self, invoice=False):

        for move in self:
            if invoice:
                move.counterparty_bank_id = invoice.counterparty_bank_id
                move.company_bank_id = invoice.company_bank_id
                move.bank_2_print_selector = invoice.bank_2_print_selector
            # end if

        # end for

        return super().post(invoice=invoice)
    # end post

# end AccountMove

