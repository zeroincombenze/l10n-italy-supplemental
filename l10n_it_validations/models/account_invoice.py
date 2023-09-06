# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging

from odoo import api, models, fields
from odoo.exceptions import UserError

from ..utils.validation_result import ValidationResult

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def invoice_validate(self):

        for invoice in self:

            # Set defaults
            invoice.setdefault_date()
            invoice.setdefault_fiscalyear()

            # Ensure everything is set
            invoice.validate_fiscalyear_is_set().on_err_raise()
            invoice.validate_fiscalyear_not_closed().on_err_raise()
            invoice.validate_date_invoice_is_set().on_err_raise()
            invoice.validate_date_is_set().on_err_raise()

            # Validate 'date_invoice' (data fattura)
            invoice.validate_date_invoice().on_err_raise()

            # Validate 'date' (data registrazione)
            invoice.validate_date().on_err_raise()
            invoice.validate_genericdate_fiscalyear(
                date_field_name='date').on_err_raise()

            # If incoming and generate from e_invoice validate
            # the date field against e_invoice data
            invoice.validate_date_e_invoice().on_err_raise()

            # Validate payment term zero amount
            invoice.validate_payment_term_zero_amount().on_err_raise()

        # end for

        return super().invoice_validate()

    # end invoice_validate

    @api.multi
    def action_date_assign(self):
        """Check and/or assign date_invoice & date"""
        for invoice in self:
            if (
                hasattr(invoice.journal_id, "rev_charge")
                and invoice.journal_id.rev_charge
            ):
                continue
            if invoice.type in ("in_invoice", "in_refund"):
                if not invoice.date_invoice:
                    raise UserError("Attenzione!\nImpostare la data fattura.")
                # end if
                if not invoice.date:
                    invoice.date = invoice.date_invoice
                # end if
            elif invoice.type in ("out_invoice", "out_refund"):
                if not invoice.date_invoice:
                    invoice.date_invoice = fields.Date.context_today(self)
                # end if
                invoice.date = invoice.date_invoice
            # end if
        return super().action_date_assign()
    # end action_date_assign

    @api.multi
    def action_move_create(self):
        for invoice in self:

            if invoice.type in ("out_invoice", "out_refund") and (
                not hasattr(invoice.journal_id, "rev_charge")
                or not invoice.journal_id.rev_charge
            ):
                if not invoice.date:
                    invoice.date = invoice.date_invoice
                else:
                    if invoice.date != invoice.date_invoice:
                        raise UserError(
                            "La data contabile deve essere uguale alla data "
                            "del documento"
                        )
                    # end if
                # end if
            # end if

            if not invoice.fiscalyear_id:
                fiscalyear_id = self.env["account.fiscal.year"].search(
                    [
                        ("date_from", "<=", invoice.date),
                        ("date_to", ">=", invoice.date),
                        ("company_id", "=", invoice.company_id.id),
                    ],
                )
                if fiscalyear_id:
                    invoice.fiscalyear_id = fiscalyear_id.id
                else:
                    raise UserError(
                        "Non è stato impostato l'anno contabile conforme "
                        "alla data del documento."
                    )

                # end if
            # end if

            if invoice.type in ("in_invoice", "in_refund"):
                if invoice.date < invoice.date_invoice:
                    raise UserError(
                        "La data contabile deve essere maggiore o uguale alla"
                        " data del documento"
                    )
                # end if
            # end if
        # end for

        res = super().action_move_create()

        return res
    # end action_move_create

    @api.model
    def create(self, vals):
        if "fiscalyear_id" in vals and not vals["fiscalyear_id"]:
            fiscal = self.env["account.fiscal.year"].search(
                [
                    ("date_from", "<=", vals["date"]),
                    ("date_to", ">=", vals["date"]),
                    ("company_id", "=", self.env.user.company_id.id),
                    ("state", "!=", "done"),
                ]
            )
            if fiscal:
                vals["fiscalyear_id"] = fiscal[0].id
            # end if
        # end if

        return super().create(vals)
    # end create

    @api.multi
    def write(self, vals):

        # Save vals
        super().write(vals)

        # Set default values, but avoid the "infinite
        # recursive calls to write" issue
        if not self.env.context.get("StopRecursion"):
            for invoice in self:
                invoice = invoice.with_context(StopRecursion=True)
                invoice.setdefault_date()
                invoice.setdefault_fiscalyear()

                # If invoice is e_invoice and date missing set default for
                # date from e_invoice data
                invoice.setdefault_date_e_invoice()

                # No validation performed in "write" methods since validations
                # are performed by @api.constraints methods defined below.

            # end for
        else:
            return
        # end if
    # end write

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # CONSTRAINTS - begin

    @api.one
    @api.constrains("fiscalyear_id")
    def _constraint_fy(self):
        self.validate_fiscalyear_not_closed().on_err_raise()
    # end _constraint_fy

    @api.one
    @api.constrains("date_invoice")
    def _constraint_date_invoice(self):
        if self.state not in ("draft", "cancel"):
            self.validate_date_invoice_is_set().on_err_raise()
            self.validate_date_invoice().on_err_raise()
        # end if
    # end _constraint_date_invoice

    @api.one
    @api.constrains("date")
    def _constraint_date(self):
        if self.state not in ("draft", "cancel"):
            self.validate_date_e_invoice().on_err_raise()
        # end if

    # end _constraint_date

    # CONSTRAINTS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # ONCHANGE - begin

    @api.onchange("fiscalyear_id")
    def _onchange_fiscalyear_id(self):

        ck_f = self.validate_fiscalyear_not_closed().on_err_warn()

        ck_d = self.validate_genericdate_fiscalyear(
            date_field_name="date"
        ).on_err_warn()

        return ck_f or ck_d or None

    # end _onchange_date_fiscalyear_id

    @api.onchange("date_invoice")
    def _onchange_date_invoice(self):

        # Update date
        if self.type in ("out_invoice", "out_refund") and (
            not hasattr(self.journal_id, "rev_charge") or not self.journal_id.rev_charge
        ):
            self.date = self.date_invoice
        # end if

        # Update date, date_apply_vat and fiscalyear
        self.fiscalyear_id = self._search_fy(self.date_invoice) or False

        res = super()._onchange_date_invoice()
        return res
    # end _onchange_date_invoice

    @api.onchange("date")
    def _onchange_date(self):
        res = {}
        if self.fiscalyear_id:
            fy_name = self.fiscalyear_id.name
            fy_from = self.fiscalyear_id.date_from
            fy_to = self.fiscalyear_id.date_to

            if not (fy_from <= self.date <= fy_to):
                # Get the descriptive name of the field translated in
                # the current UI lang
                error_msg = (
                    "La data di registrazione deve essere all'interno "
                    "del periodo contabile "
                    "selezionato ({}).".format(fy_name)
                )
                raise UserError(error_msg)

        if self.journal_id and self.date and self.date_invoice:

            # Journal type is used to determine if the invoice is
            # for a purchase or for sell
            journal_type = self.journal_id.type

            if hasattr(self.journal_id, "rev_charge"):
                is_rev_charge = self.journal_id.rev_charge
            else:
                is_rev_charge = False

            # For sale invoices 'Date' and 'Invoice Date' must have
            # the same value.
            if (
                journal_type in ("sale", "sale_refound")
                and not is_rev_charge
                and not (self.date == self.date_invoice)
            ):
                res["warning"] = {
                    "title": "Attenzione!",
                    "message": "Nelle fatture di vendita la data di "
                    "registazione deve essere uguale alla data "
                    "fattura!",
                }
                res["value"] = {
                    "date": self.date_invoice,
                    "date_apply_vat": self.date_invoice,
                    "date_apply_balance": self.date_invoice,
                }
            # For purchase invoices 'Date' must be >= 'Invoice Date'
            elif (
                journal_type in ("purchase", "purchase_refound") or is_rev_charge
            ) and not (self.date >= self.date_invoice):
                res["warning"] = {
                    "title": "Attenzione!",
                    "message": "La data di registrazione della fattura non può "
                    "precedere la data fattura.",
                }
                res["value"] = {
                    "date": self._origin.date,
                    "date_apply_vat": self._origin.date_apply_vat,
                    "date_apply_balance": self._origin.date_apply_balance,
                }

            # end if
        return res

    # end _onchange_date

    # ONCHANGE - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # VALIDATION METHODS - begin

    @api.model
    def validate_genericdate_fiscalyear(self, date_field_name):

        date_field = getattr(self, date_field_name)

        # Perform the check only if the date_field is actually set!
        if self.fiscalyear_id and date_field:

            fy_name = self.fiscalyear_id.name
            fy_from = self.fiscalyear_id.date_from
            fy_to = self.fiscalyear_id.date_to

            if not (fy_from <= date_field <= fy_to):
                # Get the name of the field translated in the current UI lang
                date_field_desc = self.env["ir.translation"].get_field_string(
                    self._name
                )[date_field_name]
                error_msg = (
                    "La data '{}' deve essere all'interno del periodo"
                    " contabile selezionato ({}).".format(date_field_desc, fy_name)
                )
                return ValidationResult(
                    passed=False, title=date_field_desc, msg=error_msg
                )
            # end if

        # end if

        return ValidationResult()

    # end validate_genericdate_fiscalyear

    @api.model
    def validate_fiscalyear_not_closed(self):
        if self.fiscalyear_id and self.fiscalyear_id.state == "done":
            return ValidationResult(
                passed=False,
                title="Periodo contabile!",
                msg="Periodo contabile chiuso",
            )
        # end if

        return ValidationResult()

    # end validate_fiscalyear_not_closed

    @api.model
    def validate_fiscalyear_is_set(self):
        if not self.fiscalyear_id:
            return ValidationResult(
                passed=False,
                title="Periodo contabile!",
                msg="Impostare il periodo contabile",
            )
        # end if

        return ValidationResult()

    # end validate_fiscalyear_is_set

    @api.model
    def validate_date_is_set(self):
        if not self.date:
            return ValidationResult(
                passed=False,
                title="Data registrazione!",
                msg="Manca data registrazione",
            )
        # end if

        return ValidationResult()

    # end validate_date

    @api.model
    def validate_date_invoice_is_set(self):
        # Ensure date_invoice is set
        if not self.date_invoice:
            return ValidationResult(
                passed=False, title="Data fattura!", msg="Manca data fattura"
            )
        # end if

        return ValidationResult()

    # end validate_date_invoice_is_set

    @api.model
    def validate_date_invoice(self):
        return ValidationResult()

    # end validate_date_invoice

    @api.model
    def validate_date(self):
        # Ensure we have all the required data to perform the validation
        if self.journal_id and self.date and self.date_invoice:

            # Journal type is used to determine if the invoice is
            # for a purchase or for sell
            journal_type = self.journal_id.type

            if hasattr(self.journal_id, "rev_charge"):
                is_rev_charge = self.journal_id.rev_charge
            else:
                is_rev_charge = False

            # For sale invoices 'Date' and 'Invoice Date' must have the same value.
            if (
                journal_type in ("sale", "sale_refound")
                and not is_rev_charge
                and not (self.date == self.date_invoice)
            ):
                return ValidationResult(
                    passed=False,
                    title="Data registrazione",
                    msg="Nelle fatture di vendita la data di registazione"
                    " deve essere uguale alla data fattura!",
                )

            # For purchase invoices 'Date' must be >= 'Invoice Date'
            elif (
                journal_type in ("purchase", "purchase_refound") or is_rev_charge
            ) and not (self.date >= self.date_invoice):
                return ValidationResult(
                    passed=False,
                    title="Data registrazione fattura!",
                    msg="La data di registrazione della fattura non "
                    "può precedere la data fattura",
                )

            else:
                pass
            # end if

        # end if

        return ValidationResult()

    # end validate_date

    @api.model
    def validate_date_e_invoice(self):
        """
        If the document is an inbound document from e_invoice
        ensure "date" >= "e_invoice_received_date"
        """
        if (
                hasattr(self, "rc_self_invoice_id")
                and self._context.get('autofattura', False) is False
                and self.rc_self_invoice_id is False
        ):

            # Check if document is an incoming document
            is_in_doc = self.type in ("in_invoice", "in_refund")

            # Check if document has been generated from e_invoice
            from_e_invoice = (
                hasattr(self, "e_invoice_received_date")
                and self.e_invoice_received_date
            )

            # Check if journal is set and is purchase
            journal_ok = self.journal_id and self.journal_id.type == "purchase"

            # Perform validation
            if is_in_doc and from_e_invoice and journal_ok:

                date_valid = self.date >= self.e_invoice_received_date

                if not date_valid:
                    return ValidationResult(
                        passed=False,
                        title="Data registrazione",
                        msg="Nel caso di importazione di fattura elettronica la "
                        '"Data di registrazione" deve essere successiva alla '
                        "data riportata nella fattura elettronica",
                    )
                # end if
            # end if
        # end if

        return ValidationResult(passed=True)

    # end validate_date_e_invoice

    @api.model
    def validate_reference(self):
        # Purchase invoices only!
        if self.journal.type == "purchase" and not self.reference:
            return ValidationResult(
                passed=False,
                title="Riferimento fornitore!",
                msg="Manca riferimento fornitore",
            )
        # end if

        return ValidationResult()

    # end validate_reference

    @api.model
    def validate_payment_term_zero_amount(self):
        total = 0.0
        for line in self.invoice_line_ids:
            total += line.price_subtotal
        if self.payment_term_id and self.currency_id.is_zero(total):
            return ValidationResult(
                passed=False,
                title="Importo fattura a zero!",
                msg="Per le fatture ad importo zero il termine di pagamento "
                "non è permesso.",
            )
            # end if

        return ValidationResult()

    # end validate_payment_term_zero_amount

    # VALIDATION METHODS - end
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @api.model
    def setdefault_date(self):
        # Set default for missing dates
        self.date = self.date or self.date_invoice

    # end _set_default_date

    @api.model
    def setdefault_fiscalyear(self):
        # Set fiscal year if missing
        if not self.fiscalyear_id and self.date_invoice:
            self.fiscalyear_id = self._search_fy(self.date_invoice) or False
        # end if

    # end _set_default_fiscalyear

    @api.model
    def setdefault_date_e_invoice(self):
        """
        If the document is an inbound document from e_invoice
        override the "date" field.
        """

        # Check if document is an incoming document
        is_in_doc = self.type in ("in_invoice", "in_refund")

        # Check if document has been generated from e_invoice
        from_e_invoice = hasattr(self, "e_invoice_received_date")

        # Check if journal is set and is purchase
        journal_ok = self.journal_id and self.journal_id.type == "purchase"

        # Override date field with the date from e_invoice
        if is_in_doc and from_e_invoice and journal_ok and not self.date:
            self.date = self.e_invoice_received_date
        # end if

    # end _sdi_default_date

    @api.model
    def _search_fy(self, search_date):

        fiscalyears = self.env["account.fiscal.year"].search(
            [
                ("date_from", "<=", search_date),
                ("date_to", ">=", search_date),
                ("company_id", "=", self.company_id.id),
                ("state", "!=", "done"),
            ],
            limit=1,
        )

        if fiscalyears:
            return fiscalyears[0].id
        else:
            return None


# class AccountInvoiceLine(models.Model):
#     _inherit = "account.invoice.line"
#
#     @api.onchange("account_id")
#     def _onchange_account_id(self):
#         if not self.account_id:
#             return
#         if self.account_id.is_parent:
#             self.account_id = False
#             warning_mess = {
#                 "title": "Tipo non accettabile!",
#                 "message": "Usare solo sottoconti",
#             }
#             return {"warning": warning_mess}
#         return super()._onchange_account_id()
