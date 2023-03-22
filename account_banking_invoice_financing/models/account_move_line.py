# Copyright (c) 2020
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    bank_invoice_financing_amount = fields.Float(
        string='Importo anticipato',
        digits=dp.get_precision('Account'),
    )

    @api.multi
    def registra_incasso(self):
        p_method = self.get_payment_method()
        if p_method.code == 'invoice_financing':
            self.registra_incasso_invoice_financing()
        else:
            super().registra_incasso()
    # end registra_incasso

    @api.multi
    def registra_incasso_invoice_financing(self):

        account_expense_id = self._context.get('expenses_account_id')
        amount_expense = self._context.get('expenses_amount')

        for line in self:
            payment_order = line.payment_line_ids[0].order_id
            break

        # CONFIG

        cfg = payment_order.get_move_config()

        # validazione conti impostati

        if not cfg['sezionale'].id:
            raise UserError("Attenzione!\nSezionale non "
                            "impostato.")

        if not cfg['bank_journal'].id:
            raise UserError("Attenzione!\nConto di costo non impostato.")

        bank_account = cfg['bank_journal'].default_debit_account_id

        vals = self.env['account.move'].default_get([
            # 'date_apply_balance',
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
            'journal_id': cfg['sezionale'].id,
            'type': 'entry',
            'ref': "Conferma pagamento ",
            'state': 'draft',
        })
        # Creazione registrazione contabile

        ac_id = self.env['account.move'].create(vals)

        conto_banca_totale = 0.0

        for line in self:

            # per ogni riga
            # genero un movimento

            conto_banca_totale += line.debit

            conto_cliente = {
                'move_id': ac_id.id,
                'account_id': line.account_id.id,
                'partner_id': line.partner_id.id,
                'credit': line.debit,
                'debit': 0
            }

            acc_line = self.env['account.move.line'].with_context(
                check_move_validity=False).create(conto_cliente)

            # riconciliazione
            to_reconcile = self.browse([line.id, acc_line.id])
            to_reconcile.reconcile()
            line.write({
                'incasso_effettuato': True
            })
        # end for

        # se ci sono spese le aggiungo
        if amount_expense > 0:
            bank_expense_move_line = {
                'move_id': ac_id.id,
                'account_id': account_expense_id,
                'credit': amount_expense,
                'debit': 0,
            }
            self.env['account.move.line'].with_context(
                check_move_validity=False).create(bank_expense_move_line)

            conto_banca = {
                'move_id': ac_id.id,
                'account_id': bank_account.id,
                'credit': 0,
                'debit': amount_expense
            }
            self.env['account.move.line'].with_context(
                check_move_validity=False).create(conto_banca)

        # totale in dare
        conto_banca = {
            'move_id': ac_id.id,
            'account_id': bank_account.id,
            'credit': 0,
            'debit': conto_banca_totale
        }
        self.env['account.move.line'].with_context(
            check_move_validity=False).create(conto_banca)

    # end registra_incasso_invoice_financing
