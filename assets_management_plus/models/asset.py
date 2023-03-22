# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class Asset(models.Model):
    _inherit = 'asset.asset'

    def _default_deduction_rate(self):
        rate = 0.0
        if self.deduction_type:
            rate = self.deduction_type.deduction_rate
        return rate

    def _default_deduction_limit(self):
        limit = 0.0
        if self.deduction_type and self.deduction_type.deduction_limit:
            limit = self.deduction_type.deduction_limit
        return limit

    purchase_qty = fields.Integer(string='Quantità acquistata', default=0)

    # group_ids = fields.Many2many(
    #     comodel_name='account.asset.group',
    #     relation="asset_group_rel",
    #     column1="asset_id",
    #     column2="group_id",
    #     string='Gruppo cespiti')

    deduction_type = fields.Many2one(
        'asset.depreciation.deduction',
        string='Tipo deducibilità',
    )

    service_type = fields.Many2one(
        'asset.asset.service',
        string='% spese di manutenzione',
    )

    deduction_rate = fields.Float(
        string='Percentuale di deducibilità',
        digits=dp.get_precision('Account'),
        default=_default_deduction_rate,
    )

    deduction_limit = fields.Float(
        string='Limite deducibilità',
        digits=dp.get_precision('Account'),
        default=_default_deduction_limit,
    )

    active = fields.Boolean(string="Bene in uso", default=True)

    serial_number = fields.Char(string='Matricola',)

    service_contract = fields.Boolean(string="Contratto di manutenzione",
                                      default=False)

    note = fields.Text(string='Note',)

    @api.onchange('deduction_type')
    def onchange_deduction_type(self):
        if self.deduction_type:
            dep = self._get_fiscal_depreciation()
            if dep.line_ids:
                return {
                    'warning': {
                        'title': "Attenzione!",
                        'message': "Sono presenti degli ammortamenti che non "
                                   "permettono la modifica del tipo."},
                }
            # if not self.deduction_rate:
            self.deduction_rate = self.deduction_type.deduction_rate
            # if not self.deduction_limit:
            self.deduction_limit = self.deduction_type.deduction_limit
            # check on deduction limit
            # TODO only consolidato?
            if self.deduction_limit > 1 and not dep.line_ids:
                if dep.amount_depreciable > self.deduction_limit:
                    amount_depreciable = self.deduction_limit
                    amount_depreciable_updated = amount_depreciable
                    amount_residual = amount_depreciable
                    base_coeff = self.deduction_rate / 100
                    dep.update({
                        'amount_depreciable': amount_depreciable,
                        'amount_depreciable_updated': amount_depreciable_updated,
                        'amount_residual': amount_residual,
                    })
            else:
                if not dep.line_ids:
                    for cat_type in self.category_id.type_ids:
                        if cat_type.depreciation_type_id.id == dep.type_id.id:
                            amount_depreciable = self.purchase_amount\
                                                 * cat_type.base_coeff
                            dep.update({
                                'amount_depreciable': amount_depreciable,
                                'base_coeff': cat_type.base_coeff,
                                'amount_depreciable_updated': amount_depreciable,
                                'amount_residual': amount_depreciable,
                            })

    @api.model
    def create(self, vals):
        asset = super().create(vals)
        fiscale = self._get_fiscal_id(asset.company_id.id)

        if 'deduction_limit' in vals:
            if vals['deduction_limit'] > 1:
                # update fiscal depreciation
                fiscal_depreciation = asset.depreciation_ids.filtered(
                    lambda x: x.type_id.id == fiscale
                )
                fs_amount = fiscal_depreciation.amount_depreciable
                if fs_amount > vals['deduction_limit']:
                    amount_depreciable = vals['deduction_limit']
                    amount_depreciable_updated = amount_depreciable
                    amount_residual = amount_depreciable
                    base_coeff = vals['deduction_rate'] / 100
                    fiscal_depreciation.write({
                        'amount_depreciable': amount_depreciable,
                        'amount_depreciable_updated': amount_depreciable_updated,
                        'amount_residual': amount_residual,

                    })
                # end if
            # end if
        # end if
        return asset

    @api.model
    def _get_fiscal_id(self, company_id):
        conf = self.env['res.company'].browse(company_id)
        fiscale_id = conf.compute_fiscale()
        return fiscale_id
    # end _get_fiscale_id

    @api.model
    def _get_fiscal_depreciation(self):
        company = self.company_id.id
        fiscale = self._get_fiscal_id(company)
        fiscal_depreciation = self.depreciation_ids.filtered(
            lambda x: x.type_id.id == fiscale
        )
        if not fiscal_depreciation:
            raise UserError('Attenzione!\nL\'ammortamento di tipo fiscale non '
                            'è stato trovato.')
        return fiscal_depreciation
    # end _get_fiscale_depreciation

