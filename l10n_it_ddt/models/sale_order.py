# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

from .res_partner import DDT_INVOICING_GROUPS


class SaleOrder(models.Model):
    _inherit = "sale.order"

    ddt_invoicing_group = fields.Selection(
        DDT_INVOICING_GROUPS,
        string="DDT invoicing group",
        compute="_compute_ddt_invoicing_group",
        store=True,
        readonly=False,
        precompute=True,
    )

    @api.depends("partner_invoice_id.commercial_partner_id.ddt_invoicing_group")
    def _compute_ddt_invoicing_group(self):
        for order in self:
            order.ddt_invoicing_group = (
                order.partner_invoice_id.commercial_partner_id.ddt_invoicing_group
                or "billing_partner"
            )
