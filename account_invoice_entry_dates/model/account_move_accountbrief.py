# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import models, fields
# from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp


class AccountBrief(models.Model):
    _name = 'account.move.accountbrief'
    _description = 'Prima nota - Somma movimenti contabili fattura raggruppati per contro e date di competenza'

    # TODO: definire ordinamento
    # _order = 'due_date'

    move_id = fields.Many2one(
        comodel_name='account.move',
        domain=[('journal_id.type', 'in', ['sale', 'sale_refund', 'purchase', 'purchase_refund'])],
        string='Registrazione contabile',
        requred=True
    )

    account_id = fields.Many2one(
        comodel_name='account.account',
        string='Conto',
        requred=True
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        requred=True
    )

    accrual_date_start = fields.Date(string='Inizio competenza', index=True)

    accrual_date_end = fields.Date(string='Fine competenza', index=True)

    # Dare
    debit = fields.Float(
        string='Dare', digits=dp.get_precision('Account')
    )

    # Avere
    credit = fields.Float(
        string='Avere', digits=dp.get_precision('Account')
    )

# end AccountBrief
