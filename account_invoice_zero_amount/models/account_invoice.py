# Copyright 2020
#
# Copyright 2021-2022 LibrERP enterprise network <https://www.librerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import models, _
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = 'account.invoice'

    def inherit_action_invoice_open(self):
        """ Overridden.
        Now we can also check amount between lines
        """
        total = 0.0
        for line in self.invoice_line_ids:
            total += line.price_subtotal
        if self.currency_id.is_zero(total):
            # if not total:
            return {
                'name': 'Conferma l\'inserimento della fattura '
                        'con importo a zero?',
                'type': 'ir.actions.act_window',
                'res_model': 'wizard.confirm.zero.amount',
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
            }

        if self.type in ('out_invoice', 'out_refund'):
            for tax_line in self.tax_line_ids:
                precision = self.currency_id.decimal_places
                calculated_amount = round(tax_line.base * tax_line.tax_id.amount / 100, precision)
                # if calculated_amount != round(tax_line.amount, precision):
                if abs(calculated_amount - tax_line.amount) > 0.007:
                    raise Warning(f"Il valore calcolato della tassa non coincide: {calculated_amount} vs {tax_line.amount}")

        return super(AccountInvoice, self).action_invoice_open()
