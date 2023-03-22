# Copyright 2019-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License LGPL-3 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
#
from odoo import api, fields, models
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class AccountGroup(models.Model):
    _inherit = 'account.group'

    nature = fields.Selection(
        [('A', 'Attivo'),
         ('P', 'Passivo'),
         ('R', 'Ricavi'),
         ('C', 'Costi'),
         ('O', 'C/Ordine')],
        'Natura',
    )
    opposite_sign_description = fields.Char(
        string='Descrizione se segno invertito',
        size=255)
    opposite_sign_code = fields.Many2one(
        comodel_name='account.group',
        string='Gruppo se segno invertito',
        default='',
        help="Inserimento del codice conto per il segno opposto. "
             "La natura deve essere opposta.")
    account_ids = fields.One2many(
        'account.account', 'group_id',
        string='Accounts',
        help="Assigned accounts")
