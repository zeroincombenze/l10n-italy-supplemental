# -*- coding: utf-8 -*-
#
# Copyright 2018-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    customer_payment_term = fields.Selection(
        [("customer", "From e-invoice file"), ("company", "Local payment assigned")],
        "Customer Payment Term",
        default="company",
        help="Which payment term will be loaded in imported sale invoice; may be:"
        "\nfrom the e-invoice file (warning: payment term must exist)"
        "\nuse the payment term assigned in the customer record",
    )
    arrotondamenti_tax_sale_id = fields.Many2one(
        "account.tax",
        "Rounding Tax on sale",
        domain=[("type_tax_use", "=", "sale"), ("amount", "=", 0.0)],
        help="Tax used for rounding amount on imported sale invoices.",
    )
    customer_product_search = fields.Selection(
        [
            ("c", "By internal code"),
            ("cn", "By code or exact name"),
            ("cndx", "By code or similar name"),
            ("n", "By exact name"),
        ],
        "Customer product search",
        default="c",
        help="How to search for product from sale e-invoice",
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = "account.config.settings"

    arrotondamenti_tax_sale_id = fields.Many2one(
        related="company_id.arrotondamenti_tax_sale_id",
    )
    customer_payment_term = fields.Selection(
        related="company_id.customer_payment_term",
    )
    customer_product_search = fields.Selection(
        related="company_id.customer_product_search",
    )
