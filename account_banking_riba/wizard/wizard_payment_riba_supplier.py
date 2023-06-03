# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging
from odoo import models, api, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WizardPaymentRibaSupplier(models.TransientModel):
    _name = "wizard.payment.riba.supplier"

    def _set_default_expense_account_id(self):
        payment_order = self.env["account.payment.order"].browse(
            self._context.get("active_id")
        )

        cfg = payment_order.get_move_config()
        if "bank_expense_account_id" in cfg and cfg["bank_expense_account_id"].id:
            return cfg["bank_expense_account_id"].id
        return False

    account_expense = fields.Many2one(
        "account.account",
        string="Conto spese",
        domain=[("internal_group", "=", "expense")],
        default=_set_default_expense_account_id,
    )

    amount_expense = fields.Float(
        string="Importo",
    )

    @api.multi
    def registra_pagamento(self):
        """Create on new account.move for each line of payment order"""

        model = self.env["account.payment.order"]
        order = model.browse(self._context["active_id"])
        po = order

        # pagamento senza portafoglio

        journal = po.journal_id
        if journal.is_wallet:
            msg = "Attenzione!" "\nSelezionato per l'ordine un conto di portafoglio."
            raise UserError(msg)

        new_move_lines = list()

        # importo spese bancarie e conto di accredito
        expenses_account_id = self.account_expense
        expenses_amount = self.amount_expense
        bank_account = journal.default_credit_account_id

        if expenses_amount > 0:
            expense_move_line = {
                "account_id": expenses_account_id.id,
                "credit": 0,
                "debit": expenses_amount,
            }
            new_move_lines.append((0, 0, expense_move_line))

            bank_account_expenses_move_line = {
                "account_id": bank_account.id,
                "credit": expenses_amount,
                "debit": 0,
            }
            new_move_lines.append((0, 0, bank_account_expenses_move_line))
        # end if

        trfmoves = {}
        for bline in order.bank_line_ids:
            hashcode = bline.move_line_offsetting_account_hashcode()
            if hashcode in trfmoves:
                trfmoves[hashcode] += bline
            else:
                trfmoves[hashcode] = bline
        for _hashcode, blines in trfmoves.items():
            post_move = order.payment_mode_id.post_move
            am_obj = self.env["account.move"]
            mvals = order._prepare_move(blines)
            if expenses_amount > 0:
                for line in new_move_lines:
                    mvals["line_ids"].append(line)

            move = am_obj.create(mvals)

            blines.reconcile_payment_lines()
            if post_move:
                move.post()

        order.write(
            {
                "date_generated": fields.Date.context_today(self),
                "state": "uploaded",
                "generated_user_id": self._uid,
                "pagamento_effettuato": True,
            }
        )

        return {"type": "ir.actions.act_window_close"}

    # end registra_accredito
