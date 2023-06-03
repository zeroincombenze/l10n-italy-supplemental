# Copyright 2017-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class WizardPaymentOrderCloseFinancing(models.TransientModel):
    _name = 'wizard.payment.order.close.financing'

    def _set_default_mode(self):

        payment_order = self.env['account.payment.order'].browse(
            self._context.get('active_id'))

        if payment_order and payment_order.id:
            cfg = payment_order.get_move_config()
            if 'bank_expense_account_id' in cfg and cfg['bank_expense_account_id'].id:
                return cfg['bank_expense_account_id'].id
        return False

    account_expense = fields.Many2one(
        'account.account',
        string='Conto spese',
        domain=[(
            'internal_group', '=', 'expense')],
        default=_set_default_mode
    )

    amount_expense = fields.Float(string='Importo', )

    @api.multi
    def chiudi_anticipo(self):
        '''Create on new account.move for each line of payment order'''

        model = self.env['account.payment.order']
        recordset = model.browse(self._context['active_id'])
        recordset.with_context({
            'expenses_account_id': self.account_expense.id,
            'expenses_amount': self.amount_expense,
        }).chiudi_anticipo()

        return {'type': 'ir.actions.act_window_close'}

    # end apri_anticipo

# end AccountPaymentGenerate
