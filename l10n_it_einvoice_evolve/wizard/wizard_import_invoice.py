
from odoo import models
from odoo.tools.translate import _
import logging

logger = logging.getLogger(__name__)


class WizardImportInvoice(models.TransientModel):
    _inherit = "wizard.import.passive.invoice"

    def import_sdi_invoice(self):
        # company = self.env['res.users'].browse(self.env.uid).company_id
        return {
            "type": "ir.actions.act_window",
            "name": _("Vendor Bills"),
            "res_model": "fatturapa.attachment.in",
            "view_type": "form",
            "view_mode": "tree,form",
            "target": "main",
            # 'domain': [('id', 'in', xml_ids)]
        }
