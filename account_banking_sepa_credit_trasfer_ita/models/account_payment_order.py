# Copyright 2022 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2022 Didotech s.r.l. <https://www.didotech.com>

import datetime
import logging
import re

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError, UserError


try:
    from fintech.sepa import Account, SEPACreditTransfer
    from fintech.iban import check_iban
    _logger.debug('Importato: Account, SEPACreditTransfer, check_iban.')
except ImportError:
    _logger.debug('Cannot `import fintech`.')


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    @api.multi
    def generate_payment_file(self):
        """Creates the RiBa CBI file. That's the important code !"""
        self.ensure_one()
        
        # Check if the requested payment mode is the one we handle,
        # otherwise call super to delegate the file creation to
        # another method
        if self.payment_method_id.code != 'sct_cbi':
            return super().generate_payment_file()
        else:
            # bank_is_wallet | verifica conto di portafoglio
            # che non deve essere passato
            if self.company_partner_bank_id.bank_is_wallet:
                debtor_bank_account = \
                    self.company_partner_bank_id.bank_main_bank_account_id
            else:

                cuc_code = ''
                now = datetime.datetime.now()
                tmst = now.strftime('%Y%m%d%H%M%S')
                filename = self.name + '_' + tmst + '.xml'

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

                debtor_bank_account = self.company_partner_bank_id

                if not debtor_bank_account.sanitized_acc_number.startswith(
                        'IT'):
                    raise UserError(
                        _('Il codice IBAN deve essere di un conto italiano')
                    )

                result = check_iban(debtor_bank_account.sanitized_acc_number)
                if result is False:
                    raise UserError(
                        _(
                            "L'iban %s indicato non risulta valido."
                        ) % debtor_bank_account.acc_number)

                # company
                debtor = Account(
                    debtor_bank_account.sanitized_acc_number,
                    self.company_id.name
                )
                # creditor id and cuc
                debtor.set_originator_id(
                    ci,
                    cuc_code,
                )

                # Create a SEPACreditTransfer instance
                sct = SEPACreditTransfer(debtor, 'NORM',
                                         scheme='CBIPaymentRequest.00.04.00')
                sct.scl_check = False

                for line in self.bank_line_ids:
                    # amount
                    amount = line.amount_currency

                    # purpose
                    purpose = line.communication

                    # creditor
                    valid = check_iban(
                        line.partner_bank_id.sanitized_acc_number)
                    if valid is False:
                        raise UserError(
                            _(
                                "L'iban %s indicato non risulta valido."
                            ) % line.partner_bank_id.acc_number)

                    partner_iban = line.partner_bank_id.sanitized_acc_number
                    partner = line.partner_id.name
                    creditor = Account(partner_iban, partner)

                    # Add the transaction
                    tx = sct.add_transaction(creditor, amount, purpose)

                # Render the SEPA document
                xml = sct.render()
                return xml, filename

        # end if
    # end generate_payment_file

# end AccountPaymentOrder

