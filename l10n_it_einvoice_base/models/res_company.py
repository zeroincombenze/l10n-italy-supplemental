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


class ResCompany(models.Model):
    _inherit = "res.company"

    fatturapa_fiscal_position_id = fields.Many2one(
        "fatturapa.fiscal_position",
        "Fiscal Position",
        help="Fiscal position used by electronic invoice",
    )
    fatturapa_sequence_id = fields.Many2one(
        "ir.sequence",
        "Sequence",
        help="The univocal progressive of the file is represented by "
        "an alphanumeric sequence of maximum length 5, "
        "its values are included in 'A'-'Z' and '0'-'9'",
    )
    fatturapa_art73 = fields.Boolean("Art. 73")
    fatturapa_pub_administration_ref = fields.Char(
        "Public Administration Reference Code",
        size=20,
    )
    fatturapa_rea_office = fields.Many2one(
        related="partner_id.rea_office", string="REA Office"
    )
    fatturapa_rea_number = fields.Char(
        related="partner_id.rea_code", string="REA Number"
    )
    fatturapa_rea_capital = fields.Float(
        related="partner_id.rea_capital", string="REA Capital"
    )
    fatturapa_rea_partner = fields.Selection(
        related="partner_id.rea_member_type", string="Member Type"
    )
    fatturapa_rea_liquidation = fields.Selection(
        related="partner_id.rea_liquidation_state", string="Liquidation State"
    )
    fatturapa_tax_representative = fields.Many2one(
        "res.partner", "Legal Tax Representative"
    )
    fatturapa_sender_partner = fields.Many2one(
        "res.partner",
        "Third Party/Sender",
        help="Data of Third-Party Issuer Intermediary who emits the "
        "invoice on behalf of the seller/provider",
    )
    fatturapa_stabile_organizzazione = fields.Many2one(
        "res.partner",
        "Stable Organization",
        help="The fields must be entered only when the seller/provider is "
        "non-resident, with a stable organization in Italy",
    )
    einvoice_sender_id = fields.Many2one(
        "italy.ade.sender",
        "E-Invoice Sender Channel",
        help="Sender Channel used to send e-Invoices",
    )
    einvoice_xeu_vat_none = fields.Char(
        "No EU customer TIN",
        help="No EU customer vat number in XML file.\n"
        "Usually is OO99999999999 but may depends by sender.\n"
        "%(iso) means iso code of customer.",
        default="%(iso)s99999999999",
    )
    einvoice_xeu_fc_none = fields.Char(
        "No EU customer fc",
        help="No EU customer fiscal code in XML file.\n"
        "Usually is 00000000000 but may depends by sender.\n"
        "%(iso) means iso code of customer.",
        default="",
    )
    einvoice_no_eq_cf_pi = fields.Boolean(
        "No FC if same of TIN",
        help="Do not insert fiscalcode if it is equal to VAT number",
        default=False,
    )
    pa_move_pi_2_fc = fields.Boolean(
        "Move TIN to FC if partner is PA",
        help="If partner has TIN and not fiscalcode, move TIN to fiscalcode\n"
        "If both are set, do not insert TIN",
        default=True,
    )
    fatturapa_preview_style = fields.Selection(
        [
            ("fatturaordinaria_v1.2.1.xsl", "FatturaOrdinaria v1.2.1"),
            ("FoglioStileAssoSoftware_v1.1.xsl", "AssoSoftware v1.1"),
        ],
        string="Preview Format Style",
        required=True,
        default="fatturaordinaria_v1.2.1.xsl",
    )

    @api.multi
    @api.constrains("fatturapa_sequence_id")
    def _check_fatturapa_sequence_id(self):
        for company in self:
            if company.fatturapa_sequence_id:
                if company.fatturapa_sequence_id.use_date_range:
                    raise ValidationError(
                        _("Sequence %s can't use subsequences.")
                        % company.fatturapa_sequence_id.name
                    )
                journal = self.env["account.journal"].search(
                    [("sequence_id", "=", company.fatturapa_sequence_id.id)], limit=1
                )
                if journal:
                    raise ValidationError(
                        _(
                            "Sequence %s already used by journal %s. Please select"
                            " another one."
                        )
                        % (company.fatturapa_sequence_id.name, journal.name)
                    )

    def set_cash_accounting(self):
        tax_model = self.env["account.tax"]
        where = ["|", ("company_id", "=", False), ("company_id", "=", self.id)]
        where.append(("type_tax_use", "=", "sale"))
        where.append(("amount", "!=", 0.0))
        where.append(("kind_id", "=", False))
        where.append("|")
        where.append(("payability", "=", "I"))
        where.append(("payability", "=", False))
        for _tax in tax_model.search(where):
            tax_model.write({"payability": "D"})

    def set_ordinary_vat(self):
        tax_model = self.env["account.tax"]
        where = ["|", ("company_id", "=", False), ("company_id", "=", self.id)]
        where.append(("type_tax_use", "=", "sale"))
        where.append(("amount", "!=", 0.0))
        where.append(("kind_id", "=", False))
        where.append(("payability", "=", "D"))
        for _tax in tax_model.search(where):
            tax_model.write({"payability": "I"})

    @api.multi
    def write(self, vals):
        res = super(ResCompany, self).write(vals)
        for rec in self:
            if rec.fatturapa_fiscal_position_id.code == "RF01":
                rec.set_ordinary_vat()
            elif rec.fatturapa_fiscal_position_id.code == "RF17":
                rec.set_cash_accounting()
        return res


class AccountConfigSettings(models.TransientModel):
    _inherit = "account.config.settings"

    fatturapa_fiscal_position_id = fields.Many2one(
        related="company_id.fatturapa_fiscal_position_id",
        string="Fiscal Position",
        help="Fiscal position used by electronic invoice",
    )
    fatturapa_sequence_id = fields.Many2one(
        related="company_id.fatturapa_sequence_id",
        string="Sequence",
        help="The univocal progressive of the file is represented by "
        "an alphanumeric sequence of maximum length 5, "
        "its values are included in 'A'-'Z' and '0'-'9'",
    )
    fatturapa_art73 = fields.Boolean(
        related="company_id.fatturapa_art73",
        string="Art. 73",
        help="Indicates whether the document has been issued according to "
        "methods and terms laid down in a ministerial decree under "
        "the terms of Article 73 of Italian Presidential Decree "
        "633/72 (this enables the company to issue in the same "
        "year several documents with same number)",
    )
    fatturapa_pub_administration_ref = fields.Char(
        related="company_id.fatturapa_pub_administration_ref",
        string="Public Administration Reference Code",
    )
    fatturapa_rea_office = fields.Many2one(
        related="company_id.fatturapa_rea_office", string="REA Office"
    )
    fatturapa_rea_number = fields.Char(
        related="company_id.fatturapa_rea_number", string="REA Number"
    )
    fatturapa_rea_capital = fields.Float(
        related="company_id.fatturapa_rea_capital", string="REA Capital"
    )
    fatturapa_rea_partner = fields.Selection(
        related="company_id.fatturapa_rea_partner", string="REA Copartner"
    )
    fatturapa_rea_liquidation = fields.Selection(
        related="company_id.fatturapa_rea_liquidation", string="REA Liquidation"
    )
    fatturapa_tax_representative = fields.Many2one(
        related="company_id.fatturapa_tax_representative",
        string="Legal Tax Representative",
        help="The fields must be entered only when the seller/provider makes "
        "use of a tax representative in Italy",
    )
    fatturapa_sender_partner = fields.Many2one(
        related="company_id.fatturapa_sender_partner",
        string="Third Party/Sender",
        help="Data of Third-Party Issuer Intermediary who emits the "
        "invoice on behalf of the seller/provider",
    )
    fatturapa_stabile_organizzazione = fields.Many2one(
        related="company_id.fatturapa_stabile_organizzazione",
        string="Stable Organization",
        help="The fields must be entered only when the seller/provider is "
        "non-resident, with a stable organization in Italy",
    )
    einvoice_sender_id = fields.Many2one(
        related="company_id.einvoice_sender_id",
        string="E-Invoice Sender Channel",
        help="Sender Channel used to send e-Invoices",
    )
    einvoice_xeu_vat_none = fields.Char(
        related="company_id.einvoice_xeu_vat_none",
        string="No EU customer TIN",
        help="No EU customer vat number in XML file.\n"
        "Usually is OO99999999999 but may depends by sender.\n"
        "%(iso) means iso code of customer.",
        default="OO99999999999",
    )
    einvoice_xeu_fc_none = fields.Char(
        related="company_id.einvoice_xeu_fc_none",
        string="No EU customer fc",
        help="No EU customer fiscal code in XML file.\n"
        "Usually is 00000000000 but may depends by sender.\n"
        "%(iso) means iso code of customer.",
        default="0000000000",
    )
    pa_move_pi_2_fc = fields.Boolean(
        related="company_id.pa_move_pi_2_fc",
        string="Move TIN to FC if partner is PA",
        help="If partner has TIN and not fiscalcode, move TIN to fiscalcode\n"
        "If both are set, do not insert TIN",
        default=False,
    )
    einvoice_no_eq_cf_pi = fields.Boolean(
        related="company_id.einvoice_no_eq_cf_pi",
        string="No FC if same of TIN",
        help="Do not insert fiscalcode if it is equal to VAT number",
        default=True,
    )
    fatturapa_preview_style = fields.Selection(
        related="company_id.fatturapa_preview_style",
        string="Preview Format Style",
        required=True,
    )

    @api.onchange("company_id")
    def onchange_company_id(self):
        res = super(AccountConfigSettings, self).onchange_company_id()
        if self.company_id:
            company = self.company_id
            default_sequence = self.env["ir.sequence"].search(
                [("code", "=", "account.invoice.fatturapa")]
            )
            default_sequence = default_sequence[0].id if default_sequence else False
            self.fatturapa_fiscal_position_id = (
                company.fatturapa_fiscal_position_id
                and company.fatturapa_fiscal_position_id.id
                or False
            )
            self.fatturapa_sequence_id = (
                company.fatturapa_sequence_id
                and company.fatturapa_sequence_id.id
                or default_sequence
            )
            self.fatturapa_art73 = company.fatturapa_art73 or False
            self.fatturapa_pub_administration_ref = (
                company.fatturapa_pub_administration_ref or False
            )
            self.fatturapa_rea_office = (
                company.fatturapa_rea_office
                and company.fatturapa_rea_office.id
                or False
            )
            self.fatturapa_rea_number = company.fatturapa_rea_number or False
            self.fatturapa_rea_capital = company.fatturapa_rea_capital or False
            self.fatturapa_rea_partner = company.fatturapa_rea_partner or False
            self.fatturapa_rea_liquidation = company.fatturapa_rea_liquidation or False
            self.fatturapa_tax_representative = (
                company.fatturapa_tax_representative
                and company.fatturapa_tax_representative.id
                or False
            )
            self.fatturapa_sender_partner = (
                company.fatturapa_sender_partner
                and company.fatturapa_sender_partner.id
                or False
            )
            self.fatturapa_stabile_organizzazione = (
                company.fatturapa_stabile_organizzazione
                and company.fatturapa_stabile_organizzazione.id
                or False
            )
            self.einvoice_sender_id = (
                company.einvoice_sender_id and company.einvoice_sender_id.id or False
            )
        else:
            self.fatturapa_fiscal_position_id = False
            self.fatturapa_sequence_id = False
            self.fatturapa_art73 = False
            self.fatturapa_pub_administration_ref = False
            self.fatturapa_rea_office = False
            self.fatturapa_rea_number = False
            self.fatturapa_rea_capital = False
            self.fatturapa_rea_partner = False
            self.fatturapa_rea_liquidation = False
            self.fatturapa_tax_representative = False
            self.fatturapa_sender_partner = False
            self.fatturapa_stabile_organizzazione = False
            self.einvoice_sender_id = False
        return res
