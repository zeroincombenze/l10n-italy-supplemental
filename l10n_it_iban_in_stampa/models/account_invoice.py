# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import api, models

from .mixins import AccountMixin

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model, AccountMixin):
    _inherit = 'account.invoice'

    @api.model
    def create(self, vals):
        new_invoice: AccountInvoice = super().create(vals)

        # If both company bank and counterparty bank are missing
        # set them using the algorithm
        if not new_invoice.bank_2_print_selector:
            new_invoice._update_iban()
        # end if

        return new_invoice
    # end create

    # Extend method that loads invoice data from PO
    @api.onchange('purchase_id')
    def purchase_order_change(self):
        """Copy values from a Purchase Order to the new invoice form"""

        # Save the Purchase Order reference since the superclass
        # method will delete it once completed
        po = self.purchase_id

        # Call superclass function
        res = super().purchase_order_change()

        # Copy bank accounts related infos from Purchase Order object
        if po:
            self.bank_2_print_selector = po.bank_2_print_selector
            self.company_bank_id = po.company_bank_id and po.company_bank_id
            self.counterparty_bank_id = po.counterparty_bank_id and po.counterparty_bank_id
        # end if

        # Return the result
        return res

    # end purchase_order_change

# end AccountInvoice
