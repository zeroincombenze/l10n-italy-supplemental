# -*- coding: utf-8 -*-
#
# Copyright 2014    - Davide Corio
# Copyright 2015-16 - Lorenzo Battistini - Agile Business Group
# Copyright 2018 Simone Rubino - Agile Business Group
# Copyright 2018 Sergio Corato
# Copyright 2019 Alex Comba - Agile Business Group
# Copyright 2018-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
import base64
import itertools
import logging
import re

from python_plus import _u

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export
from odoo.tools.float_utils import float_round

from odoo.addons.l10n_it_ade.bindings import fatturapa_v_1_2
from odoo.addons.l10n_it_ade.bindings.fatturapa_v_1_2 import (
    AllegatiType,
    AltriDatiGestionaliType,
    AnagraficaType,
    CedentePrestatoreType,
    CessionarioCommittenteType,
    CodiceArticoloType,
    ContattiTrasmittenteType,
    ContattiType,
    DatiAnagraficiCedenteType,
    DatiAnagraficiCessionarioType,
    DatiAnagraficiRappresentanteType,
    DatiAnagraficiTerzoIntermediarioType,
    DatiBeniServiziType,
    DatiDocumentiCorrelatiType,
    DatiGeneraliDocumentoType,
    DatiGeneraliType,
    DatiPagamentoType,
    DatiRiepilogoType,
    DatiTrasmissioneType,
    DettaglioLineeType,
    DettaglioPagamentoType,
    FatturaElettronica,
    FatturaElettronicaBodyType,
    FatturaElettronicaHeaderType,
    IdFiscaleType,
    IndirizzoType,
    IscrizioneREAType,
    RappresentanteFiscaleCessionarioType,
    RappresentanteFiscaleType,
    ScontoMaggiorazioneType,
    TerzoIntermediarioSoggettoEmittenteType,
)
from odoo.addons.l10n_it_einvoice_base.models.account_invoice import (
    RELATED_DOCUMENT_TYPES,
)

_logger = logging.getLogger(__name__)

try:
    from pyxb.exceptions_ import SimpleFacetValueError, SimpleTypeValueError
    from unidecode import unidecode
except ImportError as err:                                           # pragma: no cover
    _logger.debug(err)

CODE_NONE_IT = "0000000"
CODE_NONE_EU = "XXXXXXX"
PAYTYPE_BNK_CUSTOMER = ("MP11", "MP12", "MP16", "MP17", "MP19", "MP20", "MP21")
PAYTYPE_BNK_COMPANY = ("MP05", "MP07", "MP08", "MP13", "MP18")
IBAN_PATTERN = re.compile("[A-Z]{2}[0-9]{2}[A-Z][0-9A-Z]+")
INHERITED_FLDS = [
    "city",
    "codice_destinatario",
    "country_id",
    "email",
    "fiscalcode",
    "ipa_code",
    "is_pa",
    "name",
    "pec_destinatario",
    "phone",
    "street",
    "vat",
    "zip",
]


class WizardExportFatturapa(models.TransientModel):
    _name = "wizard.export.fatturapa"
    _description = "Export E-invoice"

    @api.model
    def _domain_ir_values(self):
        """Get all print actions for current model"""
        return [
            ("model", "=", self.env.context.get("active_model", False)),
            ("key2", "=", "client_print_multi"),
        ]

    report_print_menu = fields.Many2one(
        comodel_name="ir.values",
        domain=_domain_ir_values,
        help="This report will be automatically included in the created XML",
    )

    def saveAttachment(self, fatturapa, number):
        attach_model = self.env["fatturapa.attachment.out"]
        if "company_id" in self.env.context:
            company_model = self.env["res.company"]
            company = company_model.browse(self.env.context["company_id"])
        else:
            company = self.env.user.company_id
        if not company.vat:                                          # pragma: no cover
            raise UserError(_("Company %s TIN not set.") % company.name)
        if (
            company.fatturapa_sender_partner
            and not company.fatturapa_sender_partner.vat
        ):                                                           # pragma: no cover
            raise UserError(
                _("Partner %s TIN not set.") % company.fatturapa_sender_partner.name
            )
        vat = company.vat
        if company.fatturapa_sender_partner:
            vat = company.fatturapa_sender_partner.vat
        vat = self.env["res.partner"].wep_vat(vat)
        attach_vals = {
            "name": "%s_%s.xml" % (vat, number),
            "datas_fname": "%s_%s.xml" % (vat, number),
            "datas": base64.encodestring(fatturapa.toxml("UTF-8")),
        }
        return attach_model.create(attach_vals)

    def setProgressivoInvio(self, fatturapa, attach=False):
        # if the attachment is given than we will reuse its file_id
        if attach:
            # Xml file name uses the format VAT_XXXXX.xml and we are interested
            # to get XXXXX
            file_id = attach.name.split("_")[1].split(".")[0]
        else:
            if "company_id" in self.env.context:
                company_model = self.env["res.company"]
                company = company_model.browse(self.env.context["company_id"])
            else:
                company = self.env.user.company_id
            fatturapa_sequence = company.fatturapa_sequence_id
            if not fatturapa_sequence:                               # pragma: no cover
                raise UserError(_("E-invoice sequence not configured."))
            file_id = fatturapa_sequence.next_by_id()
        try:                                                         # pragma: no cover
            fatturapa.FatturaElettronicaHeader.DatiTrasmissione.ProgressivoInvio = (
                file_id
            )
        except (SimpleFacetValueError, SimpleTypeValueError) as e:   # pragma: no cover
            msg = _(
                "FatturaElettronicaHeader.DatiTrasmissione." "ProgressivoInvio:\n%s"
            ) % _u(e)
            raise UserError(msg)
        return file_id

    def _wep_phone_number(self, phone):
        """ "Remove trailing +39 and all no numeric chars"""
        wep_phone = ""
        if phone:
            if phone[0:3] == "+39":
                phone = phone[3:]
            elif phone[0] == "+":
                phone = "00" + phone[1:]
            for i in range(len(phone)):
                if phone[i].isdigit():
                    wep_phone += phone[i]
        return wep_phone.strip()

    def _get_partner_field(self, partner, field, mode=None):
        """Select field from <invoice address> or <parent>
        Order refers to a <customer> and an <invoice address>.
        <invoice address> should be child of <customer>, when they differ.
        Invoice get <invoice address> from order so here we have:
        - partner is <invoice address> of order (child of <customer>)
        - parent is <customers>  of order (parent of <invoice address>)

        <invoice address> may not have some data, i.e. vat number while
        <parent> contains all customer information.

        Usually, the behavior of this funciotn is fallback:
        return value from <invoice address> field, if present,
        otherwise return <parent> field with the same name.

        When mode in <type_inv_addr> field of <invoice address> is
        'FR' (Fiscal Representative) or 'SO' (Stable Organization),
        some fields are not inherited from <parent>
        """
        mode = mode or "fallback"
        inherit = True if field in INHERITED_FLDS or mode == "fallback" else False
        value = False
        parent = partner.commercial_partner_id
        if field == "company_type":
            if partner.name:
                value = partner[field] or parent[field]
            else:
                value = (parent != partner and parent[field]) or "company"
        elif mode == "parent":
            value = (parent != partner and field in parent and parent[field]) or False
        elif field in partner:
            if inherit:
                value = partner[field] or parent[field]
            else:
                value = partner[field]
        if field in ("name", "street", "city"):
            return partner.wep_text(value)
        return value

    def _setIdTrasmittente(self, company_partner, fatturapa):
        if not company_partner.country_id:
            raise UserError(_("Company %s, Country not set.")
                            % company_partner.display_name)
        IdPaese = company_partner.country_id.code
        IdCodice = company_partner.fiscalcode if hasattr(company_partner,
                                                         "fiscalcode") else False
        if not IdCodice:
            if company_partner.vat:
                IdCodice = company_partner.vat[2:]
        if not IdCodice:                                             # pragma: no cover
            raise UserError(
                _("Company %s does not have fiscal code or VAT number.")
                % company_partner.display_name
            )

        fatturapa.FatturaElettronicaHeader.DatiTrasmissione.IdTrasmittente = (
            IdFiscaleType(IdPaese=IdPaese, IdCodice=IdCodice)
        )

        return True

    def _getFormatoTrasmissione(self, partner):
        if partner.commercial_partner_id.is_pa:
            formato = "FPA12"
        else:
            formato = "FPR12"
        return formato

    def _setFormatoTrasmissione(self, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione.FormatoTrasmissione = (
            self._getFormatoTrasmissione(partner)
        )
        return True

    def _setCodiceDestinatario(self, company_partner, fatturapa):
        pec_destinatario = None
        if company_partner.commercial_partner_id.is_pa:
            code = self._get_partner_field(company_partner, "ipa_code")
            if not code:
                raise UserError(
                    _("Partner %s is PA but does not have IPA code.")
                    % company_partner.name
                )
        else:
            code = self._get_partner_field(company_partner, "codice_destinatario")
            if not code:
                raise UserError(
                    _("Partner %s is not PA but does not have Addressee Code.")
                    % company_partner.name
                )
            if code == CODE_NONE_IT:
                pec_destinatario = self._get_partner_field(company_partner,
                                                           "pec_destinatario")
            vat = self._get_partner_field(company_partner, "vat")
            fiscalcode = company_partner.wep_fiscalcode(
                self._get_partner_field(company_partner, "fiscalcode")
            )
            if (
                code not in (CODE_NONE_IT, CODE_NONE_EU)
                and not vat and not fiscalcode
            ):                                                       # pragma: no cover
                raise UserError(
                    _(
                        "Partner %s is not PA "
                        "but does not have vat number neither fiscal code Code."
                    )
                    % company_partner.name
                )
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione.CodiceDestinatario = (
            code.upper()
        )
        if pec_destinatario:
            fatturapa.FatturaElettronicaHeader.DatiTrasmissione.PECDestinatario = (
                pec_destinatario
            )

        return True

    def _setContattiTrasmittente(self, company, fatturapa):
        if not company.phone:                                        # pragma: no cover
            raise UserError(_("Company Telephone number not set."))
        Telefono = self._wep_phone_number(company.phone)
        if not company.email:                                         # pragma: no cover
            raise UserError(_("Company Email not set."))
        Email = company.email
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione.ContattiTrasmittente = (
            ContattiTrasmittenteType(Telefono=Telefono, Email=Email)
        )

        return True

    def setDatiTrasmissione(self, company, partner, fatturapa, self_invoice=False):
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione = DatiTrasmissioneType()
        self._setIdTrasmittente(company.partner_id, fatturapa)
        self._setFormatoTrasmissione(partner, fatturapa)
        self._setCodiceDestinatario(company.partner_id if self_invoice else partner,
                                    fatturapa)
        if not self_invoice:
            self._setContattiTrasmittente(company, fatturapa)

    def _setDatiAnagraficiCedente(
            self, CedentePrestatore, company, partner=None, invoices=False):
        if not company.vat:  # pragma: no cover
            raise UserError(_("Company TIN not set."))

        CedentePrestatore.DatiAnagrafici = DatiAnagraficiCedenteType()
        fatturapa_fiscalpos = company.fatturapa_fiscal_position_id
        if not fatturapa_fiscalpos:                                  # pragma: no cover
            raise UserError(_("E-invoice fiscal position not set."))

        self_invoice = invoices[0].is_self_invoice if invoices else False
        if self_invoice:
            # Se vale IT , il sistema verifica che il TipoDocumento sia diverso da
            # TD17, TD18 e TD19; in caso contrario il file viene scartato
            if partner.vat:
                IdPaese = partner.vat[0:2]
                IdCodice = partner.vat[2:]
                if any([
                    x for x in invoices
                    if x.fiscal_document_type_id.code in ('TD17', 'TD18', 'TD19')
                ]):
                    if IdPaese == 'IT':
                        IdPaese = partner.country_id.code
                    if IdPaese == 'IT':
                        IdPaese = "EU"
                        IdCodice = partner.vat
                if (IdPaese != 'EU' and
                        IdPaese not in self.env['res.country'].search(
                            []).mapped('code')):
                    raise ValueError(_(
                        "Country code does not exist or it is not mapped in countries: "
                        "%s" % partner.vat[0:2]
                    ))
                CedentePrestatore.DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                    IdPaese=IdPaese, IdCodice=IdCodice)
            elif partner.country_id.code and partner.country_id.code != 'IT':
                CedentePrestatore.DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                    IdPaese=partner.country_id.code, IdCodice='99999999999')
            else:
                raise UserError(
                    _("Impossible to set IdFiscaleIVA for %s") % partner.display_name)
            CedentePrestatore.DatiAnagrafici.Anagrafica = AnagraficaType(
                Denominazione=partner.wep_text(partner.name)
            )
            CedentePrestatore.DatiAnagrafici.RegimeFiscale = "RF18"
        else:
            CedentePrestatore.DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                IdPaese=company.country_id.code, IdCodice=company.vat[2:]
            )
            CedentePrestatore.DatiAnagrafici.Anagrafica = AnagraficaType(
                Denominazione=company.name
            )
            if company.partner_id.fiscalcode:
                CedentePrestatore.DatiAnagrafici.CodiceFiscale = (
                    company.partner_id.fiscalcode
                )
            CedentePrestatore.DatiAnagrafici.RegimeFiscale = fatturapa_fiscalpos.code
        return True

    def _setAlboProfessionaleCedente(self, CedentePrestatore, company):
        # TODO Albo professionale, for now the main company is considered
        # to be a legal entity and not a single person
        # 1.2.1.4   <AlboProfessionale>
        # 1.2.1.5   <ProvinciaAlbo>
        # 1.2.1.6   <NumeroIscrizioneAlbo>
        # 1.2.1.7   <DataIscrizioneAlbo>
        return True

    def _setSedeCedente(self, CedentePrestatore, company, partner=None):
        partner = partner or company.partner_id
        for (item, name) in (
            ("country_id", "nazione"),
            ("street", "indirizzo"),
            ("city", "città"),
        ):
            if not getattr(partner, item):                           # pragma: no cover
                raise UserError(_("Your company %s is not set.") % name)

        for (item, name) in (
            ("zip", "CAP"),
            ("state_id", "provincia"),
            ("fatturapa_rea_office", "ufficio REA"),
            ("fatturapa_rea_number", "numero REA"),
            ("fatturapa_rea_partner", "unipersonale?"),
        ):
            if not getattr(company, item):                           # pragma: no cover
                raise UserError(_("Your company %s is not set.") % name)

        if partner.codice_destinatario != 'XXXXXXX':
            if not partner.zip:
                raise UserError(_("Your company %s is not set.") % "zip")
            if not partner.state_id:
                raise UserError(_("Your company %s is not set.") % "state_id")
            CedentePrestatore.Sede = IndirizzoType(
                Indirizzo=encode_for_export(partner.street, 60),
                CAP=partner.zip,
                Comune=encode_for_export(partner.city, 60),
                Provincia=partner.state_id.code,
                Nazione=partner.country_id.code,
            )
        else:
            CedentePrestatore.Sede = (
                IndirizzoType(
                    Indirizzo=encode_for_export(partner.street, 60),
                    CAP='00000',
                    Comune=encode_for_export(partner.city, 60),
                    Provincia='EE',
                    Nazione=partner.country_id.code))
        return True

    def _setStabileOrganizzazione(self, CedentePrestatore, company):
        if company.fatturapa_stabile_organizzazione:
            stabile_organizzazione = company.fatturapa_stabile_organizzazione
            if not stabile_organizzazione.street:                    # pragma: no cover
                raise UserError(
                    _("Street is not set for %s.") % stabile_organizzazione.name
                )
            if not stabile_organizzazione.zip:                       # pragma: no cover
                raise UserError(
                    _("ZIP is not set for %s.") % stabile_organizzazione.name
                )
            if not stabile_organizzazione.city:                      # pragma: no cover
                raise UserError(
                    _("City is not set for %s.") % stabile_organizzazione.name
                )
            if not stabile_organizzazione.country_id:                # pragma: no cover
                raise UserError(
                    _("Country is not set for %s.") % stabile_organizzazione.name
                )
            CedentePrestatore.StabileOrganizzazione = IndirizzoType(
                Indirizzo=stabile_organizzazione.street,
                CAP=stabile_organizzazione.zip,
                Comune=stabile_organizzazione.city,
                Nazione=stabile_organizzazione.country_id.code,
            )
            if stabile_organizzazione.state_id:
                CedentePrestatore.StabileOrganizzazione.Provincia = (
                    stabile_organizzazione.state_id.code
                )
        return True

    def _setRea(self, CedentePrestatore, company):

        if company.fatturapa_rea_office and company.fatturapa_rea_number:
            CedentePrestatore.IscrizioneREA = IscrizioneREAType(
                Ufficio=(
                    company.fatturapa_rea_office
                    and company.fatturapa_rea_office.code
                    or None
                ),
                NumeroREA=company.fatturapa_rea_number or None,
                CapitaleSociale=(
                    company.fatturapa_rea_capital
                    and "%.2f" % company.fatturapa_rea_capital
                    or None
                ),
                SocioUnico=(company.fatturapa_rea_partner or None),
                StatoLiquidazione=company.fatturapa_rea_liquidation or "LN",
            )

    def _setContatti(self, CedentePrestatore, company):
        CedentePrestatore.Contatti = ContattiType(
            Telefono=self._wep_phone_number(company.partner_id.phone) or None,
            Fax=self._wep_phone_number(company.partner_id.fax) or None,
            Email=company.partner_id.email or None,
        )

    def _setPubAdministrationRef(self, CedentePrestatore, company, partner):
        pa_partner_code = self._get_partner_field(partner, "pa_partner_code")
        if pa_partner_code:
            CedentePrestatore.RiferimentoAmministrazione = pa_partner_code
        elif company.fatturapa_pub_administration_ref:
            CedentePrestatore.RiferimentoAmministrazione = (
                company.fatturapa_pub_administration_ref
            )

    def setCedentePrestatore(self, company, fatturapa, partner, invoices=None):
        self_invoice = invoices[0].is_self_invoice if invoices else False
        fatturapa.FatturaElettronicaHeader.CedentePrestatore = CedentePrestatoreType()
        self._setDatiAnagraficiCedente(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company,
            partner=partner,
            invoices=invoices,
        )
        self._setSedeCedente(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company,
            partner=partner if self_invoice else None
        )
        self._setAlboProfessionaleCedente(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore, company
        )
        self._setStabileOrganizzazione(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore, company
        )
        # TODO: add Contacts
        self._setRea(fatturapa.FatturaElettronicaHeader.CedentePrestatore, company)
        self._setContatti(fatturapa.FatturaElettronicaHeader.CedentePrestatore, company)
        self._setPubAdministrationRef(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company,
            partner,
        )

    def _setDatiAnagraficiCessionario(self, partner, fatturapa):
        mode = partner.type_inv_addr
        mode = mode if mode not in ("SO", "FR") else "parent"
        fatturapa.FatturaElettronicaHeader.CessionarioCommittente.DatiAnagrafici = (
            DatiAnagraficiCessionarioType()
        )
        vat = self._get_partner_field(partner, "vat", mode=mode)
        # is_pa = self._get_partner_field(partner, "is_pa", mode=mode)
        fiscalcode = partner.wep_fiscalcode(
            self._get_partner_field(partner, "fiscalcode", mode=mode)
        )
        codice_destinatario = self._get_partner_field(
            partner, "codice_destinatario", mode=mode
        )
        if (
            not vat
            and codice_destinatario == CODE_NONE_EU
            and partner.country_id.code
            and partner.country_id.code != "IT"
        ):
            # SDI accepts missing VAT# for foreign customers by setting a
            # fake IdCodice and a valid IdPaese
            # Otherwise raise error if we have no VAT# and no Fiscal code
            vat = "%s99999999999" % partner.country_id.code
        elif vat and vat[0:3] in ("IT9", "IT8"):
            if not fiscalcode:
                fiscalcode = vat[2:]
                vat = ""
            elif fiscalcode == vat[2:]:
                vat = ""

        FatturaCessionarioCommittente = (
            fatturapa.FatturaElettronicaHeader.CessionarioCommittente
        )
        if fiscalcode:
            (FatturaCessionarioCommittente.DatiAnagrafici.CodiceFiscale) = fiscalcode
        if vat:
            country_code, vat_number = partner.split_vat_n_country(vat)
            if country_code and vat_number:
                (
                    FatturaCessionarioCommittente.DatiAnagrafici.IdFiscaleIVA
                ) = IdFiscaleType(IdPaese=country_code, IdCodice=vat_number)

        company_type = self._get_partner_field(partner, "company_type", mode=mode)
        if company_type == "company":
            (FatturaCessionarioCommittente.DatiAnagrafici.Anagrafica) = AnagraficaType(
                Denominazione=self._get_partner_field(partner, "name", mode=mode)
            )
        elif company_type == "person":
            if not partner.lastname or not partner.firstname:
                raise UserError(
                    _("Partner %s must have name and surname.") % partner.name
                )
            FatturaCessionarioCommittente.DatiAnagrafici.Anagrafica = AnagraficaType(
                Cognome=partner.lastname, Nome=partner.firstname
            )

        eori_code = self._get_partner_field(partner, "eori_code", mode=mode)
        if eori_code:
            FatturaCessionarioCommittente.DatiAnagrafici.Anagrafica.CodEORI = eori_code

        return True

    def _setDatiAnagraficiRappresentanteFiscale(self, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader.RappresentanteFiscale = (
            RappresentanteFiscaleType()
        )
        fatturapa.FatturaElettronicaHeader.RappresentanteFiscale.DatiAnagrafici = (
            DatiAnagraficiRappresentanteType()
        )
        if not partner.vat and not partner.fiscalcode:
            raise UserError(
                _("VAT number and fiscal code are not set for %s.") % partner.name
            )
        FatturaRappresentanteFiscale = (
            fatturapa.FatturaElettronicaHeader.RappresentanteFiscale
        )
        if partner.fiscalcode:
            FatturaRappresentanteFiscale.DatiAnagrafici.CodiceFiscale = (
                partner.fiscalcode
            )
        if partner.vat:
            FatturaRappresentanteFiscale.DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                IdPaese=partner.vat[0:2], IdCodice=partner.vat[2:]
            )
        FatturaRappresentanteFiscale.DatiAnagrafici.Anagrafica = AnagraficaType(
            Denominazione=partner.name
        )
        if partner.eori_code:
            FatturaRappresentanteFiscale.DatiAnagrafici.Anagrafica.CodEORI = (
                partner.eori_code
            )

        return True

    def _setTerzoIntermediarioOSoggettoEmittente(self, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader.TerzoIntermediarioOSoggettoEmittente = (
            TerzoIntermediarioSoggettoEmittenteType()
        )
        FatturaTerzoIntermediario = (
            fatturapa.FatturaElettronicaHeader.TerzoIntermediarioOSoggettoEmittente
        )
        FatturaTerzoIntermediario.DatiAnagrafici = (
            DatiAnagraficiTerzoIntermediarioType()
        )
        if not partner.vat and not partner.fiscalcode:
            raise UserError(_("Partner VAT number and fiscal code are not set."))
        if partner.fiscalcode:
            FatturaTerzoIntermediario.DatiAnagrafici.CodiceFiscale = partner.fiscalcode
        if partner.vat:
            FatturaTerzoIntermediario.DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                IdPaese=partner.vat[0:2], IdCodice=partner.vat[2:]
            )
        FatturaTerzoIntermediario.DatiAnagrafici.Anagrafica = AnagraficaType(
            Denominazione=partner.name
        )
        if partner.eori_code:
            FatturaTerzoIntermediario.DatiAnagrafici.Anagrafica.CodEORI = (
                partner.eori_code
            )
        fatturapa.FatturaElettronicaHeader.SoggettoEmittente = "TZ"
        return True

    def _setSedeCessionario(self, partner, fatturapa):
        mode = partner.type_inv_addr
        mode = mode if mode not in ("SO", "FR") else "parent"
        country_id = self._get_partner_field(partner, "country_id", mode=mode)
        if not country_id:
            raise UserError(_("Customer country is not set."))
        street = self._get_partner_field(partner, "street", mode=mode)
        zip = self._get_partner_field(partner, "zip", mode=mode)
        city = self._get_partner_field(partner, "city", mode=mode)
        state_id = self._get_partner_field(partner, "state_id", mode=mode)
        if not street:
            raise UserError(_("Customer street is not set."))
        if mode == "parent":
            codice_destinatario = CODE_NONE_EU
        else:
            codice_destinatario = self._get_partner_field(
                partner, "codice_destinatario", mode=mode
            )
        if codice_destinatario != CODE_NONE_EU and not zip:
            raise UserError(_("Customer ZIP is not set."))
        if not city:
            raise UserError(_("Customer city is not set."))
        if codice_destinatario != CODE_NONE_EU and not state_id:
            raise UserError(_("Customer province is not set."))

        if codice_destinatario != CODE_NONE_EU:
            zip = zip
        else:
            zip = "00000"
        if codice_destinatario != CODE_NONE_EU:
            province = state_id.code
        else:
            province = "EE"
        # TODO: manage address number in <NumeroCivico>
        fatturapa.FatturaElettronicaHeader.CessionarioCommittente.Sede = IndirizzoType(
            Indirizzo=encode_for_export(street, 60),
            CAP=zip,
            Comune=encode_for_export(city, 60),
            Provincia=province,
            Nazione=country_id.code,
        )
        return True

    def _setCessionarioStabileOrganizzazione(self, partner, parent, fatturapa):
        mode = "SO"
        country_id = self._get_partner_field(partner, "country_id", mode=mode)
        if not country_id:
            raise UserError(_("Customer Stabile Organization country is not set."))
        country_code = country_id.code
        street = self._get_partner_field(partner, "street", mode=mode)
        zip = self._get_partner_field(partner, "zip", mode=mode)
        city = self._get_partner_field(partner, "city", mode=mode)
        state_id = self._get_partner_field(partner, "state_id", mode=mode)
        if not street:
            raise UserError(_("Customer Stabile Organization street is not set."))
        if not zip:
            raise UserError(_("Customer Stabile Organization ZIP is not set."))
        if not city:
            raise UserError(_("Customer Stabile Organization city is not set."))
        if not state_id:
            raise UserError(_("Customer Stabile Organization province is not set."))

        zip = zip
        province = state_id.code
        Fattura = fatturapa.FatturaElettronicaHeader
        Fattura.CessionarioCommittente.StabileOrganizzazione = IndirizzoType(
            Indirizzo=street,
            CAP=zip,
            Comune=city,
            Provincia=province,
            Nazione=country_code,
        )
        return True

    def _setCessionarioRappresentanteFiscale(self, partner, parent, fatturapa):
        mode = "FR"
        company_type = self._get_partner_field(partner, "company_type", mode=mode)
        if company_type == "company":
            name = self._get_partner_field(partner, "name", mode=mode)
            if not name:
                raise UserError(_("Customer Fiscal Representative name is not set."))
        elif company_type == "person":
            lastname = self._get_partner_field(partner, "lastname", mode=mode)
            firstname = self._get_partner_field(partner, "firstname", mode=mode)
            if not lastname or not firstname:
                raise UserError(
                    _("Customer Stabile Organization must have " "name and surname.")
                )
        country_id = self._get_partner_field(partner, "country_id", mode=mode)
        if not country_id:
            raise UserError(_("Customer Stabile Organization country is not set."))
        vat = self._get_partner_field(partner, "vat", mode=mode)
        # fiscalcode = self._get_partner_field(partner, "fiscalcode", mode=mode)
        if not vat:
            raise UserError(_("Customer Stabile Organization vat is not set."))
        country_code, vat_number = self._split_vat_n_country(vat)
        if country_code != country_id.code:
            raise UserError(
                _(
                    "Customer Stabile Organization vat country"
                    " is different from from address country."
                )
            )
        FatturaCommitente = fatturapa.FatturaElettronicaHeader.CessionarioCommittente
        FatturaCommitente.RappresentanteFiscale = RappresentanteFiscaleCessionarioType()
        if company_type == "company":
            FatturaCommitente.RappresentanteFiscale.Denominazione = name
        else:
            FatturaCommitente.RappresentanteFiscale(
                Nome=firstname,
                Cognome=lastname,
            )
        if partner.vat:
            FatturaCommitente.RappresentanteFiscale.IdFiscaleIVA = IdFiscaleType(
                IdPaese=country_code, IdCodice=vat_number
            )
        return True

    def setRappresentanteFiscale(self, company, fatturapa):
        if company.fatturapa_tax_representative:
            self._setDatiAnagraficiRappresentanteFiscale(
                company.fatturapa_tax_representative, fatturapa
            )
        return True

    def setCessionarioCommittente(
            self, partner, fatturapa, invoices=None, company=None):
        fatturapa.FatturaElettronicaHeader.CessionarioCommittente = (
            CessionarioCommittenteType()
        )
        self_invoice = invoices[0].is_self_invoice if invoices else False

        if self_invoice:
            self._setDatiAnagraficiCessionario(company.partner_id, fatturapa)
            self._setSedeCessionario(company.partner_id, fatturapa)
            if invoices[0].sender == "CC":
                fatturapa.FatturaElettronicaHeader.SoggettoEmittente = "CC"
        else:
            self._setDatiAnagraficiCessionario(partner, fatturapa)
            self._setSedeCessionario(partner, fatturapa)
            mode = partner.type_inv_addr
            if mode == "SO":
                self._setCessionarioStabileOrganizzazione(partner, fatturapa)
            elif mode == "FR":
                self._setCessionarioRappresentanteFiscale(partner, fatturapa)

    def setTerzoIntermediarioOSoggettoEmittente(self, company, fatturapa):
        if company.fatturapa_sender_partner:
            self._setTerzoIntermediarioOSoggettoEmittente(
                company.fatturapa_sender_partner, fatturapa
            )
        return True

    def setTipoDocumento(self, invoice):
        if invoice.fiscal_document_type_id:
            TipoDocumento = invoice.fiscal_document_type_id.code
        elif invoice.type == "out_refund":
            TipoDocumento = "TD04"
        else:
            TipoDocumento = "TD01"
        return TipoDocumento

    def setDatiGeneraliDocumento(self, invoice, body):

        # TODO DatiSAL

        body.DatiGenerali = DatiGeneraliType()
        if not invoice.number:
            raise UserError(_("Invoice does not have a number."))

        TipoDocumento = self.setTipoDocumento(invoice)
        ImportoTotaleDocumento = invoice.amount_total
        # /!\ OCA split payment has total_amount w/o VAT e amount_sp positive
        # OIA split payment has total_amount with VTA and amount_sp negative
        # if invoice.split_payment:
        #     ImportoTotaleDocumento += invoice.amount_sp
        body.DatiGenerali.DatiGeneraliDocumento = DatiGeneraliDocumentoType(
            TipoDocumento=TipoDocumento,
            Divisa=invoice.currency_id.name,
            Data=invoice.date_invoice,
            Numero=invoice.number,
            ImportoTotaleDocumento="%.2f" % float_round(ImportoTotaleDocumento, 2),
        )

        if invoice.comment:
            # max length of Causale is 200
            caus_list = invoice.comment.split("\n")
            for causale in caus_list:
                causale = causale.strip()
                if not causale:
                    continue
                causale_list_200 = [
                    causale[i: i + 200] for i in range(0, len(causale), 200)
                ]
                for causale200 in causale_list_200:
                    # Remove non latin chars, but go back to unicode string,
                    # as expected by String200LatinType
                    causale = encode_for_export(causale200, 200)
                    body.DatiGenerali.DatiGeneraliDocumento.Causale.append(causale)

        if invoice.company_id.fatturapa_art73:
            body.DatiGenerali.DatiGeneraliDocumento.Art73 = "SI"

        return True

    def setRelatedDocumentTypes(self, invoice, body):
        for line in invoice.invoice_line_ids:
            for related_document in line.related_documents:
                doc_type = RELATED_DOCUMENT_TYPES[related_document.type]
                documento = DatiDocumentiCorrelatiType()
                if related_document.name:
                    documento.IdDocumento = related_document.name
                if related_document.lineRef:
                    documento.RiferimentoNumeroLinea.append(line.ftpa_line_number)
                if related_document.date:
                    documento.Data = related_document.date
                if related_document.numitem:
                    documento.NumItem = related_document.numitem
                if related_document.code:
                    documento.CodiceCommessaConvenzione = related_document.code
                if related_document.cup:
                    documento.CodiceCUP = related_document.cup
                if related_document.cig:
                    documento.CodiceCIG = related_document.cig
                getattr(body.DatiGenerali, doc_type).append(documento)
        for related_document in invoice.related_documents:
            doc_type = RELATED_DOCUMENT_TYPES[related_document.type]
            documento = DatiDocumentiCorrelatiType()
            if related_document.name:
                documento.IdDocumento = related_document.name
            if related_document.date:
                documento.Data = related_document.date
            if related_document.numitem:
                documento.NumItem = related_document.numitem
            if related_document.code:
                documento.CodiceCommessaConvenzione = related_document.code
            if related_document.cup:
                documento.CodiceCUP = related_document.cup
            if related_document.cig:
                documento.CodiceCIG = related_document.cig
            getattr(body.DatiGenerali, doc_type).append(documento)
        return True

    def setDatiTrasporto(self, invoice, body):
        return True

    def setDatiDDT(self, invoice, body):
        return True

    def setDatiRitenuta(self, invoice, body):
        return True

    def setDatiBollo(self, invoice, body):
        return True

    def setDatiCassaPrevidenziale(self, invoice, body):
        return True

    def _get_prezzo_unitario(self, line):
        res = line.price_unit
        if line.invoice_line_tax_ids and line.invoice_line_tax_ids[0].price_include:
            res = line.price_unit / (1 + (line.invoice_line_tax_ids[0].amount / 100))
        return res

    def setDettaglioLinee(self, invoice, body):

        body.DatiBeniServizi = DatiBeniServiziType()
        # TipoCessionePrestazione not handled

        line_no = 1
        price_precision = max(
            2, self.env["decimal.precision"].precision_get("Product Price")
        )
        uom_precision = max(
            2, self.env["decimal.precision"].precision_get("Product Unit of Measure")
        )
        for line in invoice.invoice_line_ids:
            self.setDettaglioLinea(line_no, line, body, price_precision, uom_precision)
            line_no += 1

    def setDettaglioLinea(self, line_no, line, body, price_precision, uom_precision):
        if not line.invoice_line_tax_ids:
            raise UserError(_("Invoice line %s does not have tax.") % line.name)
        if len(line.invoice_line_tax_ids) > 1:
            raise UserError(_("Too many taxes for invoice line %s.") % line.name)
        aliquota = line.invoice_line_tax_ids[0].amount
        AliquotaIVA = "%.2f" % float_round(aliquota, 2)
        line.ftpa_line_number = line_no
        prezzo_unitario = self._get_prezzo_unitario(line)
        DettaglioLinea = DettaglioLineeType(
            NumeroLinea=str(line_no),
            Descrizione=encode_for_export(line.name, 1000),
            PrezzoUnitario=("%." + str(price_precision) + "f") % prezzo_unitario,
            UnitaMisura=line.uom_id and (unidecode(line.uom_id.name)) or None,
            PrezzoTotale="%.2f" % float_round(line.price_subtotal, 2),
            AliquotaIVA=AliquotaIVA,
        )
        if line.quantity:
            DettaglioLinea.Quantita = ("%." + str(uom_precision) + "f") % line.quantity
        DettaglioLinea.ScontoMaggiorazione.extend(self.setScontoMaggiorazione(line))
        if aliquota == 0.0:
            if line.invoice_line_tax_ids:
                if not line.invoice_line_tax_ids[0].kind_id:
                    raise UserError(
                        _("No 'nature' field for tax %s.")
                        % line.invoice_line_tax_ids[0].name
                    )
                natura = line.invoice_line_tax_ids[0].kind_id.code
            else:
                natura = "N2.2"
            if natura in ("N2", "N3", "N6"):
                raise UserError(
                    _("Invalid nature code %s for %s VAT code!")
                    % (natura, line.invoice_line_tax_ids[0].description)
                )
            self.line_desc = DettaglioLinea.Natura = natura
            if line.invoice_line_tax_ids[
                0
            ].kind_id.code == "N2.1" and line.invoice_id.partner_id.country_id.code in [
                "AT",
                "BE",
                "BG",
                "CY",
                "HR",
                "DK",
                "EE",
                "FI",
                "FR",
                "DE",
                "GR",
                "IE",
                "IT",
                "LV",
                "LT",
                "LU",
                "MT",
                "NL",
                "PL",
                "PT",
                "CZ",
                "RO",
                "SK",
                "SI",
                "ES",
                "SE",
                "HU",
            ]:
                dati_gestionali = AltriDatiGestionaliType()
                dati_gestionali.TipoDato = "INVCONT"
                DettaglioLinea.AltriDatiGestionali.append(dati_gestionali)
        if line.admin_ref:
            DettaglioLinea.RiferimentoAmministrazione = line.admin_ref
        if line.product_id:
            product_code = line.product_id.default_code
            if product_code:
                CodiceArticolo = CodiceArticoloType(
                    CodiceTipo=self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("fatturapa.codicetipo.odoo", "ODOO"),
                    CodiceValore=product_code[:35],
                )
                DettaglioLinea.CodiceArticolo.append(CodiceArticolo)
            product_barcode = line.product_id.barcode
            if product_barcode:
                CodiceArticolo = CodiceArticoloType(
                    CodiceTipo="EAN",
                    CodiceValore=product_barcode[:35],
                )
                DettaglioLinea.CodiceArticolo.append(CodiceArticolo)
        body.DatiBeniServizi.DettaglioLinee.append(DettaglioLinea)
        return DettaglioLinea

    def setScontoMaggiorazione(self, line):
        res = []
        if line.discount:
            res.append(
                ScontoMaggiorazioneType(
                    Tipo="SC", Percentuale="%.2f" % float_round(line.discount, 8)
                )
            )
        return res

    def setDatiRiepilogo(self, invoice, body):
        if not invoice.tax_line_ids:
            raise UserError(
                _("Invoice {invoice} has no tax lines").format(
                    invoice=invoice.display_name
                )
            )
        found_code_line_desc = False
        for tax_line in invoice.tax_line_ids:
            tax = tax_line.tax_id
            riepilogo = DatiRiepilogoType(
                AliquotaIVA="%.2f" % float_round(tax.amount, 2),
                ImponibileImporto="%.2f" % float_round(tax_line.base, 2),
                Imposta="%.2f" % float_round(tax_line.amount, 2),
            )
            if tax.amount == 0.0:
                if not tax.kind_id:
                    raise UserError(_("No 'nature' field for tax %s") % tax.name)
                riepilogo.Natura = tax.kind_id.code
                if not tax.law_reference:
                    raise UserError(
                        _("No 'law reference' field for tax %s.") % tax.name
                    )
                riepilogo.RiferimentoNormativo = encode_for_export(
                    tax.law_reference, 100
                )
                if tax.kind_id.code == self.line_desc:
                    found_code_line_desc = True
            if hasattr(tax, "rc") and tax.rc:
                riepilogo.RiferimentoNormativo = encode_for_export(
                    tax.law_reference or tax.name, 100
                )
            elif tax.payability == "S":
                riepilogo.RiferimentoNormativo = encode_for_export(
                    tax.law_reference or tax.name, 100
                )
                riepilogo.EsigibilitaIVA = tax.payability
            elif tax.amount and tax.payability:
                riepilogo.EsigibilitaIVA = tax.payability
            # TODO

            # el.remove(el.find('SpeseAccessorie'))
            # el.remove(el.find('Arrotondamento'))

            body.DatiBeniServizi.DatiRiepilogo.append(riepilogo)
        # TODO> What is the purpose?
        if self.line_desc and not found_code_line_desc:
            riepilogo = DatiRiepilogoType(
                AliquotaIVA="%.2f" % 0.0,
                ImponibileImporto="%.2f" % 0.0,
                Imposta="%.2f" % 0.0,
                Natura=self.line_desc,
                RiferimentoNormativo="Non imponibile",
            )
            body.DatiBeniServizi.DatiRiepilogo.append(riepilogo)
        return True

    def setDatiBanca(self, DettaglioPagamento, bank_id, company=None):
        if not bank_id and company:
            for bank in company.partner_id.bank_ids:
                if bank.acc_number and IBAN_PATTERN.match(bank.acc_number):
                    bank_id = bank
                    break
        if bank_id:
            if bank_id.bank_name:
                DettaglioPagamento.IstitutoFinanziario = bank_id.bank_name
            if bank_id.acc_number:
                DettaglioPagamento.IBAN = bank_id.acc_number.replace(" ", "")
            if bank_id.bank_bic:
                DettaglioPagamento.BIC = bank_id.bank_bic
        return DettaglioPagamento

    def setDatiPagamento(self, invoice, body):
        if invoice.payment_term_id:
            payment_line_ids = invoice.get_receivable_line_ids()
            if not payment_line_ids:
                return True
            DatiPagamento = DatiPagamentoType()
            if not invoice.payment_term_id.fatturapa_pt_id:          # pragma: no cover
                raise UserError(
                    _(
                        "Payment term %s does not have a linked e-invoice "
                        "payment term."
                    )
                    % invoice.payment_term_id.name
                )
            if not invoice.payment_term_id.fatturapa_pm_id:          # pragma: no cover
                raise UserError(
                    _(
                        "Payment term %s does not have a linked e-invoice "
                        "payment method."
                    )
                    % invoice.payment_term_id.name
                )
            DatiPagamento.CondizioniPagamento = (
                invoice.payment_term_id.fatturapa_pt_id.code
            )
            move_line_pool = self.env["account.move.line"]
            TipoDocumento = self.setTipoDocumento(invoice)
            credit_amount = 0.0
            for move_line_id in payment_line_ids:
                move_line = move_line_pool.browse(move_line_id)
                # OIA split-payment management
                if TipoDocumento == "TD04":
                    if move_line.debit > 0.0:
                        credit_amount = move_line.debit
                        continue
                else:
                    if move_line.credit > 0.0:
                        credit_amount = move_line.credit
                        continue
                if TipoDocumento == "TD04":
                    ImportoPagamento = "%.2f" % (move_line.credit - credit_amount)
                else:
                    ImportoPagamento = "%.2f" % (move_line.debit - credit_amount)
                credit_amount = 0.0
                if invoice.payment_term_id.note:
                    payment_term_des = invoice.payment_term_id.note
                else:
                    payment_term_des = invoice.payment_term_id.name
                DettaglioPagamento = DettaglioPagamentoType(
                    ModalitaPagamento=(invoice.payment_term_id.fatturapa_pm_id.code),
                    DataScadenzaPagamento=move_line.date_maturity,
                    ImportoPagamento=ImportoPagamento,
                    CodicePagamento=payment_term_des,
                )
                if invoice.partner_bank_id:
                    DettaglioPagamento = self.setDatiBanca(
                        DettaglioPagamento, invoice.partner_bank_id
                    )
                elif (
                    invoice.payment_term_id.fatturapa_pm_id
                    and invoice.payment_term_id.fatturapa_pm_id.code
                    in PAYTYPE_BNK_CUSTOMER
                    and invoice.partner_id.bank_ids
                ):
                    DettaglioPagamento = self.setDatiBanca(
                        DettaglioPagamento, invoice.partner_id.bank_ids[0]
                    )
                elif (
                    invoice.payment_term_id.fatturapa_pm_id
                    and invoice.payment_term_id.fatturapa_pm_id.code
                    in PAYTYPE_BNK_COMPANY
                    and invoice.company_id.partner_id.bank_ids
                ):
                    DettaglioPagamento = self.setDatiBanca(
                        DettaglioPagamento, None, company=invoice.company_id
                    )
                DatiPagamento.DettaglioPagamento.append(DettaglioPagamento)
            body.DatiPagamento.append(DatiPagamento)
        return True

    def setAttachments(self, invoice, body):
        if invoice.fatturapa_doc_attachments:                       # pragma: no cover
            for doc_id in invoice.fatturapa_doc_attachments:
                AttachDoc = AllegatiType(
                    NomeAttachment=doc_id.datas_fname,
                    Attachment=base64.decodestring(doc_id.datas),
                )
                body.Allegati.append(AttachDoc)
        return True

    def setFatturaElettronicaHeader(
            self, company, partner, fatturapa, invoices=None):
        self_invoice = invoices[0].is_self_invoice if invoices else False
        fatturapa.FatturaElettronicaHeader = FatturaElettronicaHeaderType()
        self.setDatiTrasmissione(company, partner, fatturapa, self_invoice=self_invoice)
        self.setCedentePrestatore(company, fatturapa, partner, invoices=invoices)
        self.setRappresentanteFiscale(company, fatturapa)
        self.setCessionarioCommittente(
            partner, fatturapa, invoices=invoices, company=company)
        self.setTerzoIntermediarioOSoggettoEmittente(company, fatturapa)

    def setFatturaElettronicaBody(self, inv, FatturaElettronicaBody):

        self.line_desc = False
        self.setDatiGeneraliDocumento(inv, FatturaElettronicaBody)
        self.setDettaglioLinee(inv, FatturaElettronicaBody)
        self.setDatiDDT(inv, FatturaElettronicaBody)
        self.setDatiRitenuta(inv, FatturaElettronicaBody)
        self.setDatiBollo(inv, FatturaElettronicaBody)
        self.setDatiCassaPrevidenziale(inv, FatturaElettronicaBody)
        self.setDatiTrasporto(inv, FatturaElettronicaBody)
        self.setRelatedDocumentTypes(inv, FatturaElettronicaBody)
        self.setDatiRiepilogo(inv, FatturaElettronicaBody)
        self.setDatiPagamento(inv, FatturaElettronicaBody)
        self.setAttachments(inv, FatturaElettronicaBody)

    def group_invoices_by_partner(self):
        def split_list(my_list, size):
            it = iter(my_list)
            item = list(itertools.islice(it, size))
            while item:
                yield item
                item = list(itertools.islice(it, size))

        invoice_ids = self.env.context.get("active_ids", False)
        res = {}
        company = False
        for invoice in self.env["account.invoice"].browse(invoice_ids):
            company = company or invoice.company_id
            if company != invoice.company_id:
                raise UserError(_("Invoices must belong to the same company"))
            if invoice.partner_id not in res:
                res[invoice.partner_id] = []
            res[invoice.partner_id].append(invoice.id)

        for partner_id in res.keys():
            # Currently max_invoice_in_xml is not supported
            # if partner_id.max_invoice_in_xml:
            #     res[partner_id] = list(
            #         split_list(res[partner_id], partner_id.max_invoice_in_xml))
            # else:
            #     res[partner_id] = [res[partner_id]]
            res[partner_id] = list(split_list(res[partner_id], 1))
        return res, company

    def get_invoice_obj(self, fatturapa_attachment):
        xml_string = fatturapa_attachment.get_xml_string()
        return fatturapa_v_1_2.CreateFromDocument(xml_string)

    def exportInvoiceXML(
        self, company, partner, invoice_ids, attach=False, context=None
    ):
        context = context or {}
        invoices = self.env["account.invoice"].browse(invoice_ids)
        self_invoices_by_fiscaldoc = invoices.filtered(
            lambda x: x.is_self_invoice
        )
        invoices_no_self_by_fiscaldoc = invoices.filtered(
            lambda x: not x.is_self_invoice
        )
        if self_invoices_by_fiscaldoc and invoices_no_self_by_fiscaldoc:
            raise UserError(_(
                "Select invoices are of too many fiscal document types: "
                "select invoices exclusively of type 'TD17', 'TD18', 'TD19' "
                "or exclusively of other types."
            ))
        invoices_pa = invoices.filtered(
            lambda x: x.partner_id.commercial_partner_id.is_pa
        )
        invoices_no_pa = invoices.filtered(
            lambda x: not x.partner_id.commercial_partner_id.is_pa
        )
        if invoices_pa and invoices_no_pa:
            raise UserError(_(
                "Selected invoices are both PA and not PA."
                " You should selected a smaller set of invoices"))
        invoices_sender_cc = invoices.filtered(
            lambda x: x.sender == "CC"
        )
        invoices_no_cc = invoices.filtered(
            lambda x: not x.sender
        )
        if invoices_sender_cc and invoices_no_cc:
            raise UserError(_(
                "Selected invoices are both sender 'CC' and no sender."
                " You should selected a smaller set of invoices"))

        context[
            "self_invoices_by_fiscaldoc"
        ] = [x.fiscal_document_type_id.code
             for x in self_invoices_by_fiscaldoc]
        fatturapa = FatturaElettronica(versione=self._getFormatoTrasmissione(partner))

        try:
            self.with_context(context).setFatturaElettronicaHeader(
                company, partner, fatturapa, invoices=invoices
            )
            for invoice in invoices:
                if invoice.type not in ["out_invoice", "out_refund"]:
                    raise UserError(
                        _("Impossible to generate XML: not a customer invoice")
                    )
                if not attach and invoice.fatturapa_attachment_out_id:
                    raise UserError(
                        _("E-invoice export file still present for invoice %s.")
                        % (invoice.number)
                    )

                if self.report_print_menu:
                    self.generate_attach_report(invoice)
                invoice_body = FatturaElettronicaBodyType()
                invoice.preventive_checks()
                self.with_context(context).setFatturaElettronicaBody(invoice,
                                                                     invoice_body)
                fatturapa.FatturaElettronicaBody.append(invoice_body)
                # TODO DatiVeicoli

            number = self.setProgressivoInvio(fatturapa, attach=attach)
        except (SimpleFacetValueError, SimpleTypeValueError) as e:   # pragma: no cover
            raise UserError(_u(e))
        return fatturapa, number

    def exportFatturaPA(self):
        invoice_model = self.env["account.invoice"]
        attachments = self.env["fatturapa.attachment.out"]
        invoices_by_partner, company = self.group_invoices_by_partner()

        for partner in invoices_by_partner:
            if not partner.electronic_invoice_subjected and not partner.is_pa:
                raise UserError(
                    _("Partner %s in invoice %s not subjected to electronic invoice!")
                    % (partner.name or partner.commercial_partner_id.name,
                       invoice_model.browse(invoices_by_partner[partner][0]).number)
                )

        for partner in invoices_by_partner:
            context_partner = self.env.context.copy()
            context_partner.update({"lang": partner.lang})
            for invoice_ids in invoices_by_partner[partner]:
                fatturapa, number = self.exportInvoiceXML(
                    company, partner, invoice_ids, context=context_partner
                )

                attach = self.saveAttachment(fatturapa, number)
                attachments |= attach

                for invoice_id in invoice_ids:
                    inv = invoice_model.browse(invoice_id)
                    inv.write({"fatturapa_attachment_out_id": attach.id})

        action = {
            "view_type": "form",
            "name": "Export Electronic Invoice",
            "res_model": "fatturapa.attachment.out",
            "type": "ir.actions.act_window",
        }
        if len(attachments) == 1:                                    # pragma: no cover
            action["view_mode"] = "form"
            action["res_id"] = attachments[0].id
        else:
            action["view_mode"] = "tree,form"
            action["domain"] = [("id", "in", attachments.ids)]
        return action

    def generate_attach_report(self, inv):
        action_report_model, action_report_id = (
            self.report_print_menu.value.split(",")[0],
            int(self.report_print_menu.value.split(",")[1]),
        )
        action_report = self.env[action_report_model].browse(action_report_id)
        report_model = self.env["report"]
        attachment_model = self.env["ir.attachment"]
        # Generate the PDF: if report_action.attachment is set
        # they will be automatically attached to the invoice,
        # otherwise use res to build a new attachment
        res = report_model.get_pdf(inv.ids, action_report.report_name)
        if action_report.attachment:
            # If the report is configured to be attached
            # to the current invoice, just get that from the attachments.
            # Note that in this case the attachment in
            # fatturapa_doc_attachments is exactly the same
            # that is attached to the invoice.
            attachment = report_model._attachment_stored(inv, action_report)[inv.id]
        else:
            # Otherwise, create a new attachment to be stored in
            # fatturapa_doc_attachments.
            filename = inv.number
            data_attach = {
                "name": filename,
                "datas": base64.b64encode(res),
                "datas_fname": filename,
                "type": "binary",
            }
            attachment = attachment_model.create(data_attach)
        inv.write(
            {
                "fatturapa_doc_attachments": [
                    (
                        0,
                        0,
                        {
                            "is_pdf_invoice_print": True,
                            "ir_attachment_id": attachment.id,
                            "description": _(
                                "Attachment generated by " "electronic invoice export"
                            ),
                        },
                    )
                ]
            }
        )
