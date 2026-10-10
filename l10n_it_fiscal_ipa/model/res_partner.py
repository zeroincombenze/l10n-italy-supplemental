# -*- coding: utf-8 -*-
#
# Copyright 2014    - KTec S.r.l.
# Copyright 2018-19 - Odoo Italia Associazione <https://www.odoo-italia.org>
# Copyright 2018-19 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

STANDARD_ADDRESSEE_CODE = "0000000"


class ResPartner(models.Model):
    _inherit = "res.partner"

    ipa_code = fields.Char(string="IPA Code")
    is_pa = fields.Boolean("Public administration")
    # FatturaPa  1.1.4
    codice_destinatario = fields.Char(
        "Recipient Code",
        help="Tag 1.1.4 <CodiceDestinatario>\n"
        "Il codice, di 7 caratteri, assegnato dal SdI ai soggetti che "
        "hanno accreditato un canale; qualora il destinatario non abbia "
        "accreditato un canale presso Sdi e riceva via PEC le fatture, "
        "l'elemento deve essere valorizzato con'%s'. " % STANDARD_ADDRESSEE_CODE,
        default=STANDARD_ADDRESSEE_CODE,
    )
    electronic_invoice_subjected = fields.Boolean("Subjected to electronic invoice")
    eori_code = fields.Char(
        "EORI Code",
        size=20,
        help="Tag 1.4.1.3.5 <CodEORI>\n"
             "Numero Codice EORI (Economic Operator Registration and Identification)"
             " in base al Regolamento (CE) n. 312 del 16 aprile 2009."
             " In vigore dal 1 luglio 2009"
    )
    license_number = fields.Char("License Code", size=20)
    # FatturaPA 1.1.6
    pec_destinatario = fields.Char(
        "PEC destinatario",
        help="Tag 1.1.6 <PECDestinatario>\n"
        "PEC usata per l'invio della fattura elettronica. "
        "Da compilare solo se "
        "<CodiceDestinatario> is '%s'" % STANDARD_ADDRESSEE_CODE,
    )
    # 1.2.6 RiferimentoAmministrazione
    pa_partner_code = fields.Char(
        "PA Code for Partner", size=20, help="Tag 1.2.6 <RiferimentoAmministrazione>"
    )
    type_inv_addr = fields.Selection(
        [
            ("0", "Simple"),
            ("SO", "Stable Organization"),
            ("FR", "Fiscal Representative"),
        ],
        "Type of Invoice Address",
        default="0",
    )

    @api.onchange("electronic_invoice_subjected")
    def onchange_electronic_invoice_subjected(self):
        if (self.vat or self.fiscalcode) and not self.codice_destinatario:
            self.codice_destinatario = "0000000"

    @api.multi
    @api.constrains(
        "is_pa",
        "ipa_code",
        "codice_destinatario",
        "electronic_invoice_subjected",
        "vat",
    )
    def _check_codice_destinatario(self):
        for partner in self:
            if partner.electronic_invoice_subjected and partner.is_pa:
                raise ValidationError(
                    _("Partner %s dichiarato sia PA che Fattura B2B!") % partner.name
                )
            if partner.is_pa and (not partner.ipa_code or len(partner.ipa_code) != 6):
                raise ValidationError(
                    _(
                        "Il partner %s è una PA: "
                        "deve avere il codice IPA di 6 caratteri"
                    )
                    % partner.name
                )
            if partner.electronic_invoice_subjected:
                if (
                    not partner.vat
                    and not partner.fiscalcode
                    and (
                        not partner.codice_destinatario
                        or partner.codice_destinatario != "XXXXXXX"
                    )
                ):
                    raise ValidationError(
                        _(
                            "Partner %s, soggetto a Fattura Elettronica "
                            "ma senza P.IVA ne codice fiscale"
                        )
                        % partner.name
                    )
                if (
                    not partner.codice_destinatario
                    or len(partner.codice_destinatario) != 7
                ):
                    raise ValidationError(
                        _(
                            "Partner %s, soggetto a Fattura Elettronica: "
                            "deve avere il codice destinatario di 7 caratteri "
                            "eventualmente valorizzato con 0000000"
                        )
                        % partner.name
                    )
