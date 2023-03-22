#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import api, fields, models

TYPE_2_MOVE_TYPE = {
    'entry': 'other',
    'out_invoice': 'receivable',
    'out_refund': 'receivable_refund',
    'in_invoice': 'payable',
    'in_refund': 'payable_refund',
}
MOVE_TYPE_2_TYPE = {
    'other': 'entry',
    'liquidity': 'entry',
    'receivable': 'out_invoice',
    'receivable_refund': 'out_refund',
    'payable': 'in_invoice',
    'payable_refund': 'in_refund',
}


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _get_default_invoice_date(self):
        return (
            fields.Date.today()
            if self._context.get('default_type', 'entry')
            in ('in_invoice', 'in_refund', 'in_receipt')
            else False
        )

    @api.model
    def _cvt_type2move_type(self, type):
        return TYPE_2_MOVE_TYPE[type]

    @api.model
    def _cvt_move_type2type(self, move_type):
        return MOVE_TYPE_2_TYPE[move_type]

    @api.multi
    @api.depends('line_ids')
    def count_line_ids(self):
        for rec in self:
            rec.lines_count = len(rec.line_ids)
        # end for
    # end def

    # Naming of 13.0 differs from account.invoice.date_invoice
    invoice_date = fields.Date(
        string='Invoice Date',
        readonly=True,
        index=True,
        copy=False,
        states={'draft': [('readonly', False)]},
        default=_get_default_invoice_date,
        help="Keep empty to use the current date",
    )
    # This is the field name and values for Odoo 14+
    # This field replaces old "type" field
    move_type = fields.Selection(
        [
            ('other', 'Other'),
            ('liquidity', 'Liquidity'),
            ('receivable', 'Receivable'),
            ('receivable_refund', 'Receivable refund'),
            ('payable', 'Payable'),
            ('payable_refund', 'Payable refund'),
        ],
        string='Entry type',
        readonly=True,
        states={'draft': [('readonly', False)]},
        index=True,
        change_default=True,
        default=lambda self: self._context.get('move_type', 'other'),
        track_visibility='always',
        required=True,
    )
    # This is the field name and the values for Odoo 13-
    # This field is for compatibility with old Odoo version
    type = fields.Selection(
        [
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            # ('out_receipt', 'Sales Receipt'),
            # ('in_receipt', 'Purchase Receipt'),
        ],
        string='Deprecated',
        readonly=True,
        states={'draft': [('readonly', False)]},
        index=True,
        change_default=True,
        default='entry',
        track_visibility='always',
        required=True,
    )
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position',
        string='Fiscal Position',
        readonly=True,
        states={'draft': [('readonly', False)]},
        domain="[('company_id', '=', company_id)]",
        help="Fiscal positions are used to adapt taxes and accounts for "
        "particular customers or sales orders/invoices. "
        "The default value comes from the customer.",
    )

    lines_count = fields.Integer(compute='count_line_ids')

    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Payment Term',
        oldname='payment_id',
    )

    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Bank Account',
        help=(
            'Bank Account Number to which the invoice will be paid. '
            'A Company bank account if this is a Customer Invoice or '
            'Vendor Credit Note, otherwise a Partner bank account number.'
        ),
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    @api.multi
    def post(self, invoice=False):
        if invoice:
            for move in self:
                for field in ('type',):
                    move[field] = getattr(invoice, field)
                move.move_type = move._cvt_type2move_type(invoice.type)
                move.invoice_date = invoice.date_invoice
                for field in ('payment_term_id',
                              'fiscal_position_id',
                              'partner_bank_id'):
                    move[field] = getattr(invoice, field)
        return super().post(invoice=invoice)

    @api.model
    def create(self, values):
        if values.get('type') and not values.get('move_type'):
            values['move_type'] = self._cvt_type2move_type(values['type'])
        elif not values.get('type') and values.get('move_type'):
            values['type'] = self._cvt_move_type2type(values['move_type'])
        return super().create(values)

    @api.multi
    def write(self, values):
        if values.get('type') and not values.get('move_type'):
            values['move_type'] = self._cvt_type2move_type(values['type'])
        elif not values.get('type') and values.get('move_type'):
            values['type'] = self._cvt_move_type2type(values['move_type'])
        return super().write(values)
