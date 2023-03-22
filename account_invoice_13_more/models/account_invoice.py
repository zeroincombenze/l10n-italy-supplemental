#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_move_create(self):
        super().action_move_create()
        for inv in self:

            updates = dict()
            for field in ('type',):
                updates[field] = getattr(inv, field)
            updates['invoice_date'] = inv.date_invoice
            for field in ('payment_term_id',
                          'fiscal_position_id',
                          'partner_bank_id'):
                if getattr(inv, field):
                    updates[field] = getattr(inv, field).id
                else:
                    updates[field] = False

            inv.move_id.write(updates)
        return True
