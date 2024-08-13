
from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def get_taxes_values(self):
        # for line in self.invoice_line_ids:
        #     if line.quantity < 0.0 and line.price_unit >= 0.0:
        #         line.quantity = -line.quantity
        #         line.price_unit = -line.price_unit
        tax_grouped = super(AccountInvoice, self).get_taxes_values()
        round_curr = self.currency_id.round
        Tax = self.env["account.tax"]
        if self.company_id.tax_calculation_rounding_method == "round_globally":
            for val in tax_grouped.items():
                taxes = Tax.browse(val[1]["tax_id"]).compute_all(val[1]["base"])
                val[1]["base"] = taxes["total_excluded"]
                val[1]["amount"] = round_curr(taxes["total_included"]
                                              - taxes["total_excluded"])
        return tax_grouped
