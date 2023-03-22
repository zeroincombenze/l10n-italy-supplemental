# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import datetime
import logging
from zeep import Client, Settings
from zeep.transports import Transport
from requests import Session
from datetime import timedelta

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class Config:
    document_host = ''
    useralias = ''
    password = ''


class Invoice2C(object):
    def __init__(self, config):
        super().__init__()

        session = Session()
        session.verify = False
        transport = Transport(session=session)
        settings = Settings(strict=False)

        self.client = Client(config.document_host, transport=transport, settings=settings)
        self.useralias = config.useralias
        self.password = bytearray(config.password, 'utf-8')

    # def get_sending_result(self, idsdi=None, filename=None):
    #     """
    #     Esito invio FatturaPA. Interroga 2C per conoscere l'esito dell'invio fattura
    #     :param idsdi: identificativo assegnato da SdI
    #     :return: codice esito SdI/2C
    #     """
    #
    #     filter_params = {'DataFullOutcomes': True}
    #
    #     if idsdi:
    #         if idsdi.isdigit():
    #             filter_params['IdSdi'] = idsdi
    #         else:
    #             _logger.error('Wrong ID Sdi: "{}"'.format(idsdi))
    #             return
    #     if filename:
    #         filter_params['FilenameInvoice'] = filename
    #
    #     ret_esito = self.client.service.GetElectronicInvoiceOutcomes(   # Nuova API
    #         paramAuth=dict(
    #             CustomerCode=self.useralias,
    #             Password=self.password,
    #         ),
    #         # paramFilter=dict(
    #         #     # IdInvoice='',
    #         #     IdSdi=idsdi,
    #         #     # FilenameInvoice='',
    #         #     # StatusLegalStorage='Conservato',   # Sconosciuto or DaConservare or VersatoPdV or VersatoRdV or Conservato
    #         #     DataFullOutcomes=True,
    #         # )
    #         paramFilter=filter_params
    #     )
    #     return ret_esito

    def search_invoices(self, date_start):
        result = self.client.service.GetElectronicInvoices(
            paramAuth=dict(
                CustomerCode=self.useralias,
                Password=self.password,
            ),
            paramFilter=dict(
                DateStart=date_start,
                # DateEnd=date_end,
                # FilenameZip
                # FilenameInvoice='xxx',
                DataCustomerServicesConsumption=False,
                DataFullInvoices=True
            )
        )

        return result['ElectronicInvoices']['ElectronicInvoice']


if __name__ == '__main__':
    config = Config()
    config.document_host = 'https://hubfe.solutiondocondemand.com/SolutionDOC_Hub.asmx?wsdl'
    config.useralias = '<user>'
    config.password = '<password>'

    service2c = Invoice2C(config)

    today = datetime.datetime.now()
    delta = timedelta(days=1)
    date_start = today - delta
    # date_end = today + delta

    result = service2c.search_invoices(date_start=date_start)
    # result = service2c.get_sending_result(idsdi='xxx')

    print(result)
