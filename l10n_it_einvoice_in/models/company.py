# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ResCompany(models.Model):
    _inherit = "res.company"

    cassa_previdenziale_product_id = fields.Many2one(
        "product.product",
        "Welfare Fund Data Product",
        help="Product used to model DatiCassaPrevidenziale XML element " "on bills.",
    )
    sconto_maggiorazione_product_id = fields.Many2one(
        "product.product",
        "Discount Supplement Product",
        help="Product used to model ScontoMaggiorazione XML element on bills.",
    )
    arrotondamenti_attivi_account_id = fields.Many2one(
        'account.account', 'Active Rounding Account',
        domain=[('deprecated', '=', False)],
        help="Account used for active rounding amount on bills."
        )
    arrotondamenti_passivi_account_id = fields.Many2one(
        'account.account', 'Passive Rounding Account',
        domain=[('deprecated', '=', False)],
        help="Account used for passive rounding amount on bills."
        )
    arrotondamenti_tax_id = fields.Many2one(
        'account.tax', 'Rounding Tax',
        domain=[('type_tax_use', '=', 'purchase'), ('amount', '=', 0.0)],
        help="Tax used for rounding amount on bills."
        )

    def xml_get_company(self, DatiAnagrafici, wizard=None):
        """Get company data from xml file"""
        vat = ""
        if DatiAnagrafici:
            if DatiAnagrafici.IdFiscaleIVA:
                vat = "%s%s" % (
                    DatiAnagrafici.IdFiscaleIVA.IdPaese,
                    DatiAnagrafici.IdFiscaleIVA.IdCodice,
                )
        if not vat:
            if wizard:
                wizard.log_inconsistency(_("E-Invoice without VAT number"))
            else:
                raise UserError(_("E-Invoice without VAT number"))
            return self.env.user.company_id
        if vat.startswith("EUIT"):
            vat = vat[2:]
        if vat == self.env.user.company_id.vat:
            return self.env.user.company_id
        if (
                self.env.user.company_id.vat.startswith("EUIT")
                and vat == self.env.user.company_id.vat[2:]
        ):
            return self.env.user.company_id
        companies = self.search([("vat", "=", vat)])
        if not companies:
            raise UserError(
                _(
                    "VAT number %s of customer invoice "
                    "is not the same of the current company" % vat
                )
            )
        return companies[0]


class AccountConfigSettings(models.TransientModel):
    _inherit = "account.config.settings"

    cassa_previdenziale_product_id = fields.Many2one(
        related="company_id.cassa_previdenziale_product_id",
    )
    sconto_maggiorazione_product_id = fields.Many2one(
        related="company_id.sconto_maggiorazione_product_id",
        string="Discount Supplement Product",
        help="Product used to model ScontoMaggiorazione XML element on bills.",
    )
    arrotondamenti_attivi_account_id = fields.Many2one(
        related='company_id.arrotondamenti_attivi_account_id',
    )
    arrotondamenti_passivi_account_id = fields.Many2one(
        related='company_id.arrotondamenti_passivi_account_id',
    )
    arrotondamenti_tax_id = fields.Many2one(
        related='company_id.arrotondamenti_tax_id',
    )

    @api.onchange("company_id")
    def onchange_company_id(self):
        res = super(AccountConfigSettings, self).onchange_company_id()
        for field in ("cassa_previdenziale_product_id",
                      "sconto_maggiorazione_product_id",
                      "arrotondamenti_attivi_account_id",
                      "arrotondamenti_passivi_account_id",
                      "arrotondamenti_tax_id"):
            if self.company_id:
                company = self.company_id
                setattr(
                    company,
                    field,
                    getattr(company, field) and getattr(company, field).id or False)
            else:
                setattr(self, field, False)
        return res
