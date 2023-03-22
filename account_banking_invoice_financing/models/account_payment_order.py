# Copyright 2020-16 Powerp Enterprise Network
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from datetime import date
import os
import tempfile
import zipfile
from io import BytesIO
from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError


class PaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    # -> data previsto incasso (date)
    forecast_payment_date = fields.Date(
        string='Data previsto incasso',
    )

    # -> importo accredito (float)
    bank_invoice_financing_amount = fields.Float(
        string='Importo accreditato',
    )

    # -> data apertura anticipo (date)
    bank_invoice_financing_date = fields.Date(
        string='Data apertura anticipo',
    )

    # -> numero anticipo (char)
    bank_invoice_financing_number = fields.Char(
        string='Numero anticipo',
    )

    # -> data rimborso (char)
    bank_return_payment_date = fields.Date(
        string='Data rimborso',
    )

    # flag per gestire lo stato e chidere l'anticipo
    anticipo_aperto = fields.Boolean(string="Anticipo aperto", default=False)

    massimale = fields.Float(
        string='Massimale anticipo',
        compute='_compute_massimale'
    )

    massimale_at_opening = fields.Float(
        string='Massimale anticipo alla conferma ordine',
    )

    @api.multi
    def generate_payment_file(self):
        """Creates the Zip file with pdf payment order and invoices."""
        self.ensure_one()

        # Check if the requested payment mode is the one we handle,
        # otherwise call super to delegate the file creation to
        # another method
        if self.payment_method_id.code != 'invoice_financing':
            return super().generate_payment_file()
        else:
            # buffer to check generated invoices
            invoices_ids = []
            # binary to return
            zip_contents = ''
            # create files pdf in /tmp as temporary
            archive_zip_name = self.name.replace('/', '_') + '.zip'
            with tempfile.TemporaryDirectory() as tmp:
                fp = BytesIO()
                # set zip file in memory
                with zipfile.ZipFile(fp, mode='w') as myzip:
                    # generate payment order pdf
                    pdf_order = self.env.ref(
                        'account_banking_invoice_financing.action_print_payment_order_ita'
                    ).sudo().render_qweb_pdf([self.id])[0]
                    pdf_order_file_arcname = self.name.replace(
                        '/', '_') + '.pdf'

                    pdf_order_file_name = os.path.join(
                        tmp, pdf_order_file_arcname
                    )
                    
                    with open(pdf_order_file_name, 'wb') as f:
                        f.write(pdf_order)
                        # Write the PDF file and flush it to ensure memory
                        # buffers are correctly saved to disk before reading
                        # it to add content to zip file
                        f.flush()
                        myzip.write(pdf_order_file_name, pdf_order_file_arcname)
                    # end with

                    for line in self.payment_line_ids:
                        # print(line.move_line_id.invoice_id.id)
                        invoice_id = line.move_line_id.invoice_id.id
                        invoice_number = line.move_line_id.invoice_id.number
                        invoice_file = invoice_number.replace('/', '_') + '.pdf'
                        if invoice_id not in invoices_ids:
                            invoices_ids.append(invoice_id)
                        else:
                            continue

                        pdf_binary_invoice = self.env.ref(
                            'account.account_invoices').sudo().render_qweb_pdf(
                            [invoice_id])[0]

                        binary_invoice_file_path = os.path.join(
                            tmp, invoice_file)
                        
                        with open(binary_invoice_file_path, 'wb') as f:
                            f.write(pdf_binary_invoice)
                            # Write the PDF file and flush it to ensure memory
                            # buffers are correctly saved to disk before reading
                            # it to add content to zip file
                            f.flush()
                            myzip.write(binary_invoice_file_path, invoice_file)
                        # end with

                fp.seek(0)
                zip_contents = fp.read()

            # return file
            return zip_contents, archive_zip_name
        # end if
    # end generate_payment_file

    # - - - - - - - - - - - - - - - - - - - - -
    # Metodi richiamati al passaggio di stato
    # - - - - - - - - - - - - - - - - - - - - -
    @api.multi
    def draft2open(self):
        
        self.ensure_one()
        
        # Validations
        if self.payment_method_id.code == 'invoice_financing':
            self._validate_forecast_payment_date()
            self._validate_bank_invoice_financing_amount()
            self.massimale_at_opening = self.massimale
        # end if
        
        # Call superclass method
        super().draft2open()
    # end draft2open

    @api.multi
    def generated2uploaded(self):
        # Questo metodo NON deve effettuare nessuna
        # operazione/registrazione contabile.
        # La generazione delle operazioni contabili
        # avverrà con le operazioni di:
        #  - accredito
        #  - incasso effettivo
        
        self.ensure_one()
        
        if self.payment_method_id.code != 'invoice_financing':
            return super().generated2uploaded()
        # end if
        
        self.write({
            'state': 'uploaded',
            'date_uploaded': fields.Date.context_today(self),
        })
        
        return True
    # end generated2uploaded

    @api.multi
    def action_anticipo_aperto(self):
        module = 'account_banking_invoice_financing'
        view = module + '.wizard_payment_order_open_credit'

        for order in self:
            if order.state == 'uploaded':
                # validation
                if order.payment_method_code not in [
                    'invoice_financing',
                ]:
                    raise UserError('Attenzione!\nIl metodo di pagamento non '
                                    'permette l\'operazione.')

                # apertura wizard
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Anticipo aperto',
                    'res_model': 'wizard.payment.order.invoice.financing',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'view_id': self.env.ref(view).id,
                    'target': 'new',
                    'res_id': False,
                    "binding_model_id": "account.model_account_payment_order"
                }

    @api.multi
    def action_anticipo_chiuso(self):
        module = 'account_banking_invoice_financing'
        view = module + '.wizard_payment_order_close_financing'

        for order in self:
            if order.state == 'done' and order.anticipo_aperto is True:
                # validation
                if order.payment_method_code not in [
                    'invoice_financing',
                ]:
                    raise UserError('Attenzione!\nIl metodo di pagamento non '
                                    'permette l\'operazione.')

                # apertura wizard
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Chiusura anticipo',
                    'res_model': 'wizard.payment.order.close.financing',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'view_id': self.env.ref(view).id,
                    'target': 'new',
                    'res_id': False,
                    "binding_model_id": "account.model_account_payment_order"
                }

    @api.multi
    def apri_anticipo(self):

        # conto bancario ordine
        # padre conto
        # registro padre conto
        # conto di default

        if self.payment_method_code != 'invoice_financing':
            raise UserError("Attenzione!\nFunzionalità non supportata.")
        # end if

        account_expense_id = self._context.get('expenses_account_id')
        amount_expense = self._context.get('expenses_amount')

        for payment_order in self:

            cfg = payment_order.get_move_config()

            # validazione conti impostati

            if not cfg['sezionale'].id:
                raise UserError("Attenzione!\nSezionale non "
                                "impostato.")
            # end if

            if not cfg['banca_conto_effetti'].id:
                raise UserError("Attenzione!\nBanca conto effetti "
                                "non impostato.")
            # end if

            if not cfg['effetti_allo_sconto'].id:
                raise UserError("Attenzione!\nConto Effetti allo sconto "
                                "non impostato.")
            # end if

            if amount_expense > 0:
                if not cfg['bank_journal'].id:
                    raise UserError("Attenzione!\nConto banca non impostato.")
            # end if

            # bank_account = cfg['bank_journal'].default_credit_account_id

            line_ids = []

            # se ci sono spese le aggiungo
            if amount_expense > 0:

                credit_account = self.set_expense_credit_account(
                    cfg['bank_journal'])

                expense_move_line = {
                    'account_id': account_expense_id,
                    'credit': 0,
                    'debit': amount_expense,
                }
                line_ids.append((0, 0, expense_move_line))

                bank_expense_line = {
                    'account_id': credit_account.id,
                    'credit': amount_expense,
                    'debit': 0,
                }
                line_ids.append((0, 0, bank_expense_line))
            # end if

            # banca conto effetti
            banca_conto_effetti = {
                'account_id': cfg['banca_conto_effetti'].id,
                # 'partner_id': partner_id,
                'credit': 0,
                'debit': self.bank_invoice_financing_amount,
            }
            line_ids.append((0, 0, banca_conto_effetti))

            effetti_allo_sconto = {
                'account_id': cfg['effetti_allo_sconto'].id,
                'credit': self.bank_invoice_financing_amount,
                'debit': 0
            }
            line_ids.append((0, 0, effetti_allo_sconto))

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
                'ref': "Apertura anticipo ordine {order}".format(
                    order=payment_order.name),
                'state': 'draft',
                'line_ids': line_ids,
                'payment_order_id': payment_order.id,
            })

            # Creazione registrazione contabile
            self.env['account.move'].create(vals)

            payment_order.write({
                'anticipo_aperto': True
            })

            payment_order.action_done()

    # end apri_anticipo

    @api.multi
    def chiudi_anticipo(self):

        if self.payment_method_code != 'invoice_financing':
            raise UserError("Attenzione!\nFunzionalità non supportata.")
        # end if

        account_expense_id = self._context.get('expenses_account_id')
        amount_expense = self._context.get('expenses_amount')

        for payment_order in self:

            cfg = payment_order.get_move_config()

            # validazione conti impostati

            if not cfg['sezionale'].id:
                raise UserError("Attenzione!\nSezionale non "
                                "impostato.")
            # end if

            if not cfg['banca_conto_effetti'].id:
                raise UserError("Attenzione!\nBanca conto effetti "
                                "non impostato.")
            # end if

            if not cfg['effetti_allo_sconto'].id:
                raise UserError("Attenzione!\nConto Effetti allo sconto "
                                "non impostato.")
            # end if

            if amount_expense > 0:
                if not cfg['bank_journal'].id:
                    raise UserError("Attenzione!\nConto banca non impostato.")
            # end if

            # bank_account = cfg['bank_journal'].default_credit_account_id

            line_ids = []

            # se ci sono spese le aggiungo
            if amount_expense > 0:

                credit_account = self.set_expense_credit_account(
                    cfg['bank_journal'])

                expense_move_line = {
                    'account_id': account_expense_id,
                    'credit': 0,
                    'debit': amount_expense,
                }
                line_ids.append((0, 0, expense_move_line))

                bank_expense_line = {
                    'account_id': credit_account.id,
                    'credit': amount_expense,
                    'debit': 0,
                }
                line_ids.append((0, 0, bank_expense_line))
            # end if

            # banca conto effetti
            banca_conto_effetti = {
                'account_id': cfg['banca_conto_effetti'].id,
                'credit': self.bank_invoice_financing_amount,
                'debit': 0,
            }
            line_ids.append((0, 0, banca_conto_effetti))

            effetti_allo_sconto = {
                'account_id': cfg['effetti_allo_sconto'].id,
                'credit': 0,
                'debit': self.bank_invoice_financing_amount,
            }
            line_ids.append((0, 0, effetti_allo_sconto))

            vals = self.env['account.move'].default_get([
                'date_apply_balance',
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
                'ref': "Chiusura anticipo ordine {order}".format(
                    order=payment_order.name),
                'state': 'draft',
                'line_ids': line_ids
            })

            # Creazione registrazione contabile
            self.env['account.move'].create(vals)

            payment_order.write({
                'anticipo_aperto': False
            })
        # end for

    # end chiudi_anticipo

    # - - - - - - - - - - - - - - - - - - - - -
    # onchange
    # - - - - - - - - - - - - - - - - - - - - -

    @api.onchange('bank_invoice_financing_amount')
    def _onchange_bank_invoice_financing_amount(self):
        if self.bank_invoice_financing_amount > self.massimale:
            warning_msg = {
                'title': 'Importo anticipato superiore al massimale!',
                'message': f'L\'importo anticipato non può essere '
                           f'superiore al massimale ({self.massimale}).'
            }
            return {
                'warning': warning_msg
            }
        # end if
    # end _onchange_massimale

    # - - - - - - - - - - - - - - - - - - - - -
    # Metodi privati
    # - - - - - - - - - - - - - - - - - - - - -
    
    @api.model
    def _validate_forecast_payment_date(self):
        if not self.forecast_payment_date:
            raise ValidationError('Data di previsto incasso mancante')
        # end if
        if self.forecast_payment_date < date.today():
            raise ValidationError('La Data di previsto incasso non può essere nel passato')
        # end if
    # end _validate_forecast_payment_date
    
    @api.model
    def _validate_bank_invoice_financing_amount(self):
        if not self.bank_invoice_financing_amount:
            raise ValidationError('Importo accreditato non impostato')
        # end if
        if self.bank_invoice_financing_amount <= 0:
            raise ValidationError('Importo accreditato deve essere maggiore di zero')
        # end if
        if self.bank_invoice_financing_amount > self.massimale:
            raise ValidationError(
                f'Importo accreditato non può superare '
                f'il massimale ({self.massimale} €)'
            )
        # end if
    # end _validate_bank_invoice_financing_amount

    @api.depends('company_partner_bank_id', 'payment_line_ids')
    def _compute_massimale(self):
        """
        il metodo scrive il massimale nel campo 'massimale' dell'ordine
        a seconda del metodo di calcolo.

        Massimale su TOTALE FATTURA (invoice_amount):
        1) Sommo il valore delle righe
        2) moltiplico il totale del passo 1) per la percentuale di anticipo

        Massimale su IMPONIBILE FATTURA (taxable_amount):
        1) Recupero la testata della fattura dove trovo: imponibile
        (amount_untaxed) e totale fattura (amount_total)
        2) Ripartisco l'imponibile in proporzione al
        totale della riga = imponibile / totale * importo_riga
        3) Il massimale è dato dal totale dell'imponibile delle righe
        moltiplicato per la percentuale di anticipo

        Massimale su ORDINI CONFERMATI (state diverso da "draft"):
        viene ritornato il valore del campo massimale_at_opening, tale
        campo viene impostato uguale al valore del massimale nel momento
        in cui si procede alla conferma dell'ordine di pagamento dal
        metodo draft2open()
        """

        def max_not_draft():
            """
                Caso ordine di pagamento confermato (stato != da bozza):
                prendo il massimale memorizzato al momento della conferma
            """
            if order.massimale_at_opening:
                order.massimale = order.massimale_at_opening
            else:
                # Fallback value to avoid errors when
                # order.massimale_at_opening is not set
                # (for example when data is imported from external systems)
                order.massimale = order.bank_invoice_financing_amount
            # end if
        # end max_not_draft

        def max_invoice_amount():
            """
                Caso massimale su totale fattura
            """

            totale_importo = 0.0

            for line in order.payment_line_ids:
                totale_importo += line.amount_currency
            # end for

            order.massimale = self._percentuale(
                journal.invoice_financing_percent,
                totale_importo,
            )
        # end max_invoice_amount

        def max_taxable_amount():
            """
                Caso massimale su imponibile fattura
            """

            totale_importo = 0.0

            for line in order.payment_line_ids:
                multiplier = self._moltiplicatore_scadenza(
                    line.move_line_id,
                )

                imponibile = line.amount_currency * multiplier

                totale_importo += imponibile
            # end for

            order.massimale = self._percentuale(
                journal.invoice_financing_percent,
                totale_importo
            )
        # end max_taxable_amount

        for order in self:

            if order.payment_method_code != 'invoice_financing':
                return 0.0

            journal = None
            bank_account = None

            # - - - - - - - - - - - - - - - - - - -
            # validazione parametri per il calcolo
            # - - - - - - - - - - - - - - - - - - -
            if order.journal_id and order.journal_id.id:
                journal = order.journal_id
            else:
                raise UserError(
                    'Attenzione!\nImpostare il registro per '
                    'la generazione dell\'ordine.'
                )
            # end if

            evaluation_method = journal.invoice_financing_evaluate

            if not evaluation_method:
                raise UserError(
                    'Attenzione!\nMetodo calcolo anticipo '
                    'non impostato nel registro.'
                )

            elif evaluation_method not in ['invoice_amount', 'taxable_amount']:
                raise UserError(
                    f'Attenzione!\nMetodo calcolo anticipo '
                    'ha un valore sconosciuto ({evaluation_method}).'
                )
            # end if

            if not journal.invoice_financing_percent:
                raise UserError(
                    'Attenzione!\nPercentuale di anticipo '
                    'non impostata nel registro.'
                )
            # end if

            if journal.invoice_financing_percent <= 0:
                raise UserError(
                    'Attenzione!\nLa percentuale di anticipo impostata '
                    'nel conto deve essere maggiore di zero.'
                )
            # end if

            # - - - - - - - - - - - - - - - - - - - - - - -
            # Calcolo massimale secondo metodo selezionato
            # - - - - - - - - - - - - - - - - - - - - - - -

            if order.state != 'draft':
                max_not_draft()

            elif evaluation_method == 'invoice_amount':
                max_invoice_amount()

            elif evaluation_method == 'taxable_amount':
                max_taxable_amount()

            else:
                # Il controllo che il metodo di calcolo massimale sia corretto
                # è già stato fatto in precedenza, quindi non si dovrebbe mai
                # entrare in questo blocco.
                assert False
            # end if

        # end for

        self.set_default_financed_amount()
    # end _compute_massimale

    @api.multi
    def set_default_financed_amount(self):
        """Ensures financed_amount has a sensible default value."""

        for order in self:

            financed_amount = order.bank_invoice_financing_amount

            if not financed_amount:
                # Set default value for bank_invoice_financing_amount
                # if the field does not have a value
                order.bank_invoice_financing_amount = self.massimale
            # end if
        # end for
    # end update_financed_amount

    def _percentuale(self, perc, total):
        val = (float(total) / 100) * float(perc)
        return round(val, 2)
    # end _percentuale

    def _moltiplicatore_scadenza(self, line):
        move_id = line.move_id
        amount_untaxed = move_id.line_ids[0].invoice_id.amount_untaxed
        amount_total = move_id.line_ids[0].invoice_id.amount_total
        return amount_untaxed / amount_total
    # end _moltiplicatore_scadenza

    @api.model_cr_context
    def _init_column(self, column_name):
        """ Initialize the value of the given column for existing rows.
            Overridden here because we need to set the value of the
            massimale_at_opening field for the payment orders created
            before the massimale_at_opening field was introduced.
            The field massimale_at_opening will be set equal to the
            bank_invoice_financing_amount (financed amount) for every
            payment order not in draft state which has zero or NULL
            as value of the massimale_at_opening field.
        """

        if column_name == 'massimale_at_opening':

            query = f'''
                UPDATE
                    "{self._table}" as apo
                SET
                    "{column_name}" = "bank_invoice_financing_amount"
                WHERE
                    id IN (
                        SELECT
                            apo.id
                        FROM
                            account_payment_order as apo
                        LEFT JOIN
                            account_payment_method as apm on apm.id = apo.payment_method_id
                        WHERE
                            state <> 'draft'
                        AND
                            apm.code = 'invoice_financing'
                    )
                ;
            '''

            self.env.cr.execute(query)

        else:
            super()._init_column(column_name)
    # end _init_column


# end PaymentOrder
