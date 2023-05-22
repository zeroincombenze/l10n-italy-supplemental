# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#

from odoo import models, api, fields
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def registra_insoluto(self):

        # The payment method of the payment order
        p_method = self.get_payment_method()

        if p_method.code == 'riba_cbi':
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

        if p_method.code == 'riba_cbi':
            self._registra_incasso_riba()
        else:
            super().registra_incasso()
        # end if
    # end registra_incasso

    @api.multi
    def _registra_incasso_riba(self):

        # NB: no need to perform checks on the selected lines, the checks have
        #     already been performed by the method:
        #
        #         account.move.line.open_wizard_payment_confirm()
        #
        #     which gets called by the server action that opens the wizard.

        expenses_account_id = self._context.get('expenses_account_id')
        expenses_amount = self._context.get('expenses_amount')

        # Retrieve the payment order
        # Since it's guaranteed to be the same for all the lines pick
        # the payment order of the first line
        po = self[0].payment_line_ids[0].order_id

        # Holds the configuration to be used to generate the new account.move
        cfg = po.get_move_config()

        # validazione conti impostati
        if not cfg["bank_journal"]:
            raise UserError("Attenzione!\nSezionale non impostato.")
        if not cfg["liquidity_account"]:
            raise UserError("Attenzione!\nConto liquidità non impostato.")
        if not cfg['conto_effetti_attivi']:
            raise UserError("Attenzione!\nConto effetti attivi non impostato.")
        if not cfg['effetti_allo_sconto']:
            raise UserError("Attenzione!\nConto effetti allo sconto non impostato.")
        if not cfg["effetti_presentati"] and not cfg["portafoglio_sbf"]:
            raise UserError("Attenzione!\nConto portafoglio SBF non impostato.")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Move generation
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        debit_amount = 0
        for line in self:
            debit_amount += line.amount_into_payment_line

        # Holds the list of lines to be included in the new account.move
        new_move_lines = list()

        if cfg['effetti_presentati']:
            # MOVE TYPE II
            liquidity_move_line = self.prepare_1_move_line(
                cfg["liquidity_account"].id,
                "debit",
                amount=debit_amount,
            )
            new_move_lines.append((0, 0, liquidity_move_line))

            # Una riga per ogni scadenza selezionata dall'operatore con il conto
            # "Effetti all'incasso" default_credit_account_id
            for line in self:
                effetti_incasso_line = line.prepare_1_move_line(
                    cfg["effetti_presentati"].id,
                    "credit",
                )
                new_move_lines.append((0, 0, effetti_incasso_line))
        else:
            effetti_sconto_move_line = self.prepare_1_move_line(
                cfg["effetti_allo_sconto"].id,
                "debit",
                amount=debit_amount,
            )
            new_move_lines.append((0, 0, effetti_sconto_move_line))

            portafoglio_move_line = self.prepare_1_move_line(
                cfg["portafoglio_sbf"].id,
                "credit",
                amount=debit_amount,
            )
            new_move_lines.append((0, 0, portafoglio_move_line))

            liquidity_move_line = self.prepare_1_move_line(
                cfg["liquidity_account"].id,
                "debit",
                amount=debit_amount,
            )
            new_move_lines.append((0, 0, liquidity_move_line))

            # Una riga per ogni scadenza selezionata dall'operatore con il conto
            # "Effetti all'incasso" default_credit_account_id
            for line in self:
                effetti_incasso_line = line.prepare_1_move_line(
                    cfg["conto_effetti_attivi"].id,
                    "credit",
                )
                new_move_lines.append((0, 0, effetti_incasso_line))

        # - - - Expenses (if any)
        if expenses_amount > 0:
            expense_move_line = line.prepare_1_move_line(
                expenses_account_id,
                "debit",
                amount=expenses_amount
            )
            new_move_lines.append((0, 0, expense_move_line))

            bank_account_expenses_move_line = line.prepare_1_move_line(
                cfg["liquidity_account"].id,
                "credit",
                amount=expenses_amount
            )
            new_move_lines.append((0, 0, bank_account_expenses_move_line))
        # end if

        # - - - Create the account.move
        vals = self.env['account.move'].default_get([
            'date_effective',
            'fiscalyear_id',
            'invoice_date',
            'narration',
            'payment_term_id',
            'reverse_date',
            'tax_type_domain',
        ])
        vals.update({
            'date': fields.Date.today(),
            'date_apply_vat': fields.Date.today(),
            'journal_id': cfg["bank_journal"].id,
            'type': 'entry',
            'ref': 'Rilevazione pagamento RIBA',
            'state': 'draft',
            'line_ids': new_move_lines
        })
        self.env['account.move'].create(vals)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Mark the lines as 'incasso_effettuato'
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.write({
            'incasso_effettuato': True
        })
    # end _registra_incasso_riba

    def prepare_1_move_line(self, account_id, side, amount=None):
        """Prepare account move line value"""
        if side not in ("debit", "credit"):
            raise UserError(
                "Invalid %s value: must be 'debit' or 'credit'" % side
            )

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
                    [x.name for x in payments])
        else:
            values["name"] = f'Fattura {self.move_id.name}'
            # Le tre righe seguenti sono state commentate perchè
            # causano comportamenti anomali.
            # La modifica è state fatta in accordo con Antonio Vigliotti in video call
            # values["payment_line_ids"] = [
            #     (6, 0, [x.id for x in self.payment_line_ids])
            # ]
        if not amount:
            values["partner_id"] = self.partner_id.id
        return values
