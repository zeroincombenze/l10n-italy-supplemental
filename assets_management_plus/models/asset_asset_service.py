# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

from odoo import models, fields
import odoo.addons.decimal_precision as dp


class AssetAssetService(models.Model):
    _name = 'asset.asset.service'
    _description = 'Spese di manutenzione'

    name = fields.Char(string='Descrizione', required=True)

    code = fields.Char(string='Codice', required=True)

    service_rate = fields.Float(
        string='% di manutenzione',
        digits=dp.get_precision('Account')
    )
