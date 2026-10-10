# -*- coding: utf-8 -*-
#    Copyright (C) 2017    SHS-AV s.r.l. <https://www.zeroincombenze.it>
#    Copyright (C) 2017    Didotech srl <http://www.didotech.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# [2017: SHS-AV s.r.l.] First version
#
import base64
import logging
import os

from odoo import _, api, exceptions, fields, models

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
try:
    from unidecode import unidecode

    if os.environ.get("SPESOMETRO_VERSION", "2.1") == "2.0":
        SPESOMETRO_VERSION = "2.0"
        from odoo.addons.l10n_it_ade.bindings.dati_fattura_v_2_0 import (
            AltriDatiIdentificativiNoCAPType,
            AltriDatiIdentificativiNoSedeType,
            CedentePrestatoreDTEType,
            CedentePrestatoreDTRType,
            CessionarioCommittenteDTEType,
            CessionarioCommittenteDTRType,
            CodiceFiscaleType,
            DatiFattura,
            DatiFatturaBodyDTEType,
            DatiFatturaBodyDTRType,
            DatiFatturaHeaderType,
            DatiGeneraliDTRType,
            DatiGeneraliType,
            DatiIVAType,
            DatiRiepilogoType,
            DichiaranteType,
            DTEType,
            DTRType,
            IdentificativiFiscaliITType,
            IdentificativiFiscaliNoIVAType,
            IdentificativiFiscaliType,
            IdFiscaleITType,
            IdFiscaleType,
            IndirizzoNoCAPType,
            IndirizzoType,
            RettificaType,
            VersioneType,
        )
    else:
        SPESOMETRO_VERSION = "2.1"
        from odoo.addons.l10n_it_ade.bindings.dati_fattura_v_2_1 import (  # noqa: F401
            # IndirizzoNoCAPType,
            AltriDatiIdentificativiITType,
            AltriDatiIdentificativiType,
            CedentePrestatoreDTEType,
            CedentePrestatoreDTRType,
            CessionarioCommittenteDTEType,
            CessionarioCommittenteDTRType,
            CodiceFiscaleType,
            DatiFattura,
            DatiFatturaBodyDTEType,
            DatiFatturaBodyDTRType,
            DatiFatturaHeaderType,
            DatiGeneraliDTEType,
            DatiGeneraliDTRType,
            DatiIVAType,
            DatiRiepilogoType,
            DichiaranteType,
            DTEType,
            DTRType,
            IdentificativiFiscaliITType,
            IdentificativiFiscaliNoIVAType,
            IdentificativiFiscaliType,
            IdFiscaleITType,
            IdFiscaleType,
            IndirizzoType,
            RettificaType,
            VersioneType,
        )
    #   ANNType)
except ImportError as err:
    _logger.debug(err)
    raise


VERSIONE = "DAT20"


class WizardVatCommunication(models.TransientModel):
    _name = "wizard.vat.communication"

    data = fields.Binary("File", readonly=True)
    name = fields.Char("Filename", size=32, readonly=True)
    state = fields.Selection((("create", "create"), ("get", "get")), default="create")
    target = fields.Char("Customers/Suppliers", size=4, readonly=True)

    def str60Latin(self, s):
        return unidecode(s)[:60]

    def str80Latin(self, s):
        return unidecode(s)[:80]

    @api.model
    def get_dati_fattura_header(self, commitment_model, commitment, dte_dtr_id):
        fields = commitment_model.get_xml_fattura_header(commitment, dte_dtr_id)
        header = DatiFatturaHeaderType()
        if "xml_CodiceFiscale" in fields:
            header.Dichiarante = DichiaranteType()
            header.Dichiarante.Carica = fields["xml_Carica"].code
            header.Dichiarante.CodiceFiscale = CodiceFiscaleType(
                fields["xml_CodiceFiscale"]
            )
        return header

    @api.model
    def get_sede(self, fields, dte_dtr_id, selector):
        if dte_dtr_id == "DTE":
            if selector == "company":
                sede = IndirizzoType()
            elif selector == "customer":
                if SPESOMETRO_VERSION == "2.0":
                    sede = IndirizzoNoCAPType()
                else:
                    sede = IndirizzoType()
            elif selector == "supplier":
                sede = IndirizzoType()
            else:
                raise exceptions.Warning(_("Internal error: invalid partner selector"))
        else:
            if selector == "company":
                sede = IndirizzoType()
            elif selector == "customer":
                if SPESOMETRO_VERSION == "2.0":
                    sede = IndirizzoNoCAPType()
                else:
                    sede = IndirizzoType()
            elif selector == "supplier":
                if SPESOMETRO_VERSION == "2.0":
                    sede = IndirizzoNoCAPType()
                else:
                    sede = IndirizzoType()
            else:
                raise exceptions.Warning(_("Internal error: invalid partner selector"))

        if fields.get("xml_Nazione"):
            sede.Nazione = fields["xml_Nazione"]
        else:
            raise exceptions.Warning(
                _(
                    "Unknow country of %s %s %s"
                    % (
                        fields.get("xml_Denominazione"),
                        fields.get("xml_Nome"),
                        fields.get("xml_Cognome"),
                    )
                )
            )

        if fields.get("xml_Indirizzo"):
            sede.Indirizzo = self.str60Latin(fields["xml_Indirizzo"])
        else:
            raise exceptions.Warning(
                _("Error!"),
                _(
                    "Missed address %s %s %s"
                    % (
                        fields.get("xml_Denominazione"),
                        fields.get("xml_Nome"),
                        fields.get("xml_Cognome"),
                    )
                ),
            )
        if fields.get("xml_Comune"):
            sede.Comune = self.str60Latin(fields["xml_Comune"])
        else:
            raise exceptions.Warning(
                _(
                    "Missed city %s %s %s"
                    % (
                        fields.get("xml_Denominazione"),
                        fields.get("xml_Nome"),
                        fields.get("xml_Cognome"),
                    )
                )
            )
        if fields.get("xml_CAP") and fields["xml_Nazione"] == "IT":
            sede.CAP = fields["xml_CAP"]
        elif selector == "company":
            raise exceptions.Warning(_("Missed company zip code"))
        if fields.get("xml_Provincia") and fields["xml_Nazione"] == "IT":
            sede.Provincia = fields["xml_Provincia"]
        return sede

    @api.model
    def get_name(self, fields, dte_dtr_id, selector):
        if dte_dtr_id == "DTE":
            if selector == "company":
                if SPESOMETRO_VERSION == "2.0":
                    AltriDatiIdentificativi = AltriDatiIdentificativiNoSedeType()
                else:
                    AltriDatiIdentificativi = AltriDatiIdentificativiITType()
            elif selector == "customer" or selector == "supplier":
                if SPESOMETRO_VERSION == "2.0":
                    AltriDatiIdentificativi = AltriDatiIdentificativiNoCAPType()
                else:
                    AltriDatiIdentificativi = AltriDatiIdentificativiType()
            else:
                raise exceptions.Warning(
                    _("Error!"), _("Internal error: invalid partner selector")
                )
        else:
            if selector == "company":
                if SPESOMETRO_VERSION == "2.0":
                    AltriDatiIdentificativi = AltriDatiIdentificativiNoSedeType()
                else:
                    AltriDatiIdentificativi = AltriDatiIdentificativiITType()
            elif selector == "customer" or selector == "supplier":
                if SPESOMETRO_VERSION == "2.0":
                    AltriDatiIdentificativi = AltriDatiIdentificativiNoCAPType()
                else:
                    AltriDatiIdentificativi = AltriDatiIdentificativiType()
            else:
                raise exceptions.Warning(
                    _("Error!"), _("Internal error: invalid partner selector")
                )

        if "xml_Denominazione" in fields:
            AltriDatiIdentificativi.Denominazione = self.str80Latin(
                fields["xml_Denominazione"]
            )
        else:
            AltriDatiIdentificativi.Nome = self.str60Latin(fields["xml_Nome"])
            AltriDatiIdentificativi.Cognome = self.str60Latin(fields["xml_Cognome"])
        AltriDatiIdentificativi.Sede = self.get_sede(fields, dte_dtr_id, selector)
        return AltriDatiIdentificativi

    @api.model
    def get_cedente_prestatore(self, fields, dte_dtr_id):
        if dte_dtr_id == "DTE":
            CedentePrestatore = CedentePrestatoreDTEType()
            CedentePrestatore.IdentificativiFiscali = IdentificativiFiscaliITType()
            # Company VAT number must be present
            CedentePrestatore.IdentificativiFiscali.IdFiscaleIVA = IdFiscaleITType()
            partner_type = "company"
        elif dte_dtr_id == "DTR":
            CedentePrestatore = CedentePrestatoreDTRType()
            CedentePrestatore.IdentificativiFiscali = IdentificativiFiscaliType()
            # Company VAT number must be present
            CedentePrestatore.IdentificativiFiscali.IdFiscaleIVA = IdFiscaleType()
            partner_type = "supplier"
        else:
            raise exceptions.Warning(
                _("Error!"), _("Internal error: invalid partner selector")
            )

        if fields.get("xml_IdPaese") and fields.get("xml_IdCodice"):
            CedentePrestatore.IdentificativiFiscali.IdFiscaleIVA.IdPaese = fields[
                "xml_IdPaese"
            ]
            CedentePrestatore.IdentificativiFiscali.IdFiscaleIVA.IdCodice = fields[
                "xml_IdCodice"
            ]
        if fields.get("xml_CodiceFiscale"):
            CedentePrestatore.IdentificativiFiscali.CodiceFiscale = CodiceFiscaleType(
                fields["xml_CodiceFiscale"]
            )
        CedentePrestatore.AltriDatiIdentificativi = self.get_name(
            fields, dte_dtr_id, partner_type
        )
        return CedentePrestatore

    @api.model
    def get_cessionario_committente(self, fields, dte_dtr_id):
        if dte_dtr_id == "DTE":
            partner = CessionarioCommittenteDTEType()
            partner_type = "customer"
            partner.IdentificativiFiscali = IdentificativiFiscaliNoIVAType()
        else:
            # DTR
            partner = CessionarioCommittenteDTRType()
            partner_type = "company"
            partner.IdentificativiFiscali = IdentificativiFiscaliITType()

        if fields.get("xml_IdPaese") and fields.get("xml_IdCodice"):
            if dte_dtr_id == "DTE":
                partner.IdentificativiFiscali.IdFiscaleIVA = IdFiscaleType()
            else:
                partner.IdentificativiFiscali.IdFiscaleIVA = IdFiscaleITType()

            partner.IdentificativiFiscali.IdFiscaleIVA.IdPaese = fields["xml_IdPaese"]
            partner.IdentificativiFiscali.IdFiscaleIVA.IdCodice = fields["xml_IdCodice"]

            if fields.get("xml_IdPaese") == "IT" and fields.get("xml_CodiceFiscale"):
                partner.IdentificativiFiscali.CodiceFiscale = CodiceFiscaleType(
                    fields["xml_CodiceFiscale"]
                )
        else:
            partner.IdentificativiFiscali.CodiceFiscale = CodiceFiscaleType(
                fields["xml_CodiceFiscale"]
            )
        # row 44: 2.2.2   <AltriDatiIdentificativi>
        partner.AltriDatiIdentificativi = self.get_name(
            fields, dte_dtr_id, partner_type
        )
        return partner

    @api.model
    def get_dte_dtr(self, commitment_model, commitment, dte_dtr_id):
        partners = []
        partner_ids = commitment_model.get_partner_list(commitment, dte_dtr_id)
        if not partner_ids:
            raise exceptions.Warning(_("No invoices found!"))
        for partner_id in partner_ids:
            fields_partner = commitment_model.get_xml_cessionario_cedente(
                commitment, partner_id, dte_dtr_id
            )
            _logger.debug(
                "partner_id=%d %s VAT=%s%s CF=%s"
                % (
                    partner_id,
                    fields_partner.get("xml_Denominazione"),
                    fields_partner.get("xml_IdPaese"),
                    fields_partner.get("xml_IdCodice"),
                    fields_partner.get("xml_CodiceFiscale"),
                )
            )

            if dte_dtr_id == "DTE":
                partner = self.get_cessionario_committente(fields_partner, dte_dtr_id)
            else:
                partner = self.get_cedente_prestatore(fields_partner, dte_dtr_id)

            invoices = []
            # Iterate over invoices of current partner
            invoice_ids = commitment_model.get_invoice_list(
                commitment, partner_id, dte_dtr_id
            )
            for invoice_id in invoice_ids:
                fields = commitment_model.get_xml_invoice(
                    commitment, invoice_id, dte_dtr_id
                )

                if dte_dtr_id == "DTE":
                    invoice = DatiFatturaBodyDTEType()
                    if SPESOMETRO_VERSION == "2.0":
                        invoice.DatiGenerali = DatiGeneraliType()
                    else:
                        invoice.DatiGenerali = DatiGeneraliDTEType()
                else:
                    invoice = DatiFatturaBodyDTRType()
                    invoice.DatiGenerali = DatiGeneraliDTRType()

                invoice.DatiGenerali.TipoDocumento = fields["xml_TipoDocumento"]
                invoice.DatiGenerali.Data = fields["xml_Data"]
                invoice.DatiGenerali.Numero = fields["xml_Numero"]
                if dte_dtr_id == "DTR":
                    invoice.DatiGenerali.DataRegistrazione = fields[
                        "xml_DataRegistrazione"
                    ]

                if (
                    dte_dtr_id == "DTR"
                    and fields["xml_TipoDocumento"] != "TD12"
                    and not fields_partner.get("xml_IdPaese")
                    and not fields_partner.get("xml_IdCodice")
                    and not fields_partner.get("xml_CodiceFiscale")
                ):
                    raise exceptions.Warning(
                        _(
                            "Error 00464: Partner id %d without fiscal data"
                            % (partner_id)
                        )
                    )

                dati_riepilogo = []
                line_ids = commitment_model.get_riepilogo_list(
                    commitment, invoice_id, dte_dtr_id
                )
                for line_id in line_ids:
                    fields = commitment_model.get_xml_riepilogo(
                        commitment, line_id, dte_dtr_id
                    )
                    riepilogo = DatiRiepilogoType()
                    riepilogo.ImponibileImporto = "{:.2f}".format(
                        fields["xml_ImponibileImporto"]
                    )
                    riepilogo.DatiIVA = DatiIVAType()
                    riepilogo.DatiIVA.Imposta = "{:.2f}".format(fields["xml_Imposta"])
                    riepilogo.DatiIVA.Aliquota = "{:.2f}".format(fields["xml_Aliquota"])
                    if fields.get("xml_Deducibile", None) is not None:
                        riepilogo.Deducibile = fields["xml_Deducibile"]
                    if fields.get("xml_Natura", False):
                        riepilogo.Natura = fields["xml_Natura"]
                    elif fields.get("xml_Detraibile", None) is not None:
                        riepilogo.Detraibile = "{:.2f}".format(fields["xml_Detraibile"])
                    if fields.get("xml_EsigibilitaIVA", False):
                        riepilogo.EsigibilitaIVA = fields["xml_EsigibilitaIVA"]
                    dati_riepilogo.append(riepilogo)
                invoice.DatiRiepilogo = dati_riepilogo
                invoices.append(invoice)

            if dte_dtr_id == "DTE":
                partner.DatiFatturaBodyDTE = invoices
            else:
                partner.DatiFatturaBodyDTR = invoices
            partners.append(partner)

        fields = commitment_model.get_xml_company(commitment, dte_dtr_id)
        if dte_dtr_id == "DTE":
            dte = DTEType()

            dte.CedentePrestatoreDTE = self.get_cedente_prestatore(fields, dte_dtr_id)
            dte.CessionarioCommittenteDTE = partners

            # dte.Rettifica = (RettificaType())

            return dte
        else:
            dtr = DTRType()

            dtr.CessionarioCommittenteDTR = self.get_cessionario_committente(
                fields, dte_dtr_id
            )

            dtr.CedentePrestatoreDTR = partners

            # dtr.Rettifica = (RettificaType())

            return dtr

    @api.multi
    def export_vat_communication_DTE(self):
        return self.with_context(dte_dtr_id="DTE").export_vat_communication()

    @api.multi
    def export_vat_communication_DTR(self):
        return self.with_context(dte_dtr_id="DTR").export_vat_communication()

    @api.multi
    def export_vat_communication(self):
        context = self.env.context
        dte_dtr_id = context.get("dte_dtr_id", "DTE")
        commitment_model = self.env["account.vat.communication"]
        commitment_ids = context.get("active_ids", False)
        if commitment_ids:
            for commitment in commitment_model.browse(commitment_ids):

                communication = DatiFattura()
                communication.versione = VersioneType(VERSIONE)
                communication.DatiFatturaHeader = self.get_dati_fattura_header(
                    commitment_model, commitment, dte_dtr_id
                )

                if dte_dtr_id == "DTE":
                    communication.DTE = self.get_dte_dtr(
                        commitment_model, commitment, dte_dtr_id
                    )
                elif dte_dtr_id == "DTR":
                    communication.DTR = self.get_dte_dtr(
                        commitment_model, commitment, dte_dtr_id
                    )
                else:
                    raise exceptions.Warning(
                        _("Internal error: invalid partner selector")
                    )
                progr_invio = commitment_model.set_progressivo_telematico(commitment)
                _logger.debug("Progressivo invio %d" % progr_invio)
                file_name = "IT%s_DF_%05d.xml" % (
                    commitment.soggetto_codice_fiscale,
                    progr_invio,
                )
                try:
                    vat_communication_xml = communication.toDOM().toprettyxml()
                except Exception as e:
                    _logger.error(e.details())
                    raise

                out = base64.b64encode(vat_communication_xml.encode("ascii"))

                attach_vals = {
                    "name": file_name,
                    "datas_fname": file_name,
                    "datas": out,
                    "res_model": "account.vat.communication",
                    "res_id": commitment.id,
                    "type": "binary",
                }

                self.env["ir.attachment"].create(attach_vals)

                return self.write(
                    {
                        "state": "get",
                        "data": out,
                        "name": file_name,
                        "target": dte_dtr_id,
                    }
                )
