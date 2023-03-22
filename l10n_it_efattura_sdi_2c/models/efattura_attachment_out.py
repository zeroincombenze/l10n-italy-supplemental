# -*- coding: utf-8 -*-
# © 2018 Nicola Gramola - Didotech srl (www.didotech.com)
# © 2019-2021 Andrei Levin - Didotech srl (www.didotech.com)

import logging
import base64
from datetime import datetime
from datetime import timedelta
from odoo import models, exceptions
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _
from .document_2c_fatturapa import ActiveInvoice_2C
from odoo.addons.l10n_it_efattura_sdi.models.sdi_lib import SimpleConfig
from odoo.addons.l10n_it_efattura_sdi.models.attachment import e_invoice_state

_logger = logging.getLogger(__name__)


class FatturaPAAttachment2C(models.Model):
    _inherit = "fatturapa.attachment.out"

    @staticmethod
    def get_2c_date(date_str):
        # 24.01.2019
        # TIME_FORMAT_2C = '%m/%d/%Y %I:%M:%S %p'
        # 29.01.2019
        # TIME_FORMAT_2C = '%d/%m/%Y %I:%M:%S %p'

        TIME_FORMAT_2C_US = '%m/%d/%Y %I:%M:%S %p'
        TIME_FORMAT_2C_EUR = '%d/%m/%Y %I:%M:%S %p'
        now = datetime.now()
        try:
            date = datetime.strptime(date_str, TIME_FORMAT_2C_EUR)
            if date.month == now.month:
                return date
            else:
                raise Exception('Probably month and day are inverted')
        except:
            try:
                date = datetime.strptime(date_str, TIME_FORMAT_2C_US)
                if date.month == now.month:
                    return date
                else:
                    raise Exception('Probably month and day are inverted')
            except:
                return now

    def upload_invoice(self, invoice_attachment_out, document_host):
        """
        Attention! This function works only with New APIs
        :param cr:
        :param uid:
        :param invoice_attachment_out:
        :param document_host:
        :param context:
        :return:
        """

        config = SimpleConfig(invoice_attachment_out.company_id)
        config.document_host = document_host
        fpa = ActiveInvoice_2C(config)

        invoice = invoice_attachment_out.out_invoice_ids[0]

        remote_fname = fpa.upload_data(invoice_attachment_out.datas_fname, base64.b64decode(invoice_attachment_out.datas))
        if remote_fname and remote_fname[-3:].lower() == 'zip':
            email = invoice.partner_id.invoice_email or False
            ret_sdi = fpa.send_invoice(email=email)

            if ret_sdi['IdSdi'] and not ret_sdi['ResultCode'] == 'Failure':
                sdi_date = self.get_2c_date(ret_sdi['DateSdi'])

                invoice_attachment_out.write({
                    # 'store_fname': 'idsdi:%s' % ret_sdi['IdSdi'],  # ret_sdi[0],
                    'sdi_fname': remote_fname,
                    'sdi_id': str(ret_sdi['IdSdi']),
                    'sdi_send_date': sdi_date,
                    'state': 'sent',
                })

                ret_sdi_text = "Identificativo SdI assegnato %s, data invio %s " % (
                    ret_sdi['IdSdi'], sdi_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT))

                invoice.message_post(body=ret_sdi_text, subject=ret_sdi['ResultCode'])
                invoice_attachment_out.message_post(body=ret_sdi_text, subject=ret_sdi['ResultCode'])
                return True
            elif ret_sdi['ResultCode'] == 'Failure':
                subject = ret_sdi['ResultCode']
                body = ret_sdi['ResultMessage']['string']

                invoice.message_post(body=body, subject=subject)
                invoice_attachment_out.message_post(body=body, subject=subject)
                if ret_sdi['IdSdi']:
                    raise exceptions.Error(ret_sdi['IdSdi'])
                return False
            else:
                invoice.message_post(body=str(ret_sdi), subject='Failure')
                invoice_attachment_out.message_post(body=str(ret_sdi), subject='Failure')
                if ret_sdi['IdSdi']:
                    raise exceptions.Error(ret_sdi['IdSdi'])

                return False
        else:
            return True

    def _hook_after_sent(self, fatturapa_attachment_out):
        return True

    def send_cron_invoice_sdi(self):
        if self:
            invoice_attachments = self
        else:
            invoice_attachments = self.search([('state', 'in', ('draft', 'ready'))])

        counter = 0
        for fatturapa_attachment_out in invoice_attachments:
            # if fatturapa_attachment_out.xml_error:
            #     continue

            try:
                fatturapa_attachment_out.action_send_invoice()
                fatturapa_attachment_out._hook_after_sent(
                    fatturapa_attachment_out)
            except Exception as error:
                _logger.error(error)

            counter += 1
            if counter == 10:
                counter = 0
                _logger.info('Committing...')
                self._cr.commit()  # pylint: disable=invalid-commit
        return True

    def update_status(self):
        tipo_messaggio = dict(e_invoice_state)

        if self:
            fattura_attachments = self
        else:
            fattura_attachments = self.search([
                ('state', '=', 'sent'),
                ('sdi_id', '!=', False)
            ])

        company = self.env['res.users'].browse(self.env.uid).company_id
        config = SimpleConfig(company)
        config.document_host = self.env['ir.config_parameter'].get_param('sdi_active_host')
        fpa = ActiveInvoice_2C(config)

        for attachment_out in fattura_attachments:
            if attachment_out.sdi_id:
                ret = fpa.get_sending_result(attachment_out.sdi_id)
                if ret and ret['ResultCode'] == 'Success' and ret['ElectronicInvoiceOutcomes']:
                    for message in ret['ElectronicInvoiceOutcomes']['ElectronicInvoiceOutcome']:
                        sending_result = self.translate_message_type(message['TipoMessaggio'])
                        sending_result['sdi_state'] = message['TipoMessaggio']
                        attachment_out.write(sending_result)
                        messaggio_log = "Messaggi FatturaPA. %s" % (tipo_messaggio.get(message['TipoMessaggio']),)
                        if attachment_out.out_invoice_ids:
                            body_text = messaggio_log + ": " + message['DescrizioneMessaggio'] if message['DescrizioneMessaggio'] else ''
                            attachment_out.out_invoice_ids[0].message_post(body=body_text, subject=ret['ResultCode'])

    def action_send_invoice(self):
        document_host = self.env['ir.config_parameter'].get_param('sdi_active_host')

        for attachment_out in self:
            if attachment_out.state in ('draft', 'ready'):
                self.upload_invoice(attachment_out, document_host)

        if len(self) == 1:
            view_res = self.env['ir.model.data'].get_object_reference(
                'l10n_it_efattura_sdi', 'view_fatturapa_out_state_form')
            view_id = view_res and view_res[1] or False

            return {
                'type': 'ir.actions.act_window',
                'name': _("Sent Invoices"),
                'res_model': 'fatturapa.attachment.out',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'res_id': self.id,
                'target': 'current'
            }
        elif len(self) > 1:
            # Unfortunately this doesn't work like it should. Sorry.
            view_res = self.env['ir.model.data'].get_object_reference(
                'l10n_it_fatturapa_out', 'view_fatturapa_out_attachment_tree')
#                 cr, uid, 'document_2c_fatturapa', 'view_fatturapa_out_state')
            view_id = view_res and view_res[1] or False

            return {
                'type': 'ir.actions.act_window',
                'name': _("Sent Invoices"),
                'res_model': 'fatturapa.attachment.out',
                'view_type': 'tree',
                'view_mode': 'tree',
                'view_id': [view_id],
                # 'res_id': ids,
                'target': 'current',
                # 'domain': "[('id', 'in', {ids})]".format(ids=ids)
                'domain': [('id', 'in', self.ids)]
            }

    def action_repair_state(self):
        # TODO: function is untested!!!
        draft_attachments = self.search([
            ('state', '=', 'draft'),
            ('sdi_id', '=', False)
        ])

        drafts = {draft.datas_fname: draft for draft in draft_attachments}

        config = SimpleConfig(self.company_id)
        config.document_host = self.env['ir.config_parameter'].get_param('sdi_active_host')
        fpa = ActiveInvoice_2C(config)

        today = datetime.datetime.now()
        delta = timedelta(days=1)
        date_start = today - delta

        invoices = fpa.search_invoices(date_start)
        for invoice in invoices:
            if invoice['TipoMessaggioEsito'] != 'NS':
                if invoice['NomeFileOriginaleFatturaPA'].rstrip('.p7m') in drafts:
                    drafts[invoice['NomeFileOriginaleFatturaPA'].rstrip('.p7m')].sdi_id = invoice['IdSdi']
                    drafts[invoice['NomeFileOriginaleFatturaPA'].rstrip('.p7m')].state = 'sent'
