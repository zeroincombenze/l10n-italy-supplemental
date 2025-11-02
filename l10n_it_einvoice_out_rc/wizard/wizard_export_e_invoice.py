# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.exceptions import UserError
# from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export
from odoo.addons.l10n_it_ade.bindings.fatturapa_v_1_2 import (
    IdFiscaleType,
    # AnagraficaType,
    # CessionarioCommittenteType,
    # DatiTrasmissioneType,
    # IndirizzoType,
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def _setIdTrasmittente_rc(self, partner, fatturapa):
        if not partner.country_id:
            raise UserError(_("Partner %s, Country not set.") % partner.display_name)
        IdPaese = partner.country_id.code
        IdCodice = partner.fiscalcode
        if not IdCodice:
            if partner.vat:
                IdCodice = partner.vat[2:]
        if not IdCodice:
            IdCodice = "%s99999999999" % IdPaese
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione.IdTrasmittente = (
            IdFiscaleType(IdPaese=IdPaese, IdCodice=IdCodice)
        )
        return True

    def _setStabileOrganizzazione(self, CedentePrestatore, company):
        res = super(WizardExportFatturapa, self)._setStabileOrganizzazione(
            CedentePrestatore, company)
        if self.env.context.get("rc_supplier"):
            CedentePrestatore.StabileOrganizzazione = None
        return res

    def _setRea(self, CedentePrestatore, company):
        res = super(WizardExportFatturapa, self)._setRea(CedentePrestatore, company)
        if self.env.context.get("rc_supplier"):
            CedentePrestatore.IscrizioneREA = None
        return res

    def _setContatti(self, CedentePrestatore, company):
        res = super(WizardExportFatturapa, self)._setContatti(
            CedentePrestatore, company)
        if self.env.context.get("rc_supplier"):
            CedentePrestatore.Contatti = None
        return res

    def _setPubAdministrationRef(self, CedentePrestatore, company, partner):
        res = super(WizardExportFatturapa, self)._setPubAdministrationRef(
            CedentePrestatore, company, partner)
        if self.env.context.get("rc_supplier"):
            CedentePrestatore.RiferimentoAmministrazione = None
        return res

    def setDatiGeneraliDocumento(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiGeneraliDocumento(
            invoice, body)
        if (
            invoice.rc_purchase_invoice_id and
            invoice.rc_purchase_invoice_id.fiscal_position_id and
            invoice.rc_purchase_invoice_id.fiscal_position_id.rc_type_id and
            invoice.rc_purchase_invoice_id.fiscal_position_id.rc_type_id.
                fiscal_document_type_id
        ):
            body.DatiGenerali.DatiGeneraliDocumento.TipoDocumento = (
                invoice.fiscal_document_type_id.code)
        if invoice.type in ['out_refund', 'in_refund'] \
                and invoice.fiscal_document_type_id.code not in ['TD04', 'TD08']:
            body.DatiGenerali.DatiGeneraliDocumento.ImportoTotaleDocumento = (
                "%.2f" % -float(
                    body.DatiGenerali.DatiGeneraliDocumento.ImportoTotaleDocumento))
        return res

    def setDettaglioLinea(
        self, line_no, line, body, price_precision, uom_precision
    ):
        DettaglioLinea = super(WizardExportFatturapa, self).setDettaglioLinea(
            line_no, line, body, price_precision, uom_precision)
        if line.invoice_id.type in ['out_refund', 'in_refund'] and \
                line.invoice_id.fiscal_document_type_id.code not in ['TD04', 'TD08']:
            DettaglioLinea.PrezzoUnitario = (("%." + str(price_precision) + "f") %
                                             -float(DettaglioLinea.PrezzoUnitario))
            DettaglioLinea.PrezzoTotale = (
                "%.2f" % -float(DettaglioLinea.PrezzoTotale))
        return DettaglioLinea

    def setDatiRiepilogo(self, invoice, body):
        super(WizardExportFatturapa, self).setDatiRiepilogo(invoice, body)
        for DatiRiepilogo in body.DatiBeniServizi.DatiRiepilogo:
            if invoice.type in ['out_refund', 'in_refund'] \
                    and invoice.fiscal_document_type_id.code not in ['TD04', 'TD08']:
                DatiRiepilogo.ImponibileImporto = (
                    "%.2f" % -float(DatiRiepilogo.ImponibileImporto))
                DatiRiepilogo.Imposta = ("%.2f" % -float(DatiRiepilogo.Imposta))
        return True

    def setDatiPagamento(self, invoice, body):
        super(WizardExportFatturapa, self).setDatiPagamento(invoice, body)
        for DatiPagamento in body.DatiPagamento:
            if (
                invoice.type in ['out_refund', 'in_refund']
                and invoice.fiscal_document_type_id.code not in ['TD04', 'TD08']
                and "ImportoPagamento" in DatiPagamento
                and DatiPagamento.ImportoPagamento
            ):
                DatiPagamento.ImportoPagamento = (
                    "%.2f" % -float(DatiPagamento.ImportoPagamento))
        return True

    def exportInvoiceXML(
        self, company, partner, invoice_ids, attach=False, context=None
    ):
        context = context or {}
        invoices = self.env["account.invoice"].browse(invoice_ids)
        invoices_with_rc = invoices.filtered(
            lambda x: x.rc_purchase_invoice_id
        )
        invoices_without_rc = invoices.filtered(
            lambda x: not x.rc_purchase_invoice_id
        )
        if invoices_with_rc and invoices_without_rc:
            raise UserError(_(
                "Selected invoices are both with and without reverse charge. You "
                "should selected a smaller set of invoices"))
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
        rc_suppliers = invoices._get_original_suppliers()
        if len(rc_suppliers) > 1:
            raise UserError(_(
                "Selected reverse charge invoices have different suppliers. Please "
                "select invoices with same supplier"))
        if rc_suppliers:
            context["rc_supplier"] = rc_suppliers[0]
            context[
                "invoices_no_self_by_fiscaldoc"
            ] = [x.fiscal_document_type_id.code
                 for x in invoices_no_self_by_fiscaldoc]
            context["company_partner"] = company.partner_id
        return super(WizardExportFatturapa, self).exportInvoiceXML(
            company, partner, invoice_ids, attach, context=context
        )
