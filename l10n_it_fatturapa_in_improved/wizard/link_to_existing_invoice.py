# © 2021 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api


class WizardImportFatturapa(models.TransientModel):
    _inherit = 'wizard.link.to.invoice.line'

    @api.multi
    def link(self):
        if self.invoice_id.rc_self_invoice_id:
            if self.invoice_id.rc_self_invoice_id.fiscal_document_type_id:
                fdt = self.invoice_id.rc_self_invoice_id.fiscal_document_type_id
                code = fdt.code
                if code in ('TD17', 'TD18', 'TD19'):
                    self = self.with_context({
                        'autofattura': True,
                    })
        self.invoice_id.e_invoice_received_date = self.wizard_id.attachment_id.e_invoice_received_date.date()
        result = super().link()
        return result
