# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2021-22 powERP enterprise network <https://www.powerp.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AssetDepreciationLine(models.Model):
    _name = 'asset.depreciation.line'
    _inherit = ['asset.depreciation.line', 'mail.thread']
    _description = "Assets Depreciations Lines"

    final = fields.Boolean(
        string="Final",
        track_visibility='onchange',
    )

