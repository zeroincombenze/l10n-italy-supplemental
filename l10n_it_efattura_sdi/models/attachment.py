# -*- coding: utf-8 -*-
# © 2020-2021 Andrei Levin - Didotech srl (www.didotech.com)

from odoo import models, fields, exceptions
from odoo.modules.module import get_module_resource
from odoo.tools.translate import _
import lxml.etree as ET
from io import BytesIO
import logging
from .sdi_lib import ActiveInvoice
from .sdi_lib import SimpleConfig


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

e_invoice_state = [
    ('ready', 'Ready to Send'),
    ('sent', 'Sent'),
    ('error', 'Error'),
    ('NS', 'Notifica di Scarto'),
    ('MC', 'Notifica di Mancata Consegna'),
    ('RC', 'Ricevuta di Consegna'),
    ('EC_ACCETTAZIONE', 'Notifica di Esito Committente: ACCETTATA'),
    ('EC_RIFIUTO', 'Notifica di Esito Committente: RIFIUTATA'),
    ('SE', 'Notifica di Scarto Esito Committente'),
    ('NE', 'Notifica di Esito'),
    ('NE_ACCETTAZIONE', 'Notifica di Esito: ACCETTATA'),
    ('NE_RIFIUTO', 'Notifica di Esito: RIFIUTATA'),
    ('DT', 'Notifica di decorrenza di Decorrenza Termini'),
    ('AT', 'Attestazione di avvenuta trasmissione con impossibilità di recapito'),
    ('MT', 'Metadati'),
    ('ED', 'ED'),
    ('EF', 'EF'),
    ('EL', 'EL'),
    ('NA', 'NA'),
    ('NONE', 'Nessuna notifica')
]


class EInvoiceAttachmentOut(models.Model):
    _inherit = "fatturapa.attachment.out"
    _description = "Generic class for SDI communication"

    def _get_data(self):
        document_host = self.env['ir.config_parameter'].get_param('sdi_active_host')
        company = self.env['res.users'].browse(self._uid).company_id
        data = {}

        # TODO: implement flag use_local_storage
        # if document_host and not config.use_local_storage:
        if document_host:
            config = SimpleConfig(company)
            config.document_host = document_host
            fpa = ActiveInvoice

            for attachment in self:
                if attachment.store_fname and attachment.store_fname[:5] == 'idsdi':
                    data[attachment.id] = fpa.get_fatturapa(idsdi=attachment.store_fname[6:],
                                                            estrazioneP7M=config.extract_from_p7m)
                else:
                    data[attachment.id] = attachment.ir_attachment_id.datas
        else:
            for attachment in self:
                data[attachment.id] = attachment.ir_attachment_id.datas
        return data

    def _set_data(self, value):
        if value:
            attachment_out = self
            company = self.env['res.users'].browse(self.uid).company_id

            document_host = self.env['ir.config_parameter'].get_param('sdi_active_host')

            if attachment_out.datas_fname[-3:] == 'xml' and document_host and company.sdi_send:
                # Save XML on local server anyway
                attachment_out.ir_attachment_id.write({
                    'datas': value
                })
                # invoice_id = context['active_id']
                self.upload_invoice(self, document_host)

            elif not document_host and company.sdi_send:
                raise exceptions.Warning(
                    _('Please set destination host (sdi_active_host) for active invoice'))
            else:
                # attachment_out.write({
                #     'index_content': value.decode('base64').decode('latin-1').encode('utf-8')
                # })
                attachment_out.ir_attachment_id.write({
                    'datas': value
                })
                return True
        else:
            return True

    def _get_fattura_elettronica_preview(self):
        # TODO: should be rewritten with the new style
        user = self.env['res.users'].browse(self.uid)
        style_sheet_mode = user.company_id.style_sheet_mode

        if style_sheet_mode == 'asso_software':
            xsl_path = get_module_resource('l10n_it_fatturapa', 'data', 'FoglioStileAssoSoftware.xsl')
        else:
            xsl_path = get_module_resource('l10n_it_fatturapa', 'data', 'fatturaordinaria_v1.2.1.xsl')
        xslt = ET.parse(xsl_path)

        res = {}
        xml_strings = self._get_data()
        for fatturapa_attachment in self:
            try:
                xml_string = xml_strings[fatturapa_attachment.id]
                xml_file = BytesIO(xml_string)
                recovering_parser = ET.XMLParser(recover=True)
                dom = ET.parse(xml_file, parser=recovering_parser)
                transform = ET.XSLT(xslt)
                newdom = transform(dom)
                res[fatturapa_attachment.id] = ET.tostring(newdom, pretty_print=True)
            # except Exception as e:
            except Exception:
                res[fatturapa_attachment.id] = ''
        return res

    xml_preview = fields.Text(compute=_get_fattura_elettronica_preview, string="Preview", method=True)
    # datas = fields.Binary(compute=_get_data, fnct_inv=_set_data, string='File Content', nodrop=True)
    # fpa_2c_fname = fields.Text('SDI full file path')
    sdi_fname = fields.Text('SDI full file path')
    # fpa_idsdi': fields.char('ID SdI', 12)
    sdi_id = fields.Char('ID SdI', size=12)
    sdi_send_date = fields.Datetime('SdI send date')
    sdi_state = fields.Selection(e_invoice_state, 'SdI State', readonly=True, required=False)

    def action_send_invoice(self):
        """
        Depends on SDI provider
        :param cr:
        :param uid:
        :param ids:
        :param context:
        :return:
        """
        raise exceptions.Warning(_('Please install specific module to access your SDI provider'))

    def update_status(self):
        pass

    def send_cron_invoice_sdi(self):
        pass

    def action_check_state(self):
        """
        Should be overwritten in SDI specific module
        :return: None
        """
        pass

    def translate_message_type(self, message_type):
        if message_type == 'NS':  # 2A. Notifica di Scarto
            # error_list = root.find('ListaErrori')
            # error_str = ''
            # for error in error_list:
            #     error_str += "\n[%s] %s %s" % (
            #         error.find('Codice').text if error.find(
            #             'Codice') is not None else '',
            #         error.find('Descrizione').text if error.find(
            #             'Descrizione') is not None else '',
            #         error.find('Suggerimento').text if error.find(
            #             'Suggerimento') is not None else ''
            #     )
            return {
                'state': 'sender_error',
                # 'last_sdi_response': 'SdI ID: {}; '
                #                      'Message ID: {}; Receipt date: {}; '
                #                      'Error: {}'.format(
                #     id_sdi, message_id, receipt_dt, error_str)
            }
        # not implemented - todo
        elif message_type == 'MC':  # 3A. Mancata consegna
            # missed_delivery_note = root.find('Descrizione').text
            return {
                'state': 'recipient_error',
                # 'last_sdi_response': 'SdI ID: {}; '
                #                      'Message ID: {}; Receipt date: {}; '
                #                      'Missed delivery note: {}'.format(
                #     id_sdi, message_id, receipt_dt,
                #     missed_delivery_note)
            }
        elif message_type == 'RC':  # 3B. Ricevuta di Consegna
            # delivery_dt = root.find('DataOraConsegna').text
            return {
                'state': 'validated',
                # 'delivered_date': fields.Datetime.now(),
                # 'last_sdi_response': 'SdI ID: {}; '
                #                      'Message ID: {}; Receipt date: {}; '
                #                      'Delivery date: {}'.format(
                #     id_sdi, message_id, receipt_dt, delivery_dt)
            }
        # not implemented - todo
        elif message_type == 'NE':  # 4A. Notifica Esito per PA
            # esito_committente = root.find('EsitoCommittente')
            # if esito_committente is not None:
            #     # more than one esito?
            #     esito = esito_committente.find('Esito')
            #     if esito is not None:
            #         if esito.text == 'EC01':
            #             state = 'accepted'
            #         elif esito.text == 'EC02':
            #             state = 'rejected'
            return {
                'state': 'NE',
                # 'last_sdi_response': 'SdI ID: {}; '
                #                      'Message ID: {}; Response: {}; '.format(
                #     id_sdi, message_id, esito.text)
            }
        elif message_type == 'NE_ACCETTAZIONE':
            return {
                'state': 'accepted'
            }
        elif message_type == 'NE_RIFIUTO':
            return {
                'state': 'rejected'
            }
        # not implemented - todo
        elif message_type == 'DT':  # 5. Decorrenza Termini per PA
            # description = root.find('Descrizione')
            # if description is not None:
                return {
                    'state': 'validated',
                    # 'last_sdi_response': 'SdI ID: {}; '
                    #                      'Message ID: {}; Receipt date: {}; '
                    #                      'Description: {}'.format(
                    #     id_sdi, message_id, receipt_dt,
                    #     description.text)
                }
        # not implemented - todo
        elif message_type == 'AT':  # 6. Avvenuta Trasmissione per PA
            # description = root.find('Descrizione')
            # if description is not None:
            return {
                'state': 'accepted',
                # 'last_sdi_response': (
                #     'SdI ID: {}; Message ID: {}; Receipt date: {};'
                #     ' Description: {}'
                # ).format(
                #     id_sdi, message_id, receipt_dt,
                #     description.text)
            }
