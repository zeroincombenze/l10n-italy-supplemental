# Copyright 2021-2022 LibrERP enterprise network <https://www.librerp.it>
#
# License OPL-1 or later
#   https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps)
#
from odoo import fields, models


class Account(models.Model):
    """
    This class extends account.account by adding a field to easily access
    to related account.move.line
    """
    _inherit = "account.account"

    # The account.move.line records already have a pointer to account,
    # the purpose of this field is just to make it easier to retrieve
    # those lines
    move_line_ids = fields.One2many(
        comodel_name="account.move.line",
        inverse_name="account_id",
        string="Righe del conto",
    )


# end Account
