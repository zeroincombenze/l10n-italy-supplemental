
from odoo import api, fields, models, _


class SaleConfiguration(models.TransientModel):
    _inherit = 'sale.config.settings'

    state = fields.Selection(
        [
            ('draft', 'RFQ'),
            ('sent', 'RFQ Sent'),
            ('to approve', 'To Approve'),
            ('purchase', 'Purchase Order'),
        ],
        string="Default PO State",
        help="Create Purchase Order will be put to selected state.",
        default='draft',
        required=True,
    )
    draft_allow_convert = fields.Boolean(
        "Allow convert Quotation",
        default=False,
        help="If checked Quotation state will have `Convert to Purchase Order` button.",
    )
    sent_allow_convert = fields.Boolean(
        "Allow convert Quotation Sent",
        default=False,
        help="If checked Quotation Sent state will have `Convert to Purchase Order` button.",
    )
    sale_allow_convert = fields.Boolean(
        "Allow convert Sales Order",
        default=False,
        help="If checked Sales Order state will have `Convert to Purchase Order` button.",
    )
    po_name_with_so_ref = fields.Boolean(
        "PO number with SO number suffix",
        default=False,
        help="If checked created PO number has SO number suffix.",
    )

    @api.multi
    def set_default_state(self):
        return self.env['ir.values'].set_default(
            'sale.config.settings', 'state', self.state)

    @api.multi
    def set_default_draft_allow_convert(self):
        return self.env['ir.values'].set_default(
            'sale.config.settings', 'draft_allow_convert', self.draft_allow_convert)   

    @api.multi
    def set_default_sent_allow_convert(self):
        return self.env['ir.values'].set_default(
            'sale.config.settings', 'sent_allow_convert', self.sent_allow_convert)   

    @api.multi
    def set_default_sale_allow_convert(self):
        return self.env['ir.values'].set_default(
            'sale.config.settings', 'sale_allow_convert', self.sale_allow_convert)

    @api.multi
    def set_default_po_name_with_so_ref(self):
        return self.env['ir.values'].set_default(
            'sale.config.settings', 'po_name_with_so_ref', self.po_name_with_so_ref)

    @api.multi
    def set_default_copy_sale_price(self):
        return self.env['ir.values'].set_default(
            'sale.config.settings', 'copy_sale_price', self.copy_sale_price)
