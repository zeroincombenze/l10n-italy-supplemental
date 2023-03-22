# © 2018-2022 Andrei Levin - Didotech srl (www.didotech.com)

from odoo.addons.l10n_it_efattura_sdi_2c.models.document_2c_fatturapa import PassiveInvoice_2C  # pylint: disable=W7950
from odoo.addons.l10n_it_efattura_sdi.models.sdi_lib import SimpleConfig
from odoo import models, exceptions
from odoo.tools.translate import _
import logging
import base64

logger = logging.getLogger(__name__)


class WizardImportInvoice(models.TransientModel):
    _inherit = "wizard.import.passive.invoice"

    def import_sdi_invoice(self):
        company = self.env['res.users'].browse(self.env.uid).company_id
        config = SimpleConfig(company)
        config.document_host = self.env.get('ir.config_parameter').get_param(
            'sdi_passive_host')

        # invoice_to_recalculate_ids = invoice_in_obj.search([('xml_supplier_id', '=', False)])
        # if invoice_to_recalculate_ids:
        #     invoice_in_obj.dummy_button(invoice_to_recalculate_ids)

        if config.document_host:
            invoice = PassiveInvoice_2C(config)
            # I should set last xml date here from view
            date_from_wizard = self.start_import_date

            if date_from_wizard:
                invoices = invoice.get_invoices({
                    'DataInizio': date_from_wizard
                })
            else:
                invoices = invoice.get_invoices({
                    'DataInizio': self.get_last_download_date()
                })

            xml_ids = []

            for invoice in invoices:
                values = {
                    'datas': base64.b64encode(invoice.FileFattura),
                    'datas_fname': invoice.DatiFattura.NomeFile,
                    'name': invoice.DatiFattura.NomeFile,
                    'sdi_id': invoice.DatiFattura.IdSdi,
                    'sdi_date': invoice.DatiFattura.DataSdi,
                    'e_invoice_received_date': invoice.DatiFattura.DataSdi,
                    'office_code': invoice.DatiFattura.CodiceUfficio
                }

                if self.env["fatturapa.attachment.in"].search_read([(
                        'name', '=', values['name'])], ['id']):
                    logger.info(f"{values['name']}: Invoice already imported")
                elif self.env["fatturapa.attachment.in"].search_read([
                    ('name', '=', str(values['sdi_id']) + '_' + values['name'])
                ], ['id']):
                    logger.info(u'{}: Invoice already imported (2)'.format(
                        str(values['sdi_id']) + '_' + values['name']))
                elif self.env["fatturapa.attachment.in"].search_read(
                        [('name', 'like', values['name'][:-4])], ['id']):
                    logger.info(
                        f"{values['name']}: Invoice already imported (3)")
                else:
                    logger.info('Importing {} ...'.format(values['name']))
                    xml = self.env["fatturapa.attachment.in"].create(values)
                    xml_ids.append(xml.id)

            return {
                'type': 'ir.actions.act_window',
                'name': _('Vendor Bills'),
                'res_model': 'fatturapa.attachment.in',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'target': 'main',
                'domain': [('id', 'in', xml_ids)]
            }
        else:
            raise exceptions.Warning(_('Please set destination host (sdi_passive_host) for passive invoice'))
