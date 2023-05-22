# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#

# from collections import defaultdict

from odoo import api, models, fields
from odoo.addons.base_iban.models.res_partner_bank import validate_iban

from ribalta import Document, Receipt

from odoo.exceptions import ValidationError, UserError


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    @api.multi
    def generate_payment_file(self):
        """Creates the RiBa CBI file. That's the important code !"""
        self.ensure_one()

        # Check if the requested payment mode is the one we handle,
        # otherwise call super to delegate the file creation to
        # another method
        if self.payment_method_id.code != 'riba_cbi':
            return super().generate_payment_file()
        else:

            # Build the Document object

            # bank_is_wallet | verifica conto di portafoglio
            # che non deve essere passato
            if self.company_partner_bank_id.bank_is_wallet:
                creditor_bank_account = \
                    self.company_partner_bank_id.bank_main_bank_account_id
            else:
                creditor_bank_account = self.company_partner_bank_id
            # end if

            self.validate_iban(
                creditor_bank_account.acc_number,
                'Codice IBAN creditore non valido'
            )

            riba_doc = Document(
                creditor_company=self.company_id,
                creditor_bank_account=creditor_bank_account,
            )

            # Add receipts to the document
            for pl in self.payment_line_ids:
                rcpt = Receipt(payment_line=pl)
                riba_doc.add_receipt(rcpt)
            # end for

            # Render the document in CBI format
            cbi_doc = riba_doc.render_cbi(group=self.batch_booking)

            return cbi_doc.encode(), f'{riba_doc.name}.txt'
        # end if
    # end generate_payment_file

    @api.multi
    def open2generated(self):

        if self.payment_method_id.code == 'RB-o':
            self.ensure_one()

            # Open the wizard
            model = 'account_banking_riba'
            wiz_view = self.env.ref(model + '.wizard_payment_riba_supplier')
            return {
                'type': 'ir.actions.act_window',
                'name': 'Spese pagamento',
                'res_model': 'wizard.payment.riba.supplier',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': wiz_view.id,
                'target': 'new',
                'res_id': False,
                'binding_model_id': model + '.model_account_payment_order',
                'context': {'active_id': self.id},
            }

        else:
            return super().open2generated()

    @api.multi
    def generated2uploaded(self):
        self.ensure_one()
        if self.payment_method_id.code == 'riba_cbi':
            self = self.with_context(account_payment_order_defer_close=True)
            res = super().generated2uploaded()
            if self.journal_id.is_wallet is False:
                for line in self.payment_line_ids:
                    line.move_line_id.write({
                        'incasso_effettuato': True
                    })
        else:
            res = super().generated2uploaded()
        return res

    @api.multi
    def registra_accredito(self):
        if self.payment_method_id.code == 'riba_cbi':
            self._registra_accredito_riba()
        else:
            super().registra_accredito()
        # end if
    # end registra_accredito

    @staticmethod
    def validate_iban(iban, error_msg):

        # Validate the IBAN
        try:
            validate_iban(iban)
        except ValidationError as ve:
            raise ValidationError(ve)
        # end try / except

        # Ensure IBAN code is for an Italian account
        if not iban.startswith('IT'):
            raise ValidationError(
                error_msg +
                '\nIl codice IBAN deve essere di un conto italiano'
            )
        # end if
    # end validate_iban

    @api.multi
    def _registra_accredito_riba(self):
        """
        TYPE I account move (when conto_effetti_presentati is empty):
        | Description             | Debit | Credit | Notes
        |🕘Portafoglio SBF        |       |    100 | (3) from j. conto_effetti_attivi
        |🕕Effetti allo sconto    |   100 |        | (3) from j. effetti_allo_sconto

        TYPE II account move (when conto_effetti_presentati is empty):
        | Description             | Debit | Credit | Notes
        |🕓Pay off/Effetti attivi |       |    100 | (2)(4) from journal debit/credit
        |🕕Effetti allo sconto    |   100 |        | (3) from j. effetti_allo_sconto
        |🕕Effetti allo sconto    |       |    100 | (3) from j. effetti_allo_sconto
        |  Effetti presentati     |   100 |        | (3) from j. effetti_presentati
        """
        account_expense_id = self._context.get('expenses_account_id')
        amount_expense = self._context.get('expenses_amount')
        credit_date = self._context.get('credit_date')
        # check because date not required
        if not credit_date:
            credit_date = fields.Date.today()
        # end if

        for payment_order in self:

            # Accounts and journals to be used to generate
            # the account.move and account.move.line
            cfg = payment_order.get_move_config()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # validazione conti impostati
            if not cfg['sezionale']:
                raise UserError("Attenzione!\nSezionale non impostato.")
            if not cfg['conto_effetti_attivi']:
                raise UserError("Attenzione!\nConto effetti attivi non impostato.")
            if not cfg['effetti_allo_sconto']:
                raise UserError("Attenzione!\nConto effetti allo sconto non impostato.")
            if not cfg['bank_journal']:
                raise UserError("Attenzione!\nConto di costo non impostato.")
            if not cfg['effetti_presentati'] and not cfg["portafoglio_sbf"]:
                raise UserError("Attenzione!\nConto portafoglio SBF non impostato.")

            # Filter to apply to the payment order lines to retrieve
            # the lines related to the payment order we are processing

            if cfg['effetti_presentati']:
                # MOVE TYPE II
                presentazione_lines = [
                    * payment_order.prepare_move_lines(
                        cfg['conto_effetti_attivi'],
                        "credit",
                        mode="auto"
                    ),
                    * payment_order.prepare_move_lines(
                        cfg['effetti_allo_sconto'],
                        "debit",
                        mode="auto"
                    ),
                ]

                accredito_lines = [
                    * payment_order.prepare_move_lines(
                        cfg['effetti_allo_sconto'],
                        "credit",
                        mode="auto"
                    ),
                    * payment_order.prepare_move_lines(
                        cfg['effetti_presentati'],
                        "debit",
                        mode="auto"
                    ),
                ]
            else:
                # MOVE TYPE I
                presentazione_lines = list()
                accredito_lines = [
                    * payment_order.prepare_move_lines(
                        cfg['effetti_allo_sconto'],
                        "credit",
                        mode="auto"
                    ),
                    * payment_order.prepare_move_lines(
                        cfg['portafoglio_sbf'],
                        "debit",
                        mode="auto"
                    ),
                ]

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # "Spese bancarie" -> una sola riga

            if amount_expense > 0:
                credit_account = self.set_expense_credit_account(
                    cfg['bank_journal'])

                expense_move_line = self.payment_line_ids[0].prepare_1_move_line(
                    account_expense_id, "debit", amount=amount_expense)
                accredito_lines.append((0, 0, expense_move_line))

                bank_expense_line = self.payment_line_ids[0].prepare_1_move_line(
                    credit_account.id, "credit", amount=amount_expense)
                accredito_lines.append((0, 0, bank_expense_line))
            # end if

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Creazione registrazione contabile

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
                'date': credit_date,
                'date_apply_vat': credit_date,
                'journal_id': cfg['sezionale'].id,
                'type': 'entry',
                'state': 'draft',
                'payment_order_id': payment_order.id
            })
            if presentazione_lines:
                vals['ref'] = f'Presentazione distinta {payment_order.name}'
                vals['line_ids'] = presentazione_lines
                new_move = self.env['account.move'].create(vals)
                # If "post_move" flag of the account.payment.mode is True
                # confirm the newly created move
                if payment_order.payment_mode_id.post_move:
                    new_move.post()
                # end if

            vals['ref'] = f'Accredito distinta {payment_order.name}'
            vals['line_ids'] = accredito_lines
            new_move = self.env['account.move'].create(vals)
            # If "post_move" flag of the account.payment.mode is True
            # confirm the newly created move
            if payment_order.payment_mode_id.post_move:
                new_move.post()
            # end if

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Impostazione ordine di pagamento come "Terminato"
            payment_order.action_done()
        # end for

    # end _registra_accredito_riba

    @api.multi
    def _create_reconcile_move(self, hashcode, blines):
        self.ensure_one()
        post_move = self.payment_mode_id.post_move
        am_obj = self.env['account.move']
        mvals = self._prepare_move(blines)
        move = am_obj.create(mvals)
        is_wallet = self.company_partner_bank_id.bank_is_wallet
        pm_code = self.payment_method_id.code
        if is_wallet and pm_code == 'riba_cbi':
            move.invoice_date = move.date
            move.date = fields.Date.today()
            fiscalyears = self.env["account.fiscal.year"].search(
                [
                    ("date_from", "<=", move.date),
                    ("date_to", ">=", move.date),
                    ("company_id", "=", move.company_id.id),
                    ("state", "!=", "done"),
                ],
                limit=1,
            )

            if fiscalyears:
                move.fiscalyear_id = fiscalyears[0]

        blines.reconcile_payment_lines()
        if post_move:
            move.post()
    # end _create_reconcile_move
