# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    # ------------------------------------------------------------------
    # Main template data
    # ------------------------------------------------------------------
    @template('it_coa')
    def _get_it_coa_template_data(self):
        return {
            'name': "Italia - Piano dei conti (Zeroincombenze)",
            'code_digits': '6',
            'property_account_receivable_id': '152100',
            'property_account_payable_id': '250100',
            'property_account_expense_categ_id': '610100',
            'property_account_income_categ_id': '510100',
        }

    # ------------------------------------------------------------------
    # Company specific data
    # ------------------------------------------------------------------
    @template('it_coa', 'res.company')
    def _get_it_coa_res_company(self):
        return {
            self.env.company.id: {
                'account_fiscal_country_id': 'base.it',
                'bank_account_code_prefix': '1810',
                'cash_account_code_prefix': '1800',
                'transfer_account_code_prefix': '1830',
                'account_default_pos_receivable_account_id': '152130',
                'income_currency_exchange_account_id': '720170',
                'expense_currency_exchange_account_id': '731170',
                'tax_calculation_rounding_method': 'round_per_line',
                'account_sale_tax_id': '22v',
                'account_purchase_tax_id': '22a',
            },
        }
