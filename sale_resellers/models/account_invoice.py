# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    end_user_id = fields.Many2one(
        'res.partner', string='End user',
        index=True)
    ref_user_id = fields.Many2one(
        'res.partner', string='Reference user')
