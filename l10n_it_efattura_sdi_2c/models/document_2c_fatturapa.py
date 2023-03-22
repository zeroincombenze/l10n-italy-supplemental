# -*- coding: utf-8 -*-
# © 2018 Nicola Gramola - Didotech srl (www.didotech.com)
# © 2019-2021 Andrei Levin - Didotech srl (www.didotech.com)

from io import BytesIO
import logging

from odoo.addons.l10n_it_efattura_sdi.models.sdi_lib import ActiveInvoice
from requests import Session
from datetime import timedelta

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

try:
    from zeep import Client, Settings
    from zeep.transports import Transport

    import logging.config
    import zipfile

except (ImportError, IOError) as err:
    _logger.debug(err)


class ActiveInvoice_2C(ActiveInvoice):
    def __init__(self, config, dry_run=False):
        super(ActiveInvoice_2C, self).__init__(config, dry_run)

        session = Session()
        session.verify = False
        transport = Transport(session=session)
        settings = Settings(strict=False)

        if self.node == self.my_node:
            self.client = Client(config.document_host, transport=transport, settings=settings)
        else:
            self.client = False
            _logger.error("Can't access remote host because of my node configuration")

        self._upload_filename = None

        self.dry_run = dry_run
        self.logger = logging.getLogger(__name__)

    def upload_data(self, document_name, data, dry_run=False):
        """
        Carica fatturaPa in 2C
        :param document_name: nome del file da inviare in formata fatturaPA
        :param data: contenuto del file fatturaPA XML
        :param dry_run: non usato
        :return: nome del file assegnato da 2C
        """
        if self._upload_filename:
            # TODO controllare se inviato prima di upload
            return None

        if self.node == self.my_node:
            # STEP 1: get file name to upload fatturapa
            self._upload_filename = self.client.service.GetNomeFileZipFatturaPA(
                codiceCliente=self.useralias,
                passwordServizi=self.password
            )

            # STEP 1.1: setup zip file
            archive = BytesIO()
            zf = zipfile.ZipFile(archive, mode='w')
            zf.writestr(document_name, data)
            zf.close()

            # STEP 2:
            archive.seek(0)
            ret_remote_filename = self.client.service.UploadFileFatturaPA(
                codiceCliente=self.useralias,
                passwordServizi=self.password,
                nomeFile=self._upload_filename,
                buffer=archive.read(),  # zeep fa la conversione in base64 automaticamente
                offset=0
            )

            return ret_remote_filename
        else:
            _logger.error("Can't send file because my node configuration is different")
            return False

    def send_invoice(self, email=False):
        """
        Invio fattura precaricata a SdI
        :param email: Lista indirizzi e-Mail a cui recapitare la fattura elettronica
        :return: esito dell'invio lista di identificativo sdi e data ora invio
                 oppure un errore
        """
        if self._upload_filename:
            # STEP 3: send to SDI

            # New API
            # Attention! ret_invio format is different!!!!
            ret_invio = self.client.service.SendElectronicInvoice(
                paramAuth=dict(
                    CustomerCode=self.useralias,
                    Password=self.password,
                ),
                paramInvoice=dict(
                    Filename=self._upload_filename,
                    ToSign=True,
                    Proforma=False,
                    paramEmail=dict(
                        Send=email and True or False,
                        Address=email
                    )
                )
            )

            return ret_invio
        else:
            return None

    def get_log_invoice(self, idsdi=None, filename_2c=None, from_date=None, to_date=None):
        params = {
            'codiceCliente': self.useralias,
            'passwordServizi': self.password,
        }

        if idsdi:
            params['identificativoSdi'] = idsdi
        if filename_2c:
            params['nomeFileZip'] = filename_2c
        if from_date:
            params['Data_Da'] = from_date
        if to_date:
            params['Data_A'] = to_date

        ret_fatturapa = self.client.service.GetLogFatturaPA(**params)

        return ret_fatturapa

    def get_invoice(self, idsdi, estrazioneP7M=True):
        """
        Recupera il file XML della fattura precedentemente inviata
        :param idsdi: identificativo assegnato da SdI
        :param estrazioneP7M:
        :return: fatturaPA XML codificata in Base 64
        """

        if self.client and idsdi.isdigit():
            ret_fatturapa = self.client.service.GetFileElectronicInvoice(   # Nuove API
                paramAuth=dict(
                    CustomerCode=self.useralias,
                    Password=self.password,
                ),
                paramFileInvoice=dict(
                    IdSdi=idsdi,
                    ExtractionP7M=True,
                )
            )

            if ret_fatturapa['ResultCode'] == 'Success':
                datas = ret_fatturapa['File'].decode('utf-8-sig').encode('utf-8')
                return datas.encode('base64')
            else:
                return None
        else:
            return None

    def get_sending_result(self, idsdi):
        """
        Esito invio FatturaPA. Interroga 2C per conoscere l'esito dell'invio fattura
        :param idsdi: identificativo assegnato da SdI
        :return: codice esito SdI/2C
        """

        if idsdi.isdigit():
            ret_esito = self.client.service.GetElectronicInvoiceOutcomes(   # Nuova API
                paramAuth=dict(
                    CustomerCode=self.useralias,
                    Password=self.password,
                ),
                paramFilter=dict(
                    # IdInvoice='',
                    IdSdi=idsdi,
                    # FilenameInvoice='',
                    # StatusLegalStorage='Conservato',   # Sconosciuto or DaConservare or VersatoPdV or VersatoRdV or Conservato
                    DataFullOutcomes=True,
                )
            )
            return ret_esito
        else:
            _logger.error('Wrong ID Sdi: "{}"'.format(idsdi))
            return

    def send_email(self, id_sdi, email):
        return self.client.service.SendEmail(
            paramAuth=dict(
                CustomerCode=self.useralias,
                Password=self.password,
            ),
            paramEmail=dict(
                IdSdi=id_sdi,
                Send=email and True or False,
                Address=email
            )
        )

    def search_invoices(self, date_start):
        result = self.client.service.GetElectronicInvoices(
            paramAuth=dict(
                CustomerCode=self.useralias,
                Password=self.password,
            ),
            paramFilter=dict(
                DateStart=date_start,
                # DateEnd=date_end,
                DataCustomerServicesConsumption=False,
                DataFullInvoices=True
            )
        )

        return result['ElectronicInvoices']['ElectronicInvoice']


class PassiveInvoice_2C(object):
    def __init__(self, config, dry_run=False):
        self.useralias = config.document_username
        self.password = bytearray(config.document_password, 'utf-8')

        session = Session()
        session.verify = False
        transport = Transport(session=session)
        settings = Settings(strict=False)
        self.client = Client(config.document_host, transport=transport, settings=settings)

        self._upload_filename = None

        self.dry_run = dry_run
        self.logger = logging.getLogger(__name__)

    def list(self, filter=False):
        """
        :param filter (dict):
            DataFine: xsd:dateTime,
            DataInizio: xsd:dateTime,
            NumeroProtocollo: xsd:string,
            DataProtocolloInizio: xsd:dateTime,
            DataProtocolloFine: xsd:dateTime,
            StatoProtocollo: {http://2csolution.it/FatturaPassivaPA/DTO/V1.0}StatoProtocolloEnum,
            NumeroRegistrazione: xsd:string,
            DataRegistrazioneInizio: xsd:dateTime,
            DataRegistrazioneFine: xsd:dateTime,
            StatoRegistrazione: {http://2csolution.it/FatturaPassivaPA/DTO/V1.0}StatoRegistrazioneEnum`
            Sezionale: xsd:string,
            StatoArchiviazione: {http://2csolution.it/FatturaPassivaPA/DTO/V1.0}StatoArchiviazioneEnum,
            StatoEsiti: {http://2csolution.it/FatturaPassivaPA/DTO/V1.0}StatoEsitiEnum

        """
        if filter:
            return self.client.service.GetFattureParam(
                codiceCliente=self.useralias,
                passwordServizi=self.password,
                request=filter
            )
        else:
            return self.client.service.GetFatture(
                codiceCliente=self.useralias,
                passwordServizi=self.password
            )

    def get(self, invoice_codes):
        office_code, sdi_id = invoice_codes
        return self.client.service.GetFatturaDisinbustata(
            codiceCliente=self.useralias,
            passwordServizi=self.password,
            codiceUfficio=office_code,
            idSdi=sdi_id
        )

    def get_list(self, invoice_list):
        return map(self.get, invoice_list)

    def get_invoices(self, filter=False):
        invoice_info_list = self.list(filter)

        invoice_list = [(invoice.CodiceUfficio, invoice.IdSdi) for invoice in invoice_info_list]

        return self.get_list(invoice_list)
