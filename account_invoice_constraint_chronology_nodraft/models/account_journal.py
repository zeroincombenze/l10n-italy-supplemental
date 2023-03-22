# Copyright 2015-19 ACSONE SA/NV <http://acsone.eu>
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = ['account.journal']

    check_chronology = fields.Boolean(
        default=False,
    )

    @api.onchange('type')
    def _onchange_type(self):
        self.ensure_one()
        if self.type not in ['sale', 'purchase']:
            self.check_chronology = False
