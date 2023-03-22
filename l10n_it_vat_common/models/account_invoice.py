# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    date_apply_vat = fields.Date(
        'Apply for VAT date',
        states={
            'paid': [('readonly', True)],
            'open': [('readonly', True)],
            'close': [('readonly', True)]
        },
        copy=False,
        help="Date to apply for VAT")

    @api.onchange('date')
    def _onchange_date(self):
        # res = super()._onchange_date()
        if self.date:
            self.date_apply_vat = self.date
        # end if
        # return res

    @api.onchange('date_apply_vat')
    def _onchange_date_apply_vat(self):
        res = {}
        warnings = ''
        if self.date and self.date_apply_vat:
            min_date_30 = self.date - timedelta(days=30)
            min_date_60 = self.date - timedelta(days=60)
            if self.date_apply_vat < min_date_60:
                warnings += '\nLa data di applicazione iva è minore di 60 ' \
                            'giorni dalla data di registrazione'

            elif self.date_apply_vat < min_date_30:
                warnings += '\nLa data di applicazione iva è minore di 30 ' \
                            'giorni dalla data di registrazione'
            # end if

            if self.type in ['out_invoice', 'out_refund']:
                if self.date_apply_vat != self.date:
                    warnings = '\nLa data di applicazione iva è diversa ' \
                               'dalla data di registrazione'
                # end if
            # end if

            if warnings:
                res['warning'] = {
                    'title': 'Attenzione!',
                    'message': warnings
                }
            # end if

        return res

    @api.multi
    def action_move_create(self):

        super().action_move_create()

        for inv in self:
            if not inv.date_apply_vat:
                inv.date_apply_vat = inv.date
            # end if
            if inv.fiscalyear_id and inv.fiscalyear_id.date_from \
                    and inv.fiscalyear_id.date_to:
                fy_name = inv.fiscalyear_id.name
                fy_from = inv.fiscalyear_id.date_from
                fy_to = inv.fiscalyear_id.date_to

                if not (fy_from <= inv.date_apply_vat <= fy_to):
                    raise UserError('Data applicazione iva non compresa '
                                    'nell\'esercizio contabile {fiscal}'.
                                    format(fiscal=fy_name))
                # end if
            # end if
        # end for

    @api.model
    def create(self, vals):
        if 'date_apply_vat' in vals and not vals['date_apply_vat']:
            vals['date_apply_vat'] = vals['date']
        # end if
        return super().create(vals)

    @api.multi
    def write(self, vals):
        if 'date_apply_vat' in vals and not vals['date_apply_vat']:
            vals['date_apply_vat'] = self.date
        # end if
        res = super().write(vals)
        return res
