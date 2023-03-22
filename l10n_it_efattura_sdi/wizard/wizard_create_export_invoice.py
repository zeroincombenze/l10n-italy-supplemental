# © 2018-2022 Andrei Levin - Didotech srl (www.didotech.com)

import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class WizardCreateExportInvoice(models.TransientModel):
    _name = "wizard.create.export.invoice"
    _description = "Wizard Export Invoice to SDI"

    def _get_journal_id(self):
        vals = []

        for jr_type in self.env['account.journal'].search(['|', ('type', '=', 'sale'), ('type', '=', 'sale_refund')]):
            t1 = jr_type.id, jr_type.name
            if t1 not in vals:
                vals.append(t1)
        return vals

    journal_id = fields.Selection(_get_journal_id, 'Destination Journal', required=True)
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    auto_approve = fields.Boolean('Group by Partner')

    def create_export_invoice_sdi(self):
        invoice_model = self.env['account.invoice']
        export_pa_model = self.env['wizard.export.fatturapa']
        wizard = self[0]

        invoices = invoice_model.search([
            ('journal_id', '=', int(wizard.journal_id)),
            ('fatturapa_attachment_out_id', '=', False),
            ('state', 'in',  ('open', 'paid')),
            ('date_invoice', '>=', wizard.date_from),
            ('date_invoice', '<=', wizard.date_to)
        ])
        if invoices:
            if wizard.auto_approve:
                # context['active_ids'] = invoices
                try:
                    export_pa_model.with_context({'active_ids': invoices}).exportFatturaPA([])
                except Exception as e:
                    _logger.error(e)
            else:
                total_length = len(invoices)
                for count, invoice_id in enumerate(invoices, start=1):
                    _logger.info('{} / {}'.format(count, total_length))
                    try:
                        export_pa_model.with_context({'active_ids': invoices}).exportFatturaPA([])
                    except Exception as e:
                        _logger.error(e)

        return {
            'type': 'ir.actions.act_window_close',
        }
