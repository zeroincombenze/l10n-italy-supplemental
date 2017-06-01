# -*- coding: utf-8 -*-
# Copyright 2017 Didotech srl (<http://www.didotech.com>)
#                Andrei Levin <andrei.levin@didotech.com>
#                Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo-Italia.org Community
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.osv import fields, orm
# from openerp.addons.l10n_it_vat_settlement.bindings.vat_settlement_v_1_0 import (
from l10n_it_pyxb_bindings.bindings.vat_settlement_v_1_0 import (
    Fornitura,
    # Intestazione,
    Intestazione_IVP_Type,
    # Comunicazione,
    Comunicazione_IVP_Type,
    Frontespizio_IVP_Type,
    DatiContabili_IVP_Type,
    CTD_ANON
)
import base64
import logging
import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

_logger = logging.getLogger(__name__)


_logger.setLevel(logging.DEBUG)


codice_fornitura = 'IVP17'
identificativo = "12345"
# TODO: mettere in impostazioni del modulo
FirmaDichiarazione = False
# TODO: which format????
# identificativo_software = 'LibrERP61'
identificativo_software = '61'


class WizardVatSettlement(orm.TransientModel):
    _name = "wizard.vat.settlement"

    _columns = {
        'data': fields.binary("File", readonly=True),
        'name': fields.char('Filename', 32, readonly=True),
        'state': fields.selection((
            ('create', 'create'),  # choose
            ('get', 'get'),  # get the file
        )),
    }

    _defaults = {
        'state': lambda *a: 'create',
    }

    def get_date_start_stop(self, statement, context=None):
        date_start = False
        date_stop = False
        for period in statement.period_ids:
            if not date_start:
                date_start = period.date_start
            else:
                if period.date_start < date_start:
                    date_start = period.date_start
            if not date_stop:
                date_stop = period.date_stop
            else:
                if period.date_stop > date_stop:
                    date_stop = period.date_stop
        date_start = datetime.datetime.strptime(date_start,
                                                DEFAULT_SERVER_DATE_FORMAT)
        date_stop = datetime.datetime.strptime(date_stop,
                                               DEFAULT_SERVER_DATE_FORMAT)
        return date_start, date_stop

    def get_taxable(self, cr, uid, statement, invoice_type, context=None):
        """
        :param cr:
        :param uid:
        :param statement:
        :param invoice_type: 'out_invoice' or 'in_invoice'
        :param context:
        :return: amount_taxable
        """

        invoice_obj = self.pool['account.invoice']
        # Selet invoice base on periods of statements.
        # Date invoice is not valeid, because Italian user can write
        # supplier invoices to another period
        # date_start, date_stop = self.get_date_start_stop(statemente,
        #                                                  context=context)
        periods = []
        for period in statement.period_ids:
            periods.append(period.id)
        domain = [
            # ('date_invoice', '>=', date_start),
            # ('date_invoice', '<=', date_stop),
            ('period_id', 'in', periods),
            ('type', '=', invoice_type),
            ('state', 'in', ('paid', 'open'))
        ]
        invoice_ids = invoice_obj.search(cr, uid, domain)
        taxables = [invoice.amount_untaxed for invoice in invoice_obj.browse(cr, uid, invoice_ids, context)]

        return reduce(lambda x, y: x + y, taxables, 0)

    @staticmethod
    def italian_number(number):
        return '{:.2f}'.format(number).replace('.', ',')

    def export_vat_settlemet(self, cr, uid, ids, context=None):
        # TODO: insert period verification

        context = {} if context is None else context

        model_data_obj = self.pool['ir.model.data']
        # vat_period_end_statement_obj = self.pool['account.vat.period.end.statement']
        statement_debit_account_line_obj = self.pool['statement.debit.account.line']
        statement_credit_account_line_obj = self.pool['statement.credit.account.line']

        self.company = self.pool['res.users'].browse(
            cr, uid, uid, context=context).company_id

        trimestre = {
            '3': '1',
            '6': '2',
            '9': '3',
            '12': '4'
        }

        statement_ids = context.get('active_ids', False)

        for statement in self.pool[
                'account.vat.period.end.statement'].browse(cr,
                                                           uid,
                                                           statement_ids,
                                                           context=context):
            settlement = Fornitura()
            settlement.Intestazione = (Intestazione_IVP_Type())
            settlement.Intestazione.CodiceFornitura = codice_fornitura
            # settlement.Intestazione.CodiceFiscaleDichiarante =
            # settlement.Intestazione.CodiceCarica =
            # settlement.Intestazione.IdSistema

            _logger.debug(settlement.Intestazione.toDOM().toprettyxml(
                encoding="latin1"))

            settlement.Comunicazione = (Comunicazione_IVP_Type())
            settlement.Comunicazione.Frontespizio = (Frontespizio_IVP_Type())
            settlement.Comunicazione.Frontespizio.CodiceFiscale = \
                self.company.partner_id.fiscalcode

            # date_period_end = datetime.datetime.strptime(statement.date, DEFAULT_SERVER_DATE_FORMAT)
            # settlement.Comunicazione.Frontespizio.AnnoImposta = str(date_period_end.year)
            date_start, date_stop = self.get_date_start_stop(statement,
                                                             context=context)
            settlement.Comunicazione.Frontespizio.AnnoImposta = str(
                date_stop.year)

            if self.company.partner_id.vat[:2].lower() == 'it':
                vat = self.company.partner_id.vat[2:]
            else:
                vat = self.company.partner_id.vat
            settlement.Comunicazione.Frontespizio.PartitaIVA = vat
            # settlement.Comunicazione.Frontespizio.PIVAControllante
            # settlement.Comunicazione.Frontespizio.UltimoMese = str(date_period_end.month)
            # settlement.Comunicazione.Frontespizio.LiquidazioneGruppo
            # settlement.Comunicazione.Frontespizio.CFDichiarante
            # settlement.Comunicazione.Frontespizio.CodiceCaricaDichiarante
            # settlement.Comunicazione.Frontespizio.CodiceFiscaleSocieta
            # TODO: Per il momento 0, poi dovremmo stampare il modulo
            settlement.Comunicazione.Frontespizio.FirmaDichiarazione = "1"
            # settlement.Comunicazione.Frontespizio.CFIntermediario = "0"
            # settlement.Comunicazione.Frontespizio.ImpegnoPresentazione = "1"
            # settlement.Comunicazione.Frontespizio.DataImpegno
            # settlement.Comunicazione.Frontespizio.FirmaIntermediario
            # settlement.Comunicazione.Frontespizio.FlagConferma
            # settlement.Comunicazione.Frontespizio.IdentificativoProdSoftware = identificativo_software

            _logger.debug(settlement.Comunicazione.Frontespizio.toDOM().toprettyxml(encoding="latin1"))

            settlement.Comunicazione.DatiContabili = (DatiContabili_IVP_Type())

            # We may have more than one modulo, but do we want it?
            # modulo_period_end = datetime.datetime.strptime(statement.date,
            #                                                DEFAULT_SERVER_DATE_FORMAT)
            modulo = CTD_ANON()
            # <<<<< quarter_vat_period non esite nella 7.0 >>>>>
            # if statement.period_ids[0].fiscalyear_id.quarter_vat_period:
            #     # trimestrale
            #     modulo.Trimestre = trimestre[str(modulo_period_end.month)]
            # else:
            #     # mensile
            #    modulo.Mese = str(modulo_period_end.month)
            if date_start.month == date_stop.month:
                modulo.Mese = str(date_stop.month)
            else:
                if date_start.month in (1, 4, 7, 10) and \
                        date_stop.month in (3, 6, 9, 11):
                    modulo.Trimestre = trimestre[str(date_stop.month)]
            # TODO: Per aziende supposte al controllo antimafia (i subfornitori), per il momento non valorizziamo
            # modulo.Subfornitura = "0"
            # TODO: facultativo: Vittime del terremoto, per il momento non valorizziamo
            # modulo.EventiEccezionali =

            modulo.TotaleOperazioniAttive = self.italian_number(
                self.get_taxable(cr, uid, statement, 'out_invoice', context)
            )
            modulo.TotaleOperazioniPassive = self.italian_number(
                self.get_taxable(cr, uid, statement, 'in_invoice', context)
            )

            iva_esigibile = 0
            debit_account_line_ids = statement_debit_account_line_obj.search(
                cr, uid, [('statement_id', '=', statement.id)])
            for debit_account_line in statement_debit_account_line_obj.browse(
                    cr, uid, debit_account_line_ids, context):
                iva_esigibile += debit_account_line.amount
            # NOTE: formato numerico;
            #  i decimali vanno separati con il carattere  ',' (virgola)
            modulo.IvaEsigibile = self.italian_number(iva_esigibile)

            iva_detratta = 0
            credit_account_line_ids = statement_credit_account_line_obj.search(
                cr, uid, [('statement_id', '=', statement.id)])
            for credit_account_line in statement_credit_account_line_obj.\
                    browse(cr, uid, credit_account_line_ids, context):
                iva_detratta += credit_account_line.amount
            # NOTE: formato numerico;
            #  i decimali vanno separati con il carattere  ',' (virgola)
            modulo.IvaDetratta = self.italian_number(iva_detratta)

            if iva_esigibile > iva_detratta:
                iva_dovuta = iva_esigibile - iva_detratta
                modulo.IvaDovuta = self.italian_number(iva_dovuta)
            else:
                iva_credito = iva_detratta - iva_esigibile
                modulo.IvaCredito = self.italian_number(iva_credito)
            # TODO: lasciamo per dopo
            # modulo.IvaDetratta = self.italian_number(iva_detratta)
            # modulo.IvaCredito =

            previous_debit = statement.previous_debit_vat_amount
            if previous_debit:
                modulo.DebitoPrecedente = self.italian_number(previous_debit)

            previous_credit = statement.previous_credit_vat_amount
            if previous_credit:
                if date_start.month == 1:
                    modulo.CreditoAnnoPrecedente = self.italian_number(previous_credit)
                else:
                    modulo.CreditoPeriodoPrecedente = self.italian_number(previous_credit)

            # Chiedere all'utente
            # modulo.CreditoAnnoPrecedente

            # TODO: lasciamo per dopo
            # modulo.VersamentiAutoUE

            # modulo.CreditiImposta
            # modulo.InteressiDovuti
            # modulo.Acconto

            if statement.authority_vat_amount > 0:
                # NOTE: formato numerico; i decimali vanno separati dall'intero con il carattere  ',' (virgola)
                modulo.ImportoDaVersare = self.italian_number(statement.authority_vat_amount)
            elif statement.authority_vat_amount < 0:
                # NOTE: formato numerico; i decimali vanno separati dall'intero con il carattere  ',' (virgola)
                modulo.ImportoACredito = self.italian_number(statement.authority_vat_amount)

            settlement.Comunicazione.DatiContabili.Modulo.append(modulo)

            _logger.debug(settlement.Comunicazione.DatiContabili.toDOM().toprettyxml(encoding="latin1"))

            settlement.Comunicazione.identificativo = identificativo

            vat_settlement_xml = settlement.toDOM().toprettyxml(encoding="latin1")

            # TODO: Resolve: It will attach separate XML to every vat.period.end.statement document
            attach_vals = {
                'name': 'Liquidazione IVA {}.xml'.format(date_stop.month),
                'datas_fname': 'Liquidazione IVA {}.xml'.format(date_stop.month),
                'datas': base64.encodestring(vat_settlement_xml),
                'res_model': 'account.vat.period.end.statement',
                'res_id': statement.id
            }
            vat_settlement_attachment_out_id = self.pool['account.vat.settlement.attachment'].create(cr, uid, attach_vals, context={})

        view_rec = model_data_obj.get_object_reference(
            cr, uid, 'l10n_it_vat_settlement',
            'view_vat_settlement_attachment_form')
        if view_rec:
            view_id = view_rec and view_rec[1] or False
        return {
            'view_type': 'form',
            'name': "Export Liquidazione IVA",
            'view_id': [view_id],
            'res_id': vat_settlement_attachment_out_id,
            'view_mode': 'form',
            'res_model': 'account.vat.settlement.attachment',
            'type': 'ir.actions.act_window',
            'context': context
        }
