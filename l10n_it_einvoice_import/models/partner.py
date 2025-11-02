# -*- coding: utf-8 -*-
#
# Copyright 2018-19 - Odoo Italia Associazione <https://www.odoo-italia.org>
# Copyright 2018-19 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
import logging

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"

    e_invoice_default_product_id = fields.Many2one(
        comodel_name="product.product",
        string="E-bill Default Product",
        help="Used by electronic invoice XML import. "
        "If filled in, generated bill lines will use this product when "
        "no other possible product is found.",
    )
    e_invoice_default_account_id = fields.Many2one(
        comodel_name="account.account",
        string="E-bill Default Account",
        help="Used by electronic invoice XML import. "
        "If filled in, generated bill lines will use this account when "
        "no other possible product is found.",
    )
    e_invoice_detail_level = fields.Selection(
        [
            ("0", "Minimum"),
            ("1", "Aliquote"),
            ("2", "Maximum"),
        ],
        string="E-bills Detail Level",
        help="Minimum level: Bill is created with no lines; "
        "User will have to create them, according to what specified in "
        "the electronic bill.\n"
        # "Livello Aliquote: viene creata una riga fattura per ogni "
        # "aliquota presente nella fattura elettronica\n"
        "Maximum level: every line contained in the electronic bill "
        "will create a line in the bill.",
        default="2",
        required=True,
    )

    def CountryByCode(self, CountryCode):
        country_model = self.env["res.country"]
        return country_model.search([("code", "=", CountryCode)])

    def ProvinceByCode(self, provinceCode):
        province_model = self.env["res.country.state"]
        return province_model.search(
            [("code", "=", provinceCode), ("country_id.code", "=", "IT")]
        )

    def check_partner_base_data(self, partner_id, DatiAnagrafici, fatturapa):
        partner = self.env["res.partner"].browse(partner_id)
        if (
            DatiAnagrafici.Anagrafica.Denominazione
            and partner.name != DatiAnagrafici.Anagrafica.Denominazione
        ):
            fatturapa.log_inconsistency(
                _("Ragione sociale da XML '%s' " "differisce da dato in sistema'%s'.")
                % (DatiAnagrafici.Anagrafica.Denominazione, partner.name)
            )
        if (
            DatiAnagrafici.Anagrafica.Nome
            and partner.firstname != DatiAnagrafici.Anagrafica.Nome
        ):
            fatturapa.log_inconsistency(
                _("Nome da XML '%s' " "differisce da dato in sistema'%s'.")
                % (DatiAnagrafici.Anagrafica.Nome, partner.firstname or partner.name)
            )
        if (
            DatiAnagrafici.Anagrafica.Cognome
            and partner.lastname != DatiAnagrafici.Anagrafica.Cognome
        ):
            fatturapa.log_inconsistency(
                _("Cognome da XML '%s' " "differisce da dato in sistema'%s'.")
                % (DatiAnagrafici.Anagrafica.Cognome, partner.lastname or partner.name)
            )

    def getPartnerBase(self, partner_xml, fatturapa=None):
        """Get data from xml and write or create partner"""
        if not partner_xml:
            return -1
        if hasattr(partner_xml, "DatiAnagrafici"):
            DatiAnagrafici = partner_xml.DatiAnagrafici
        else:
            return -1
        if hasattr(DatiAnagrafici, "Anagrafica"):
            Anagrafica = DatiAnagrafici.Anagrafica
        else:
            return -1
        fiscalPosModel = self.env["fatturapa.fiscal_position"]
        vals = {
            "customer": False,
            "supplier": True,
            "is_company": True,
            "street": partner_xml.Sede.Indirizzo,
            "zip": partner_xml.Sede.CAP,
            "city": partner_xml.Sede.Comune,
        }
        if partner_xml.Sede.Provincia:
            Provincia = partner_xml.Sede.Provincia
            prov_sede = self.ProvinceByCode(Provincia)
            if not prov_sede:
                if fatturapa:
                    fatturapa.log_inconsistency(
                        _('Provincia "%s" non presente in archivio') % Provincia
                    )
                else:
                    raise UserError(
                        _('Provincia "%s" non presente in archivio') % Provincia
                    )
            else:
                vals["state_id"] = prov_sede[0].id

        if partner_xml.Contatti:
            vals["phone"] = partner_xml.Contatti.Telefono
            vals["email"] = partner_xml.Contatti.Email
            vals["fax"] = partner_xml.Contatti.Fax

        if DatiAnagrafici.AlboProfessionale:
            vals["register"] = DatiAnagrafici.AlboProfessionale
            if DatiAnagrafici.ProvinciaAlbo:
                ProvinciaAlbo = DatiAnagrafici.ProvinciaAlbo
                prov = self.ProvinceByCode(ProvinciaAlbo)
                if not prov:
                    if fatturapa:
                        fatturapa.log_inconsistency(
                            _('Provincia albo "%s" non presente in archivio ')
                            % ProvinciaAlbo
                        )
                else:
                    vals["register_province"] = prov[0].id
            vals["register_code"] = DatiAnagrafici.NumeroIscrizioneAlbo or ""
            vals["register_regdate"] = DatiAnagrafici.DataIscrizioneAlbo or ""

        if DatiAnagrafici.RegimeFiscale:
            rfPos = DatiAnagrafici.RegimeFiscale
            FiscalPos = fiscalPosModel.search([("code", "=", rfPos)])
            if not FiscalPos:
                raise UserError(_("Tax Regime %s not present in your system.") % rfPos)
            else:
                vals["register_fiscalpos"] = FiscalPos[0].id

        if partner_xml.IscrizioneREA:
            REA = partner_xml.IscrizioneREA
            vals["rea_code"] = REA.NumeroREA
            offices = self.ProvinceByCode(REA.Ufficio)
            if not offices:
                if fatturapa:
                    fatturapa.log_inconsistency(
                        _('Provincia ufficio REA "%s" non presente in ' "archivio")
                        % REA.Ufficio
                    )
            else:
                office_id = offices[0].id
                vals["rea_office"] = office_id
            vals["rea_capital"] = REA.CapitaleSociale or 0.0
            vals["rea_member_type"] = REA.SocioUnico or False
            vals["rea_liquidation_state"] = REA.StatoLiquidazione or False

        if DatiAnagrafici.CodiceFiscale:
            vals["fiscalcode"] = DatiAnagrafici.CodiceFiscale
        if DatiAnagrafici.IdFiscaleIVA:
            vals["vat"] = "%s%s" % (
                DatiAnagrafici.IdFiscaleIVA.IdPaese,
                DatiAnagrafici.IdFiscaleIVA.IdCodice,
            )

        if (
            hasattr(partner_xml, "DatiAnagraficiVettore")
            and partner_xml.DatiAnagraficiVettore
            and partner_xml.DatiAnagraficiVettore.NumeroLicenzaGuida
        ):
            vals[
                "license_number"
            ] = partner_xml.DatiAnagraficiVettore.NumeroLicenzaGuida

        if DatiAnagrafici.IdFiscaleIVA:
            CountryCode = DatiAnagrafici.IdFiscaleIVA.IdPaese
            countries = self.CountryByCode(CountryCode)
            if countries:
                country_id = countries[0].id
            else:
                raise UserError(
                    _("Country Code %s not found in the system.") % CountryCode
                )
            vals["country_id"] = country_id
        if Anagrafica.CodEORI:
            vals["eori_code"] = Anagrafica.CodEORI
        if Anagrafica.Denominazione:
            vals["name"] = Anagrafica.Denominazione
        else:
            vals["name"] = "%s %s" % (Anagrafica.Cognome, Anagrafica.Nome)
        SKEYS = (
            ["vat", "fiscalcode", "type"],
            ["vat", "name", "type"],
            ["fiscalcode", "dim_name", "type"],
            ["vat", "dim_name", "type"],
            ["rea_code"],
            ["vat", "type"],
            ["dim_name", "type"],
            ["vat", "fiscalcode", "is_company"],
            ["vat"],
            ["name", "is_company"],
        )
        partner_id = self.synchro2(
            "res.partner",
            vals,
            skeys=SKEYS,
            constraints=[("id", "!=", "parent_id")],
            keep=[
                "customer",
                "country_id",
                "name",
                "street",
                "zip",
                "city",
                "state_id",
                "phone",
            ],
            default={
                "rea_member_type": "SM",
                "rea_liquidation_state": "LN",
                "type": "contact",
                "supplier": True,
            },
        )
        if partner_id > 0:
            partner = self.browse(partner_id)
            if partner.type == "invoice":
                partner_id = partner.parent_id.id
            if fatturapa:
                self.check_partner_base_data(partner_id, DatiAnagrafici, fatturapa)
        return partner_id

    @api.model
    def synchro2(
        self, model, values, skeys=None, constraints=None, keep=None, default=None
    ):
        def is_the_same(rec, vals):
            for field in ("name", "street", "zip", "city"):
                if self.dim_text(rec[field]) != self.dim_text(vals.get(field, "")):
                    break
            return rec

        def clear_dup_rea_code(vals):
            if "rea_code" in vals:
                for rec in self.search([("rea_code", "=", vals["rea_code"])]):
                    if rec.type != "contact" or rec.parent_id:
                        rec.write({"rea_code": False})

        vals = values.copy()
        clear_dup_rea_code(vals)
        skeys = skeys or []
        MAGIC_FIELDS = {
            "company_id": False,
            "is_company": True,
            "supplier": True,
        }
        keep = keep or []
        default = default or {}
        rec = False
        for keys in skeys:
            domain = []
            repeat = False
            for key in keys:
                if key not in vals and key == "type":
                    domain.append([key, "=", "invoice"])
                    repeat = True
                elif key not in vals and key in MAGIC_FIELDS:
                    if MAGIC_FIELDS[key]:
                        domain.append([key, "=", MAGIC_FIELDS[key]])
                elif key not in vals:
                    domain = []
                    break
                else:
                    domain.append([key, "=", vals[key]])
            if domain:
                for constr in constraints:
                    add_domain = False
                    if constr[0] in vals:
                        constr[0] = vals[constr[0]]
                        add_domain = True
                    if constr[-1] in vals:
                        constr[-1] = vals[constr[-1]]
                        add_domain = True
                    if add_domain:
                        domain.append(constr)
                rec = self.search(domain)
                if rec:
                    rec = rec[0]
                    break
                if repeat:
                    for i, kk in enumerate(domain):
                        if kk[0] == "type":
                            domain[i][2] = "contact"
                    domain.append(("parent_id", "=", False))
                    rec = self.search(domain)
                    if rec:
                        rec = rec[0]
                        break
        if rec:
            if rec.parent_id and is_the_same(rec.parent_id, vals):
                defvals = {}
                if rec.rea_code:
                    defvals["rea_code"] = False
                if rec.type == "contact":
                    defvals["type"] = "invoice"
                if rec.name == rec.parent_id.name:
                    defvals["name"] = False
                if defvals:
                    rec.write(defvals)
                rec = rec.parent_id
            if not rec.parent_id and not is_the_same(rec, vals):
                vals["parent_id"] = rec.id
                vals["type"] = "invoice"
                rec = False
        if rec:
            try:
                if rec.type != "invoice":
                    for field in keep:
                        if field in vals and rec[field]:
                            del vals[field]
                    for field in default:
                        if not vals.get(field) and field in default:
                            vals[field] = default[field]
                if "rea_code" in vals and (rec.rea_code or rec.type == "invoice"):
                    del vals["rea_code"]
                for item in vals.keys():
                    if (
                        vals[item] is None
                        or isinstance(rec[item], (basestring, bool, int, float))
                        and rec[item] == vals[item]
                    ):
                        del vals[item]
                if vals:
                    rec.write(vals)
                id = rec.id
            except BaseException as e:
                raise UserError(e)
        else:
            if vals.get("type") == "invoice" and "rea_code" in vals:
                del vals["rea_code"]
            try:
                id = self.create(vals).id
            except BaseException as e:
                raise UserError(e)
        return id
