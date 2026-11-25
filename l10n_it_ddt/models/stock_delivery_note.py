# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from collections import OrderedDict

from odoo import models


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    def _get_ddt_invoicing_group(self):
        """Return the invoicing group method of this delivery note.

        The sale order setting wins; without sale order the partner setting is used.
        """
        self.ensure_one()
        order = self.sale_ids[:1]
        if order:
            return order.ddt_invoicing_group or "billing_partner"
        partner = self.partner_shipping_id or self.partner_id
        return partner.commercial_partner_id.ddt_invoicing_group or "billing_partner"

    def _get_ddt_invoicing_key(self):
        """Return the key delivery notes must share to end up in the same invoice.

        The standard invoicing already splits by invoice partner, currency, fiscal
        position and payment term: the key adds only the extra splitting.
        """
        self.ensure_one()
        method = self._get_ddt_invoicing_group()
        if method == "nothing":
            return (method, self.id)
        if method == "shipping_partner":
            return (method, self.partner_shipping_id.id)
        if method == "sale_order":
            return (method, tuple(sorted(self.sale_ids.ids)))
        if method == "code_group":
            code = self.partner_shipping_id.ddt_code_group
            # Without code the shipping partner is its own group
            return (method, code or "id:%s" % self.partner_shipping_id.id)
        return (method,)

    def action_invoice(self, invoice_method=False):
        groups = OrderedDict()
        for note in self:
            key = note._get_ddt_invoicing_key()
            groups[key] = groups.get(key, self.browse()) | note
        if len(groups) <= 1:
            return super().action_invoice(invoice_method)
        # Check all notes before creating anything, to avoid partial results
        self._check_delivery_notes_before_invoicing()
        for notes in groups.values():
            super(StockDeliveryNote, notes).action_invoice(invoice_method)
        return True
