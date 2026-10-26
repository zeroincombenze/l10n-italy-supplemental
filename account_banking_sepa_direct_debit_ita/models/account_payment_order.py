# Copyright 2021-26 Zeroincombenze srls <https://www.zeroincombenze.it>
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
    from fintech.sepa import Account, SEPADirectDebit
except ImportError:  # pragma: no cover
    _logger.debug("Cannot import fintech.")

SDD_CBI_TYPES = {
    "sdd_core_cbi": "CORE",
    "sdd_b2b_cbi": "B2B",
}


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    def _sdd_cbi_creditor_bank(self):
        """Bank account written in the file as creditor.

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

    def _sdd_cbi_check_iban(self, bank, message):
        if not bank or not check_iban(bank.sanitized_acc_number):
            raise UserError(message)

    def generate_payment_file(self):
        """Creates the SEPA Direct Debit CBI file (CBISDDReqLogMsg)."""
        self.ensure_one()
        sdd_type = SDD_CBI_TYPES.get(self.payment_method_id.code)
        if not sdd_type:
            return super().generate_payment_file()

        creditor_bank = self._sdd_cbi_creditor_bank()
        self._sdd_cbi_check_iban(
            creditor_bank,
            _("Creditor IBAN %s is not valid.") % (creditor_bank.acc_number or ""),
        )

        # Codice Identificativo del Creditore
        ci = (
            self.payment_mode_id.sepa_creditor_identifier
            or self.company_id.sepa_creditor_identifier
        )
        if not ci:
            raise UserError(_("SEPA Creditor Identifier is not set."))

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

        creditor = Account(creditor_bank.sanitized_acc_number, self.company_id.name)
        creditor.set_originator_id(ci, cuc_code)
        sdd = SEPADirectDebit(creditor, sdd_type)

        for count, payment in enumerate(self.payment_ids, start=1):
            payment_line = payment.payment_line_ids[:1]
            partner_bank = payment.partner_bank_id or payment_line.partner_bank_id
            self._sdd_cbi_check_iban(
                partner_bank,
                _("IBAN %(iban)s of %(partner)s is not valid.")
                % {
                    "iban": partner_bank.acc_number or "",
                    "partner": payment.partner_id.name,
                },
            )
            bic = partner_bank.bank_id.bic
            if not bic:
                raise UserError(
                    _("BIC code of bank account %s is not set.")
                    % partner_bank.acc_number
                )

            mandate = payment_line.mandate_id
            if not mandate or mandate.state != "valid" or mandate.scheme != sdd_type:
                raise UserError(
                    _("No valid %(type)s mandate for partner %(partner)s.")
                    % {"type": sdd_type, "partner": payment.partner_id.name}
                )

            try:
                debtor = Account(
                    (partner_bank.sanitized_acc_number, bic), payment.partner_id.name
                )
            except ValueError as e:
                raise UserError(
                    _("Bank account %(iban)s / BIC %(bic)s of %(partner)s: %(err)s")
                    % {
                        "iban": partner_bank.acc_number,
                        "bic": bic,
                        "partner": payment.partner_id.name,
                        "err": e,
                    }
                ) from e
            debtor.set_mandate(
                mref=mandate.unique_mandate_reference,
                signed=mandate.signature_date,
                recurrent=mandate.type == "recurrent",
            )
            communication = payment.memo or payment_line.communication or self.name
            sdd.add_transaction(
                debtor,
                payment.amount,
                f"{communication}_{count}",
                eref=str(count),
                due_date=payment.payment_line_date,
            )

        tmst = fields.Datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{self.name}_{tmst}.xml".replace("/", "-")
        xml_content = sdd.render()
        if isinstance(xml_content, str):
            xml_content = xml_content.encode("utf-8")
        return xml_content, filename
