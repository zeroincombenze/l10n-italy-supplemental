# Copyright 2020-23 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-23 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-23 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import models, api
from odoo.exceptions import UserError
from .open_items import OpenItems


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def registra_insoluto(self):
        # The payment method of the payment order
        p_method = self.get_payment_method()

        if p_method.code == "riba_cbi":
            self.registra_insoluto_standard()
        else:
            super().registra_insoluto()
        # end if

    # end registra_insoluto

    @api.multi
    def registra_incasso(self):
        # Checks that all the lines have the same
        # payment method and returns it
        p_method = self.get_payment_method()

        if p_method.code == "riba_cbi":
            self._registra_incasso_riba()
        else:
            super().registra_incasso()
        # end if

    # end registra_incasso

    @api.multi
    def _registra_incasso_riba(self):
        open_items = OpenItems()
        for move_line in self:
            open_items.add_move_line(move_line)

        vals = open_items.load_move_vals()
        if vals:
            settlement_move = self.env["account.move"].create(vals)
            open_items.couple_settlement(settlement_move)
            # settlement_move.post()
        open_items.do_reconciles()
        self.write({"incasso_effettuato": True})

    # end _registra_incasso_riba

    def prepare_1_move_line(self, account_id, side, amount=None):
        """Prepare account move line value"""
        if side not in ("debit", "credit"):
            raise UserError("Invalid %s value: must be 'debit' or 'credit'" % side)

        opposite_side = "debit" if side == "credit" else "credit"
        amount_db_cr = amount or self.amount_into_payment_line
        if amount_db_cr < 0.0:
            values = {
                "account_id": account_id,
                side: 0.0,
                opposite_side: -amount_db_cr,
            }
        else:
            values = {
                "account_id": account_id,
                side: amount_db_cr,
                opposite_side: 0.0,
            }
        if amount:
            payments = []
            for line in self:
                for payment_line in line.payment_line_ids:
                    if payment_line.order_id not in payments:
                        payments.append(payment_line.order_id)
            if payments:
                values["name"] = "Distinta scadenze %s" % ",".join(
                    [x.name for x in payments]
                )
        else:
            values["name"] = f"Fattura {self.move_id.name}"
            # Le tre righe seguenti sono state commentate perchè
            # causano comportamenti anomali.
            # La modifica è state fatta in accordo con Antonio Vigliotti in video call
            # values["payment_line_ids"] = [
            #     (6, 0, [x.id for x in self.payment_line_ids])
            # ]
        if not amount:
            values["partner_id"] = self.partner_id.id
        return values
