# -*- coding: utf-8 -*-
#
# Copyright 2018-19 - Odoo Italia Associazione <https://www.odoo-italia.org>
# Copyright 2018-19 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ResCompany(models.Model):
    _inherit = "res.company"
    sconto_maggiorazione_product_id = fields.Many2one(
        "product.product",
        "Discount Supplement Product",
        help="Product used to model ScontoMaggiorazione XML element on bills.",
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
        if vat and vat == self.env.user.company_id.vat:
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
    sconto_maggiorazione_product_id = fields.Many2one(
        related="company_id.sconto_maggiorazione_product_id",
        string="Discount Supplement Product",
        help="Product used to model ScontoMaggiorazione XML element on bills.",
    )

    @api.onchange("company_id")
    def onchange_company_id(self):
        res = super(AccountConfigSettings, self).onchange_company_id()
        if self.company_id:
            company = self.company_id
            self.sconto_maggiorazione_product_id = (
                company.sconto_maggiorazione_product_id
                and company.sconto_maggiorazione_product_id.id
                or False
            )
        else:
            self.sconto_maggiorazione_product_id = False
        return res
