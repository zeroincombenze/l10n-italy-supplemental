# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
import datetime
import logging
import re

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

try:
    from fintech.sepa import Account, SEPADirectDebit
    from fintech.iban import check_iban
except ImportError:
    _logger.debug('Cannot import SEPADirectDebit.')

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    @api.multi
    def generate_payment_file(self):
        """Creates the SEPA Direct Debit CBI file.
         That's the important code !"""
        self.ensure_one()
        
        if self.payment_method_id.code != 'sdd_core_cbi' and (
                self.payment_method_id.code != 'sdd_b2b_cbi'):
            return super().generate_payment_file()
        else:
            # bank_is_wallet | verifica conto di portafoglio
            # che non deve essere passato
            if self.company_partner_bank_id.bank_is_wallet:
                creditor_bank_account = \
                    self.company_partner_bank_id.bank_main_bank_account_id
            else:
                creditor_bank_account = self.company_partner_bank_id
            # end if

            if self.payment_method_id.code == 'sdd_core_cbi':
                sdd_type = 'CORE'
            elif self.payment_method_id.code == 'sdd_b2b_cbi':
                sdd_type = 'B2B'
            else:
                raise UserError(_("Il tipo di Sepa Direct Debit non è ne' "
                                  "CORE ne' B2B."))

            now = datetime.datetime.now()
            tmst = now.strftime('%Y%m%d%H%M%S')
            filename = self.name + '_' + tmst + '.xml'

            self.validate_iban(
                creditor_bank_account.acc_number,
                'Codice IBAN creditore non valido'
            )

            # Codice Identificativo di Creditore
            if self.company_id.sepa_creditor_identifier:
                ci = self.company_id.sepa_creditor_identifier
            else:
                raise UserError(_('Il Codice Identificativo di Creditore '
                                  'non è stato impostato.'))

            # cuc codice univoco cbi
            if self.company_id.initiating_party_identifier:
                cuc_code = self.company_id.initiating_party_identifier
            else:
                raise UserError(
                    _('Il Codice Univoco CBI non è stato impostato.'))

            if re.match(r'[A-Z0-9]{8}', cuc_code) is False:
                raise UserError(
                    _('Il Codice Univoco CBI non è valido.'))

            # Creditore
            creditor = Account(creditor_bank_account.sanitized_acc_number,
                               self.company_id.name)
            # Imposta ID creditore
            creditor.set_originator_id(ci, cuc_code)

            # Create a SEPADirectDebit instance of type sdd_type
            sdd = SEPADirectDebit(creditor, sdd_type)

            for count, line in enumerate(self.bank_line_ids, start=1):
                # amount
                amount = line.amount_currency
                # purpose
                purpose = f"{line.communication}_{count}"

                valid = check_iban(
                    line.partner_bank_id.sanitized_acc_number)
                if valid is False:
                    raise UserError(
                        _(
                            "L'iban %s indicato non risulta valido."
                        ) % line.partner_bank_id.acc_number)

                partner_iban = line.partner_bank_id.sanitized_acc_number
                bic = line.partner_bank_id.bank_id.bic
                if bic is False:
                    raise UserError(
                        _(
                            "Il codice BIC della banca %s non risulta valido."
                        ) % line.partner_bank_id.bank_id.name)

                # debtor
                partner = line.partner_id.name
                ptr_tup = (partner_iban, bic)
                debtor = Account(ptr_tup, partner)

                mandate = self._get_mandate(line.partner_id, sdd_type)
                if mandate is False:
                    raise UserError(
                        _(
                            "Il mandato per il partner %s non risulta valido."
                        ) % line.partner_id.name)

                mref = mandate.unique_mandate_reference
                signed = mandate.signature_date
                recurrent = True if mandate.type == 'recurrent' else False
                # For a SEPA direct debit a valid mandate is required
                debtor.set_mandate(mref=mref, signed=signed, recurrent=recurrent)
                # Add the transaction
                trans = sdd.add_transaction(debtor, amount, purpose, eref=f"{count}", due_date=line.date)
                # Render the SEPA document

            xml_content = sdd.render()
            return xml_content, filename

    # end generate_payment_file

    def _get_mandate(self, partner, scheme):
        mandate = self.env['account.banking.mandate'].search([
            ('partner_id', '=', partner.id),
            ('scheme', '=', scheme),
            ('state', '=', 'valid'),
        ])

        if len(mandate) == 1:
            return mandate
        return False
    # and _get_mandate

# end AccountPaymentOrder
