# -*- coding: utf-8 -*-
#
# Copyright 2017-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = ["account.journal"]

    enable_date = fields.Boolean(
        default=False, help="If set, end-user can update account date"
    )

    # @api.onchange('type')
    # def _onchange_type(self):
    #     self.check_4_sequence = False
