# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

import logging
from odoo import models, fields
import odoo.addons.decimal_precision as dp


_logger = logging.getLogger(__name__)


class AssetDepreciationDeduction(models.Model):
    _name = 'asset.depreciation.deduction'
    _description = 'Tipo deducibilità'

    name = fields.Char(string='Descrizione', required=True)

    code = fields.Char(string='Codice', required=True)

    deduction_rate = fields.Float(
        string='Percentuale di deducibilità',
        digits=dp.get_precision('Account')
    )

    deduction_limit = fields.Float(
        string='Limite deducibilità',
        digits=dp.get_precision('Account')
    )
