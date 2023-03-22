# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class AccountCompensationGenerate(models.TransientModel):
    _name = "wizard.account.compensation.generate"
    _description = "Create compensation from duedates tree view"

    def _set_same_account(self):
        return self._context["same_account"]

    def _set_compensation_amount(self):
        return self._compute_compensation_amount()

    journal_id = fields.Many2one(
        "account.journal",
        string="Registro",
    )

    compensation_date = fields.Date(
        string="Data di registrazione",
    )

    compensation_amount = fields.Float(
        string="Importo di compensazione",
        default=_set_compensation_amount,
    )

    same_account = fields.Boolean(string="Stesso conto", default=_set_same_account)

    def compensate(self):
        # lines = self.env['account.move.line'].browse(
        #     self._context['active_ids']
        # )

        lines = self.env["account.move.line"].search(
            [("id", "in", self._context["active_ids"])], order="date_maturity asc"
        )

        if self._context.get("same_account"):
            # nothing to do only reconcile
            lines.reconcile()
        else:

            compensation_amount = self._compute_compensation_amount()
            comp_sign = self._compute_compensation_sign()
            to_reconcile = dict()
            # Creazione registrazione contabile

            vals = self.env["account.move"].default_get(
                [
                    "date_effective",
                    "fiscalyear_id",
                    "invoice_date",
                    "narration",
                    "payment_term_id",
                    "reverse_date",
                    "tax_type_domain",
                ]
            )

            vals.update(
                {
                    "date": self.compensation_date,
                    "date_apply_vat": self.compensation_date,
                    "journal_id": self.journal_id.id,
                    "type": "entry",
                    "ref": "Compensazione ",
                    "state": "draft",
                }
            )

            move_id = self.env["account.move"].create(vals)

            # scadenze totalmente compensate
            totally_compensate = self._totally_compensate_lines(
                lines, comp_sign, move_id
            )

            # scadenze da compensare anche parzialmente
            if compensation_amount:
                partial_compensate = self._partial_compensate_lines(
                    comp_sign, lines, compensation_amount, move_id
                )
            else:
                partial_compensate = dict()

            # movimenti della registrazione da memorizzare,
            # accoppiare e riconciliare
            move_line_model_no_check = self.env["account.move.line"].with_context(
                check_move_validity=False
            )

            # to_reconcile_full = self.env["account.move.line"]
            if totally_compensate:
                for index, vals in totally_compensate.items():
                    mvl = move_line_model_no_check.create(vals)
                    to_reconcile.update({index: mvl.id})
                # end for
            # end if

            to_reconcile_partial = self.env["account.move.line"]
            if partial_compensate:
                for index, vals in partial_compensate.items():
                    mvl = move_line_model_no_check.create(vals)
                    to_reconcile.update({index: mvl.id})
                # end for
            # end if
            # validate move
            move_id.post()

            # reconciliations
            if to_reconcile:
                for index, index_to_rec in to_reconcile.items():
                    to_reconcile_partial = self.env["account.move.line"]
                    mvl = self.env["account.move.line"].browse(index)
                    to_reconcile_partial += mvl
                    mvl_to_rec = self.env["account.move.line"].browse(index_to_rec)
                    to_reconcile_partial += mvl_to_rec
                    to_reconcile_partial.reconcile()
                # end for
        # # end if

    def _compute_compensation_amount(self):
        total_debit_amount, total_credit_amount = self._compute_totals_debit_credit()

        if total_debit_amount > total_credit_amount:
            compensation_amount = total_credit_amount
        elif total_credit_amount > total_debit_amount:
            compensation_amount = total_debit_amount
        else:
            compensation_amount = total_debit_amount

        return compensation_amount

    def _compute_compensation_sign(self):
        total_debit_amount, total_credit_amount = self._compute_totals_debit_credit()

        if total_debit_amount > total_credit_amount:
            sign = "credit"
        elif total_credit_amount > total_debit_amount:
            sign = "debit"
        else:
            sign = "debit"

        return sign

    def _compute_totals_debit_credit(self):
        lines = self.env["account.move.line"].browse(self._context["active_ids"])
        total_debit_amount = 0
        total_credit_amount = 0

        for line in lines:
            total_debit_amount += line.debit
            total_credit_amount += line.credit

        return total_debit_amount, total_credit_amount

    def _totally_compensate_lines(self, lines, sign, move):

        totally_compensate = dict()

        if sign == "credit":
            tot_compensate_lines = lines.filtered(lambda x: x.credit > 0)
        else:
            tot_compensate_lines = lines.filtered(lambda x: x.debit > 0)

        for line in tot_compensate_lines:
            v = {
                "partner_id": line.partner_id.id,
                "account_id": line.account_id.id,
                "debit": line.credit if sign == "credit" else 0,
                "credit": line.debit if sign == "debit" else 0,
                "move_id": move.id,
            }
            totally_compensate.update({line.id: v})
        return totally_compensate

    def _partial_compensate_lines(self, sign, lines, amount, move):

        partial_compensate = dict()
        left = amount
        if sign == "credit":
            compensate_lines = lines.filtered(lambda x: x.debit > 0)
        else:
            compensate_lines = lines.filtered(lambda x: x.credit > 0)
        # end if

        for line in compensate_lines:

            if sign == "credit":
                amount = line.debit
            else:
                amount = line.credit

            if amount <= left:
                v = {
                    "partner_id": line.partner_id.id,
                    "account_id": line.account_id.id,
                    "debit": amount if sign == "debit" else 0,
                    "credit": amount if sign == "credit" else 0,
                    "move_id": move.id,
                }
                partial_compensate.update({line.id: v})
                left -= amount
            else:
                v = {
                    "partner_id": line.partner_id.id,
                    "account_id": line.account_id.id,
                    "debit": left if sign == "debit" else 0,
                    "credit": left if sign == "credit" else 0,
                    "move_id": move.id,
                }
                partial_compensate.update({line.id: v})
                break
            # end if
        # end for
        return partial_compensate
