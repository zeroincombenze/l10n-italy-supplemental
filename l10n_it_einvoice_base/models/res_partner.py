# -*- coding: utf-8 -*-
#
# Copyright 2018-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

STANDARD_ADDRESSEE_CODE = "0000000"


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    regime_fiscale = fields.Many2one("fatturapa.fiscal_position", string="Tax Regime")
    fiscal_document_type_id = fields.Many2one(
        'italy.ade.invoice.type',
        string="Fiscal Document Type",
        oldname="invoice_type_id",
        help="To be used when sending self invoices to the exchange system")


class ResPartner(models.Model):
    _inherit = "res.partner"

    # 1.2.1.4
    register = fields.Char("Professional Register", size=60)
    # 1.2.1.5
    register_province = fields.Many2one("res.country.state", string="Register Province")
    # 1.2.1.6
    register_code = fields.Char("Register Registration Number", size=60)
    # 1.2.1.7
    register_regdate = fields.Date("Register Registration Date")
    # 1.2.1.8
    register_fiscalpos = fields.Many2one(
        "fatturapa.fiscal_position", string="Register Fiscal Position"
    )
    # # 1.1.6
    # pec_destinatario = fields.Char(
    #     "Addressee PEC",
    #     help="PEC to which the electronic invoice will be sent. "
    #     "Must be filled "
    #     "ONLY when the information element "
    #     "<CodiceDestinatario> is '0000000'",
    # )

    @api.multi
    @api.constrains(
        "is_pa",
        "ipa_code",
        "codice_destinatario",
        "company_type",
        "electronic_invoice_subjected",
        "vat",
        "fiscalcode",
        "customer",
        "street",
        "zip",
        "city",
        "state_id",
        "country_id",
    )
    def _check_ftpa_partner_data(self):
        for partner in self:
            if partner.electronic_invoice_subjected and partner.customer:
                # These checks must be done for customers only, as only
                # needed for XML generation
                if partner.is_pa and (
                    not partner.ipa_code or len(partner.ipa_code) != 6
                ):
                    raise ValidationError(
                        _(
                            "As a Public Administration, partner %s IPA Code "
                            "must be 6 characters long."
                        )
                        % partner.name
                    )
                if partner.company_type == "person" and (
                    not partner.lastname or not partner.firstname
                ):
                    raise ValidationError(
                        _(
                            "As a natural person, partner %s "
                            "must have Name and Surname."
                        )
                        % partner.name
                    )
                if not partner.is_pa and (
                    not partner.codice_destinatario
                    or len(partner.codice_destinatario) != 7
                ):
                    raise ValidationError(
                        _("Partner %s Addressee Code " "must be 7 characters long.")
                        % partner.name
                    )
                if (
                    not partner.vat
                    and not partner.fiscalcode
                    and (
                        not partner.codice_destinatario
                        or partner.codice_destinatario != "XXXXXXX"
                    )
                ):
                    raise ValidationError(
                        _("Partner %s must have VAT Number or Fiscal Code.")
                        % partner.name
                    )
                if not partner.street:
                    raise ValidationError(
                        _("Customer %s: street is needed for XML generation.")
                        % partner.name
                    )
                if not partner.zip and (
                    not partner.codice_destinatario
                    or partner.codice_destinatario != "XXXXXXX"
                ):
                    raise ValidationError(
                        _("Customer %s: ZIP is needed for XML generation.")
                        % partner.name
                    )
                if not partner.city:
                    raise ValidationError(
                        _("Customer %s: city is needed for XML generation.")
                        % partner.name
                    )
                if not partner.country_id:
                    raise ValidationError(
                        _("Customer %s: country is needed for XML" " generation.")
                        % partner.name
                    )
