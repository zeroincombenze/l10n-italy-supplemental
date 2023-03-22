# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AssetDepreciationBalance(models.Model):
    _name = 'asset.depreciation.balance'
    _description = "Assets Depreciations Temporary"

    balance_id = fields.Many2one(
        'italy.account.balance',
        string="Bilancio",
    )

    asset_id = fields.Many2one(
        'asset.asset',
        readonly=True,
        string="Asset",
    )

    type_id = fields.Many2one('asset.depreciation.type',
                              string="Depreciation Type")

    category_id = fields.Many2one(
        'asset.category',
        readonly=True,
        string="Category",
    )

    date_start = fields.Date(string="Date Start")

    pro_rata_temporis = fields.Boolean(string="Pro-rata Temporis")

    percentage = fields.Float(string="Depreciation (%)")

    mode_id = fields.Many2one(
        'asset.depreciation.mode',
        string="Mode",
    )

    last_depreciation_date = fields.Date(
        string="Last Dep.",
    )

    amount_depreciable = fields.Monetary(string="Depreciable Amount")

    amount_depreciable_updated = fields.Monetary(
        string="Updated Amount",
    )

    amount_current = fields.Monetary(
        string="Quota ammortamento",
    )

    amount_depreciated = fields.Monetary(
        string="Depreciated Amount",
    )

    amount_residual = fields.Monetary(
        string="Residual Amount",
    )

    base_coeff = fields.Float(
        default=1,
        help="Coeff to compute amount depreciable from purchase amount",
        string="Depreciable Base Coeff",
    )

    currency_id = fields.Many2one(
        'res.currency', readonly=True, related='asset_id.currency_id',
        string="Currency"
    )

    company_id = fields.Many2one(
        'res.company', readonly=True, related='asset_id.company_id',
        string="Company"
    )

    @api.model
    def load_asset_depreciations(self, asset, date_end, balance):
        ids = []

        for adp in asset.depreciation_ids:
            _logger.info(
                'asset {bene} - tipo {tipo} modo {modo}'.format(
                    bene=asset.name, tipo=adp.type_id.name,
                    modo=adp.mode_id.name
                )
            )

            if not self.is_valid_appreciation(asset, adp, date_end):
                continue

            vals = {
                'balance_id': balance.id,
                'asset_id': adp.asset_id.id,
                'category_id': adp.asset_id.category_id.id,
                'type_id': adp.type_id.id,
                'date_start': adp.date_start,
                'pro_rata_temporis': adp.pro_rata_temporis,
                'percentage': adp.percentage,
                'mode_id': adp.mode_id.id,
                'amount_current': None,
                'amount_depreciable': adp.amount_depreciable,
                'amount_depreciable_updated': adp.amount_depreciable_updated,
                'amount_depreciated': adp.amount_depreciated,
                'last_depreciation_date': adp.last_depreciation_date,
                'amount_residual': adp.amount_residual,
                'base_coeff': adp.base_coeff,
                'currency_id': adp.currency_id.id,
                'company_id': adp.company_id.id,
            }
            # in balance, update quote of depreciation and residual
            vals = self.update_totals_by_date(vals, adp, date_end)

            # create line
            adpc = self.create(vals)

            ids.append(adpc.id)
        return ids

    def update_totals_by_date(self, vals, adp, date):

        # type id civilistico
        final_lines = adp.line_ids.filtered(lambda l: l.final is True)

        if len(final_lines) > 0:
            nr_lines = len(final_lines) + 1
        else:
            nr_lines = 1

        adp = adp.with_context(dep_nr=nr_lines, used_asset=adp.asset_id.used)

        # update values
        amount_depreciable = adp.amount_depreciable
        # amount now
        amount_current = adp.get_depreciation_amount(date)
        # residual plus amount
        # if nr_lines > 1:
        left_residual = adp.calculate_residual_summary(date) + amount_current
        # else:
        #     left_residual = adp.calculate_residual_summary(
        #         date)
        # real residual at
        amount_residual = amount_depreciable - left_residual
        # depreciated at
        amount_depreciated = amount_depreciable - amount_residual

        vals.update(
            {
                'amount_depreciable': amount_depreciable,
                'amount_current': amount_current,
                'amount_depreciated': amount_depreciated,
                'amount_residual': amount_residual,
            }
        )
        return vals

    # end update_totals_by_date

    def is_valid_appreciation(self, asset, adp, date_end):

        conf = self.env['res.company'].browse(asset.company_id.id)
        # possiamo mettere in bilancio solo gli ammortamenti civilistici
        # imposto il filtro

        civilistico = conf.compute_civilistico()
        # il fiscale si mette nelle righe per facilitare la differenza
        # tra le quote
        fiscale = conf.compute_fiscale()

        # do not put into this model
        not_for_balance = adp.type_id.id not in [
            civilistico, fiscale]

        # is total depreciated?
        total_dep = asset.state == 'totally_depreciated'

        # out of balance by date?
        if adp.last_depreciation_date:
            # check if last depreciation date is into balance interval dates
            discard_date = adp.last_depreciation_date <= date_end
        else:
            discard_date = False

        # total depreciated and out of balance jump away
        totally_depreciated = total_dep and discard_date

        if not_for_balance or totally_depreciated:
            return False
        else:
            return True

    # end is_valid_appreciation

    def get_total_by_category_nature(self, balance_id, nature_id, category_id):

        lines = self.search([
            ('balance_id', '=', balance_id),
            ('category_id', '=', category_id),
            ('type_id', '=', nature_id),
        ])
        tt = sum(lines.mapped('amount_current'))
        return sum(lines.mapped('amount_current'))

