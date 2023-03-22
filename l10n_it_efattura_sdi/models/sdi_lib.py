# -*- coding: utf-8 -*-
# © 2020 Andrei Levin - Didotech srl (www.didotech.com)


class SimpleConfig:
    def __init__(self, company):
        self.document_username = company.sdi_username
        self.document_password = company.sdi_password or ''
        self.extract_from_p7m = True if company.sdi_storage_format == 'xml' else False
        self.node = company.sdi_node
        self.my_node = company.node
        self.use_local_storage = company.use_local_storage


class ActiveInvoice:
    def __init__(self, config, dry_run=False):
        self.useralias = config.document_username
        self.password = bytearray(config.document_password, 'utf-8')
        self.node = config.node
        self.my_node = config.my_node

    def upload_data(self, document_name, data, dry_run=False):
        pass

    def send_invoice(self, email=False):
        """
        Invio fattura precaricata a SdI
        :param email: Lista indirizzi e-Mail a cui recapitare la fattura elettronica
        :return: esito dell'invio lista di identificativo sdi e data ora invio
                 oppure un errore
        """
        pass

    def get_log_invoice(self, sdi_id=None, sdi_filename=None, from_date=None, to_date=None):
        pass

    def get_invoice(self, sdi_id, estrazioneP7M=True):
        """
        Recupera il file XML della fattura precedentemente inviata
        :param idsdi: identificativo assegnato da SdI
        :param estrazioneP7M:
        :return: fatturaPA XML codificata in Base 64
        """
        pass

    def get_sending_result(self, sdi_id):
        """
        Esito invio FatturaPA. Interroga 2C per conoscere l'esito dell'invio fattura
        :param idsdi: identificativo assegnato da SdI
        :return: codice esito SdI/2C
        """
        pass

    def send_email(self, sdi_id, email):
        pass

    def upload_invoice(self, invoice_out, doucment_host, config):
        pass

    def _hook_after_sent(self, fatturapa_attachment_out):
        return True

    def update_status(self):
        pass


class PassiveInvoice:
    pass
