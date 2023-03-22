# © 2018-2022 Andrei Levin - Didotech srl (www.didotech.com)

import datetime
from odoo.addons.l10n_it_efattura_sdi.models.sdi_lib import SimpleConfig  # pylint: disable=W7950
from odoo import models, fields, exceptions
from odoo.tools import (DEFAULT_SERVER_DATETIME_FORMAT,
                        DEFAULT_SERVER_DATE_FORMAT)
from odoo.tools.translate import _
import logging

logger = logging.getLogger(__name__)


class WizardImportInvoice(models.TransientModel):
    _name = "wizard.import.passive.invoice"
    _description = 'Wizard Import Passive Invoice from SDI'

    def get_last_download_date(self):
        last_xmls = self.env['fatturapa.attachment.in'].search(
            [('sdi_date', '!=', False)],
            order='sdi_date desc', limit=1)

        if last_xmls:
            return last_xmls[0].sdi_date.date()
        else:
            return datetime.date.today()

    def get_default(self):
        invoice_in_obj = self.env['fatturapa.attachment.in']
        company = self.env['res.users'].browse(self.env.uid).company_id
        config = SimpleConfig(company)
        config.document_host = self.env['ir.config_parameter'].get_param(
            'sdi_passive_host')

        if config.document_host:
            # try to set as default last date
            last_xml_date_date = self.get_last_download_date().strftime(
                DEFAULT_SERVER_DATETIME_FORMAT)
        else:
            raise exceptions.Error(_('Please set destination host (sdi_passive_host) for passive invoice'))

        return last_xml_date_date

    def _get_dummy_name(self):
        self.name = '...'

    name = fields.Char(compute=_get_dummy_name, string='Name')
    start_import_date = fields.Date(
        'Data inizio importazione', required=True, default=get_default)

    def import_sdi_invoice(self):
        raise exceptions.Warning(_(
            'Please install specific module to access your SDI provider'))
