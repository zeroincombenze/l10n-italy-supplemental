# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools.misc import formatLang
from odoo.tools.translate import _
from odoo.exceptions import Warning as UserError

import time


class ReportRegistroIva(models.AbstractModel):
    _inherit = 'report.l10n_it_vat_registries.report_registro_iva'
    _description = 'Report VAT registry'

    @api.model
    def _get_report_values(self, docids, data=None):
        # docids required by caller but not used
        # see addons/account/report/account_balance.py
        docargs = super()._get_report_values(docids, data)
        docargs.update({
            'number_ref': self._set_move_line_ref
        })
        return docargs

    def _set_move_line_ref(self, line):
        reference = line['move_rec'].name
        if line['move_rec'].type in ('in_invoice', 'in_refund'):
            reference = line['reference'].split(',')[0]
            # fattura RC si prende l'autofattura
            if line['invoice_rec'] and line['invoice_rec'].rc_self_invoice_id:
                inv = line['invoice_rec'].rc_self_invoice_id
                reference += ' Integr. Autofat. '
                reference += inv.number
                reference += ' del ' + str(
                    inv.date_invoice.strftime('%d-%m-%Y'))

        elif line['move_rec'].type in ('out_invoice', 'out_refund'):
            # autofattura si prende il documento origine
            if line['invoice_rec'] and line[
                'invoice_rec'].rc_purchase_invoice_id:
                inv = line['invoice_rec'].rc_purchase_invoice_id
                reference += ' Fatt. Orig. '
                reference += inv.number
                reference += ' del ' + str(
                    inv.date_invoice.strftime('%d-%m-%Y'))

        return reference

