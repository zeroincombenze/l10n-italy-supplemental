# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AssetCategoryDifference(models.Model):
    _name = 'asset.category.difference'
    _description = "Quote amount difference by category"

    balance_id = fields.Many2one(
        'italy.account.balance',
        string="Bilancio",
    )

    category_id = fields.Many2one(
        'asset.category',
        readonly=True,
        string="Categoria",
    )

    amount_current_civilistico = fields.Monetary(
        string="Quota ammortamento civilistico",
    )

    amount_current_fiscale = fields.Monetary(
        string="Quota ammortamento fiscale",
    )

    amount_balance = fields.Monetary(
        string="Differenza",
    )

    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.user.company_id)

    currency_id = fields.Many2one(
        'res.currency', readonly=True, related='company_id.currency_id',
        string="Currency"
    )

    @api.model
    def load_differences(self, company_id, balance_id):
        conf = self.env['res.company'].browse(company_id.id)
        civilistico = conf.compute_civilistico()
        fiscale = conf.compute_fiscale()
        asset_dp_model = self.env['asset.depreciation.balance']

        lines = asset_dp_model.search([
            ('balance_id', '=', balance_id),
        ])

        categories = lines.mapped('category_id')

        for category in categories:

            total_civilistico = asset_dp_model.get_total_by_category_nature(
                balance_id,
                civilistico,
                category.id
            )

            total_fiscale = asset_dp_model.get_total_by_category_nature(
                balance_id,
                fiscale,
                category.id
            )

            vals = {
                'balance_id': balance_id,
                'category_id': category.id,
                'amount_current_civilistico': total_civilistico,
                'amount_current_fiscale': total_fiscale,
                'amount_balance': total_civilistico - total_fiscale,
                'company_id': company_id.id,
                'currency_id': company_id.currency_id.id,
            }

            adpc = self.create(vals)

