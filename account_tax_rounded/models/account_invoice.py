
from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model_cr
    def _register_hook(self):

        @api.multi
        def get_taxes_values_rounded(self):
            tax_grouped = {}
            round_curr = self.currency_id.round
            Tax = self.env["account.tax"]
            for line in self.invoice_line_ids:
                price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = (
                    line.invoice_line_tax_ids.compute_all(
                        price_unit, self.currency_id,
                        line.quantity, line.product_id,
                        self.partner_id)["taxes"]
                )
                for tax in taxes:
                    val = self._prepare_tax_line_vals(line, tax)
                    key = Tax.browse(tax["id"]).get_grouping_key(val)

                    if key not in tax_grouped:
                        tax_grouped[key] = val
                        tax_grouped[key]["base"] = round_curr(val["base"])
                    else:
                        tax_grouped[key]["amount"] += val["amount"]
                        tax_grouped[key]["base"] += round_curr(val["base"])
            if self.company_id.tax_calculation_rounding_method == "round_globally":
                for val in tax_grouped.items():
                    taxes = Tax.browse(val[1]["tax_id"]).compute_all(val[1]["base"])
                    val[1]["base"] = taxes["total_excluded"]
                    val[1]["amount"] = round_curr(taxes["total_included"]
                                                  - taxes["total_excluded"])
            return tax_grouped

        self._patch_method("get_taxes_values",
                           get_taxes_values_rounded)
        return super(AccountInvoice, self)._register_hook()
