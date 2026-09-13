#
# Copyright 2018-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import api, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    # `active` and `acc_type` used to be re-declared here to restore
    # features Odoo core had dropped after 10.0; both are now native,
    # computed core fields again (`acc_type` via `_compute_acc_type`,
    # `active` with its own "Archived" ribbon on the form), so they are
    # no longer redeclared here to avoid clashing with the core computed
    # field definitions.

    @api.depends("bank_id.name", "acc_number")
    def _compute_display_name(self):
        for bank in self:
            if bank.bank_id.name:
                bank.display_name = "%s *%s " % (
                    bank.bank_id.name,
                    bank.acc_number[-4:],
                )
            else:
                bank.display_name = bank.acc_number
