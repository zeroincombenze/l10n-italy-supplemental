# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
from odoo import fields, models


class ItalyAccountBalance(models.Model):
    _inherit = 'italy.account.balance'

    balance_line_asset_depreciation_ids = fields.One2many(
        comodel_name='asset.depreciation.balance',
        inverse_name='balance_id',
        string='Quote di ammortamento',
    )

    balance_line_amount_difference_ids = fields.One2many(
        comodel_name='asset.category.difference',
        inverse_name='balance_id',
        string='Differenze Quote di ammortamento',
    )

