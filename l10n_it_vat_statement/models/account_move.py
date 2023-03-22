# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from datetime import timedelta
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    date_apply_vat = fields.Date(
        string='Data applicazione IVA',
    )

    # @api.constrains('date_apply_vat')
    # def _constraint_date_apply_vat(self):
    #     for move in self:
    #         min_date = move.mindate_apply_vat()
    #         if min_date and move.date_apply_vat < min_date:
    #             raise Warning(
    #                 'Data applicazione IVA antecedente data fattura')

    @api.onchange('date')
    def _onchange_date(self):
        if self.date:
            self.date_apply_vat = self.date

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

    # @api.model
    # def mindate_apply_vat(self):
    #     if self.date_apply_vat and self.date:
    #         min_date = self.date - timedelta(days=31)
    #         if self.date_apply_vat < min_date:
    #             return min_date
    #     return False

    @api.multi
    def post(self, invoice=False):
        for move in self:
            if invoice:
                move.date_apply_vat = invoice.date_apply_vat
                if not move.date_apply_vat:
                    move.date_apply_vat = move.date
        return super().post(invoice=invoice)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    date_apply_vat = fields.Date(
        string='Data applicazione IVA',
        related='move_id.date_apply_vat',
        stored=True,
    )
