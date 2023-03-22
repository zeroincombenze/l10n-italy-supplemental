# Copyright 2017-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = ['account.journal']

    enable_date = fields.Boolean(
        default=False,
        help='If set, end-user can update account date')

    @api.onchange('type')
    def _onchange_type(self):
        self.check_4_sequence = False
