# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import api, models


_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Journal Entries'

    @api.constrains('line_ids', 'journal_id', 'auto_reverse', 'reverse_date')
    def _validate_move_modification(self):

        # ---- ATTENZIONE ---- ---- ATTENZIONE ---- ---- ATTENZIONE ---- ---- ATTENZIONE ----
        # Il presente metodo sovrascrive il metodo originale eliminando il
        # controllo eseguito perchè bloccava di fatto alcune operazioni LECITE.
        # Il presente codice andrà eliminato qualora il modulo "account" di
        # Odoo core venisse correttp adeguatamente.
        # ---- ATTENZIONE ---- ---- ATTENZIONE ---- ---- ATTENZIONE ---- ---- ATTENZIONE ----

        # if 'posted' in self.mapped('line_ids.payment_id.state'):
        #     raise ValidationError(_("You cannot modify a journal entry linked to a posted payment."))

        pass

    # end _validate_move_modification

# end AccountMove
