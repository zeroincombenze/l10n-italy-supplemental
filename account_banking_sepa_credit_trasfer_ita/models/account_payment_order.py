# Copyright 2022-26 Zeroincombenze srls <https://www.zeroincombenze.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
import re

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import fintech

    try:
        # Unlicensed mode; must run before the fintech submodules are imported.
        # Raises if another module has already registered the library.
        fintech.register()
    except Exception:  # pylint: disable=broad-except
        pass
    from fintech.iban import check_iban
    from fintech.sepa import Account, SEPACreditTransfer
except ImportError:  # pragma: no cover
    _logger.debug("Cannot import fintech.")

SCT_CBI_SCHEME = "CBIPaymentRequest.00.04.00"


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    def _sct_cbi_debtor_bank(self):
        """Bank account written in the file as debtor.

        A wallet account ("conto di portafoglio") is never sent to the bank:
        its main account is used. The wallet fields are not part of this
        module; they are used only when some other module provides them.
        """
        bank = self.company_partner_bank_id
        if (
            "bank_is_wallet" in bank._fields
            and bank.bank_is_wallet
            and bank.bank_main_bank_account_id
        ):
            return bank.bank_main_bank_account_id
        return bank

    def _sct_cbi_creditor_identifier(self):
        """SEPA creditor id is optional for credit transfers; the field
        exists only when account_banking_sepa_direct_debit is installed."""
        for record in (self.payment_mode_id, self.company_id):
            if "sepa_creditor_identifier" in record._fields:
                if record.sepa_creditor_identifier:
                    return record.sepa_creditor_identifier
        return None

    def generate_payment_file(self):
        """Creates the SEPA Credit Transfer CBI file (CBIPaymentRequest)."""
        self.ensure_one()
        if self.payment_method_id.code != "sct_cbi":
            return super().generate_payment_file()

        # CUC: Codice Univoco CBI
        cuc_code = (
            self.payment_mode_id.initiating_party_identifier
            or self.company_id.initiating_party_identifier
        )
        if not cuc_code:
            raise UserError(_("CBI Unique Code (CUC) is not set."))
        if not re.fullmatch(r"[A-Z0-9]{8}", cuc_code):
            raise UserError(
                _("CBI Unique Code (CUC) %s is not valid: 8 letters or digits.")
                % cuc_code
            )

        debtor_bank = self._sct_cbi_debtor_bank()
        iban = debtor_bank.sanitized_acc_number or ""
        if not iban.startswith("IT"):
            raise UserError(_("The company bank account must be an Italian IBAN."))
        if not check_iban(iban):
            raise UserError(_("Company IBAN %s is not valid.") % debtor_bank.acc_number)

        debtor = Account(iban, self.company_id.name)
        debtor.set_originator_id(self._sct_cbi_creditor_identifier(), cuc_code)
        sct = SEPACreditTransfer(debtor, "NORM", scheme=SCT_CBI_SCHEME)
        sct.scl_check = False

        today = fields.Date.context_today(self)
        for count, payment in enumerate(self.payment_ids, start=1):
            payment_line = payment.payment_line_ids[:1]
            partner_bank = payment.partner_bank_id or payment_line.partner_bank_id
            if not partner_bank or not check_iban(partner_bank.sanitized_acc_number):
                raise UserError(
                    _("IBAN %(iban)s of %(partner)s is not valid.")
                    % {
                        "iban": partner_bank.acc_number or "",
                        "partner": payment.partner_id.name,
                    }
                )
            try:
                creditor = Account(
                    partner_bank.sanitized_acc_number, payment.partner_id.name
                )
            except ValueError as e:
                raise UserError(
                    _("Bank account %(iban)s of %(partner)s: %(err)s")
                    % {
                        "iban": partner_bank.acc_number,
                        "partner": payment.partner_id.name,
                        "err": e,
                    }
                ) from e
            communication = payment.memo or payment_line.communication or self.name
            due_date = payment.payment_line_date
            sct.add_transaction(
                creditor,
                payment.amount,
                communication,
                eref=str(count),
                # a past date means "as soon as possible"
                due_date=due_date if due_date and due_date > today else None,
            )

        tmst = fields.Datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{self.name}_{tmst}.xml".replace("/", "-")
        xml_content = sct.render()
        if isinstance(xml_content, str):
            xml_content = xml_content.encode("utf-8")
        return xml_content, filename
