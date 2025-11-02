# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

HELP = "Testo da inserire in fattura"
DEFAULT = "Imposta di bollo assolta virtualmente ai sensi del D.M. 17.06.2014"


class ResCompany(models.Model):
    _inherit = "res.company"

    tax_stamp_product_id = fields.Many2one(
        "product.product",
        "Tax Stamp Product",
        help="Product used as Tax Stamp in customer invoices.",
    )
    text_stamp = fields.Char(
        "Note su fattura",
        help=HELP,
        default=DEFAULT,
    )
    aut_min_bv = fields.Char("Autorizzazione ministeriale")


class AccountConfigSettings(models.TransientModel):
    _inherit = "account.config.settings"

    tax_stamp_product_id = fields.Many2one(
        related="company_id.tax_stamp_product_id",
        string="Tax Stamp Product",
        help="Product used as Tax Stamp in customer invoices.",
    )
    text_stamp = fields.Char(
        related="company_id.text_stamp",
        string="Note su fattura",
        help=HELP,
        default=DEFAULT,
    )
    aut_min_bv = fields.Char(
        related="company_id.aut_min_bv", string="Autorizzazione ministeriale"
    )

    @api.onchange("company_id")
    def onchange_company_id(self):
        res = super(AccountConfigSettings, self).onchange_company_id()
        if self.company_id:
            company = self.company_id
            self.tax_stamp_product_id = (
                company.tax_stamp_product_id
                and company.tax_stamp_product_id.id
                or False
            )
        else:
            self.tax_stamp_product_id = False
        return res
