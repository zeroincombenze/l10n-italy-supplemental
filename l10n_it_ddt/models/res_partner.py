# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

DDT_INVOICING_GROUPS = [
    ("nothing", "One DDT - One Invoice"),
    ("billing_partner", "Billing Partner"),
    ("shipping_partner", "Shipping Partner"),
    ("sale_order", "By Sale Order"),
    ("code_group", "Code group"),
]


class ResPartner(models.Model):
    _inherit = "res.partner"

    ddt_invoicing_group = fields.Selection(
        DDT_INVOICING_GROUPS,
        string="DDT invoicing group",
        default="billing_partner",
        help="How the delivery notes of this customer are grouped into invoices.",
    )
    ddt_code_group = fields.Char(
        string="DDT code group",
        help="Delivery notes shipped to partners with the same code (and the same "
        "billing partner) are invoiced together when the invoicing group is "
        "'Code group'.",
    )
