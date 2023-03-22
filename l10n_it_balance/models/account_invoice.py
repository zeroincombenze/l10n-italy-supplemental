# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later
# (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps)
#
from datetime import timedelta
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    date_apply_balance = fields.Date(
        'Data competenza bilancio',
        states={
            'paid': [('readonly', True)],
            'open': [('readonly', True)],
            'close': [('readonly', True)]
        },
        help="Date to apply for balance sheet",
        copy=False
    )

    @api.onchange('date')
    def _onchange_date(self):
        res = super()._onchange_date()
        self.date_apply_balance = self.date
        return res
    # end _onchange_date

    @api.onchange('date_apply_balance')
    def _onchange_date_apply_balance(self):
        res = {}
        if self.date and self.date_apply_balance:
            min_date_plus_60 = self.date + timedelta(days=60)
            min_date_minus_60 = self.date - timedelta(days=60)
            if not (min_date_minus_60 <= self.date_apply_balance <=
                    min_date_plus_60):
                res['warning'] = {
                    'title': 'Attenzione!',
                    'message': 'Data di competenza bilancio fuori dai '
                               'limiti di + 60 e - 60 giorni'
                }
            # end if
        # end if
        return res
    # end _onchange_date_apply_balance

    @api.model
    def create(self, vals):
        if 'date' in vals and vals['date']:
            if 'date_apply_balance' in vals and not vals['date_apply_balance']:
                vals['date_apply_balance'] = vals['date']
            # end if
        # end if
        return super().create(vals)
    # end create

    @api.multi
    def write(self, vals):
        # Save vals
        super().write(vals)

        # Set default values, but avoid the "infinite
        # recursive calls to write" issue
        if not self.env.context.get('StopRecursion'):
            for invoice in self:
                invoice = invoice.with_context(StopRecursion=True)
                if invoice.date and not invoice.date_apply_balance:
                    invoice.date_apply_balance = invoice.date
                # end if
            # end for
        else:
            return
        # end if
    # end write

    @api.multi
    def action_move_create(self):
        for invoice in self:
            if not invoice.date_apply_balance:
                invoice.date_apply_balance = invoice.date
            # end if
        # edn for
        return super().action_move_create()
    # end action_move_create
