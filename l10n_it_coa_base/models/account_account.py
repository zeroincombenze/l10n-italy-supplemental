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

ACC_NATURE = [
    ('A', 'Attivo'),
    ('P', 'Passivo'),
    ('R', 'Ricavi'),
    ('C', 'Costi'),
    ('O', 'C/Ordine')
]


class AccountAccount(models.Model):
    _inherit = 'account.account'

    # TODO> move to group_id, remove early
    parent_id = fields.Many2one(
        string='Parent',
        comodel_name='account.account',
        index=True,
        ondelete='cascade'
    )
    # TODO> unuseful, remove early
    child_ids = fields.One2many(
        string='Child Accounts',
        comodel_name='account.account',
        inverse_name='parent_id',
        copy=False,
    )
    # TODO> unuseful, remove early
    is_parent = fields.Boolean(
        string='Mastro/Capoconto',
        # store=True,
        copy=False,
    )
    nature = fields.Selection(
        ACC_NATURE,
        'Natura',
    )
    alt_nature = fields.Selection(
        related='user_type_id.alt_nature',
        type='selection',
        string='Natura alternativa'
    )
    negative_balance = fields.Selection(
        [('invert', 'Inverti'),
         ('invert_on_demand', 'Inverti se richiesto'),
         ('no_invert', 'Non invertire'),
         ],
        'Saldo negativo',
        default='no_invert',
    )
    negative_group_id = fields.Many2one(
        'account.group',
        string='Gruppo se saldo negativo',
        help='Usare questo gruppo se saldo negativo')
    # TODO> moved to account group, to remove early
    opposite_sign_description = fields.Char(
        string='Descrizione a segno invertito',
        size=255)
    # TODO> moved to account group, to remove early
    opposite_sign_code = fields.Many2one(
        comodel_name='account.account',
        string='Codice conto a segno invertito',
        domain="[('is_parent', '=', False)]",
        default='',
        help="Inserimento del codice conto per il segno opposto. "
             "La natura deve essere opposta.")

    @api.onchange('user_type_id')
    def onchange_user_type(self):
        if not self.user_type_id:
            return
        if self.user_type_id.type in ('payable', 'receivable'):
            self.reconcile = True
        elif (self.user_type_id.type == 'liquidity' or
              self.user_type_id.type in ('R', 'C', 'O')):
            self.reconcile = False
        if (self.user_type_id.alt_nature and
                self.user_type_id.nature != self.user_type_id.alt_nature):
            self.negative_balance = 'invert'

    @api.onchange('reconcile')
    def onchange_reconcile(self):
        if (self.reconcile and (
                self.user_type_id.type == 'liquidity' or
                self.user_type_id.type in ('R', 'C', 'O'))):
            self.reconcile = False

    # @api.onchange('opposite_sign_code')
    # def onchange_opposite_sign_code(self):
    #     opposite_natures = {
    #         'A': 'P',
    #         'P': 'A',
    #         'C': 'R',
    #         'R': 'C'
    #     }
    #     domain = [('is_parent', '=', False)]
    #     if self.nature and self.nature != 'O':
    #         domain.append(('nature', '=', opposite_natures[self.nature]))
    #     return {'domain': {'opposite_sign_code': domain}}


class AccountAccountType(models.Model):
    _inherit = 'account.account.type'

    nature = fields.Selection(
        ACC_NATURE,
        'Natura'
    )
    alt_nature = fields.Selection(
        ACC_NATURE,
        'Natura alternativa'
    )
    account_ids = fields.One2many(
        'account.account', 'user_type_id',
        string='Accounts',
        help="Assigned accounts")
