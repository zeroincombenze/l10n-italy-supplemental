# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import datetime
import logging

from odoo import api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


TYPE2JOURNAL12 = {
    "out_invoice": "sale",
    "in_invoice": "purchase",
    "out_refund": "sale",
    "in_refund": "purchase",
    "entry": "general",
}
TYPE2JOURNAL = {
    "out_invoice": "sale",
    "in_invoice": "purchase",
    "out_refund": "sale_refund",
    "in_refund": "purchase_refund",
    "entry": "general",
}
JOURNAL2TYPE = {
    "sale": ["out_invoice", "out_refund"],
    "purchase": ["in_invoice", "in_refund"],
    "sale_refund": ["out_refund"],
    "purchase_refund": ["in_refund"],
}
VAT_DOCUMENTS = ["out_invoice", "in_invoice", "out_refund", "in_refund"]


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def get_actual_val(self, vals, name, layer=None, ttype=None):
        """Get real value from vals or from record
        @layer: 'onchange', 'create', 'write', 'validate', 'post'
        @ttype: 'company', 'company_id', 'many2one', 'id', 'date', 'datetime'
        """
        if name in vals:
            if ttype == "date" and vals[name] and isinstance(vals[name], str):
                return datetime.datetime.strptime(vals[name], "%Y-%m-%d").date()
            elif (
                isinstance(vals[name], int)
                and hasattr(self, name)
                and ttype in ("company", "many2one")
            ):
                return getattr(self, name).browse(vals[name])
            return vals[name]
        elif self and len(self) == 1:
            if ttype == "company":
                if self[name]:
                    return self[name]
                return self.env.user.company_id
            elif ttype == "many2one":
                if self[name]:
                    return self[name]
                return False
            elif ttype == "company_id":
                if self[name]:
                    return self[name].id
                return self.env.user.company_id.id
            elif ttype == "id":
                if self[name]:
                    return self[name].id
                return False
            else:
                return self[name]
        elif ttype == "company":
            return self.env.user.company_id
        elif ttype == "company_id":
            return self.env.user.company_id.id
        return False

    @api.model
    def show_error(self, vals, message, title, layer=None):
        if layer != "onchange":
            raise UserError(message)
        warning_mess = {"title": title, "message": message}
        return {
            "warning": warning_mess,
            "values": vals,
        }

    @api.model
    def ret_by_layer(self, vals, layer=None):
        if layer != "onchange":
            return vals
        return {
            "values": vals,
        }

    @api.model
    def check_n_set(self, vals, layer=None):
        # TODO> WARNING! this code is a patch to validate
        # Need to check for actual reason of error
        journal = self.get_actual_val(vals, "journal_id", ttype="many2one", layer=layer)
        if not journal and not self:
            return vals
        if (
                hasattr(journal, "rev_charge")
                and journal.rev_charge
        ):
            return vals
        if journal and journal.type == "sale":
            date_rec = self.get_actual_val(
                vals, "invoice_date", ttype="date", layer=layer
            )
        else:
            date_rec = self.get_actual_val(vals, "date", ttype="date", layer=layer)
        if not date_rec and not self:
            return vals
        if journal and journal.type == "purchase":
            date_doc = self.get_actual_val(
                vals, "invoice_date", ttype="date", layer=layer
            )
            if (
                not date_doc
                and self.type != "entry"
                and layer in ("onchange", "validate", "post")
            ):
                return self.show_error(
                    vals, "Manca data documento", "Data documento!", layer=layer
                )
            # if date_doc and date_rec and date_doc > date_rec:
            #     return self.show_error(
            #         vals,
            #         'Data documento successiva alla data di registrazione',
            #         'Data documento!', layer=layer)
            ref = self.get_actual_val(vals, "ref", layer=layer)
            if not ref and layer in ("onchange", "validate", "post"):
                return self.show_error(
                    vals,
                    "Manca riferimento fornitore",
                    "Riferimento fornitore!",
                    layer=layer,
                )
        fiscalyear = self.get_actual_val(
            vals, "fiscalyear_id", ttype="many2one", layer=layer
        )
        if fiscalyear and fiscalyear.state == "done":
            return self.show_error(
                vals, "Periodo contabile chiuso", "Periodo contabile!", layer=layer
            )
        if not date_rec:
            if layer != "validate":
                return self.ret_by_layer(vals, layer=layer)
            date_rec = datetime.date.today()
        company_id = self.get_actual_val(
            vals, "company_id", ttype="company_id", layer=layer
        )
        if not fiscalyear:
            fys = self.env["account.fiscal.year"].search(
                [
                    ("date_from", "<=", date_rec),
                    ("date_to", ">=", date_rec),
                    ("company_id", "=", company_id),
                    ("state", "!=", "done"),
                ]
            )
            if fys:
                vals["fiscalyear_id"] = fys[0].id
            elif layer == "validate":
                return self.show_error(
                    vals,
                    "Impostare esercizio contabile",
                    "Periodo contabile!",
                    layer=layer,
                )
            return self.ret_by_layer(vals, layer=layer)
        if fiscalyear.date_from <= date_rec <= fiscalyear.date_to:
            return self.ret_by_layer(vals, layer=layer)
        return self.show_error(
            vals,
            "Data fuori limiti esercizio contabile",
            "Data contabile!",
            layer=layer,
        )

    @api.onchange("fiscalyear_id", "date")
    def _onchange_date_fiscalyear_id(self):
        return self.check_n_set({}, layer="onchange")

    @api.onchange("type")
    def _onchange_type(self):
        """
        Filter the journals selectable for the move based on the
        move type, company and currency
        """

        if self.type:

            # Shortcuts
            journal_model = self.env["account.journal"]
            inv_type = self.type
            company = self.company_id or self.env.user.company_id
            company_id = company.id
            company_currency_id = company.currency_id.id
            context_currency_id = self._context.get("default_currency_id")

            # Ensure inv_type is in TYPE2JOURNAL,
            # if it is not there is something bad!
            assert inv_type in TYPE2JOURNAL, (
                "Il tipo di registrazione {} non ha un giornale associato."
                "Tipi conosciuti: {}".format(inv_type, TYPE2JOURNAL.keys())
            )

            # Filter journals by journal_type
            if inv_type in VAT_DOCUMENTS:
                journal_type_filter = ("type", "=", TYPE2JOURNAL12[inv_type])
            else:
                journal_types = [TYPE2JOURNAL12[ty] for ty in VAT_DOCUMENTS]
                journal_type_filter = ("type", "not in", journal_types)
            # end if

            domain_jt_comp = [journal_type_filter, ("company_id", "=", company_id)]

            # Filter journals by currency:
            # - if 'default_currency_id' is set in context and is different
            #   from company currency select only journals with currency
            #   matching 'default_currency_id'
            # - else select journals with currency matching the company
            #   currency OR with currency NOT set
            currency_id = context_currency_id or company_currency_id
            if currency_id == company_currency_id:
                domain_curr = [
                    "|",
                    ("currency_id", "=", False),
                    ("currency_id", "=", currency_id),
                ]
            else:
                domain_curr = [("currency_id", "=", currency_id)]
            # end if

            # Retrieve the list of journals suitable to be used as default,
            # that is journals matching the selected:
            # - journal_type
            # - company
            # - currency
            journals = journal_model.search(
                domain_jt_comp + domain_curr
            ) or journal_model.search(domain_jt_comp)

            # Ensure a suitable journal is set
            if not self.journal_id or self.journal_id not in journals:
                if journals:
                    self.journal_id = journals[0]
                else:
                    self.journal_id = False
            # end if

            # Return the filter to restrict the selectable journals
            return {"domain": {"journal_id": domain_jt_comp}}
        # end if

    # end _onchange_type

    @api.multi
    def post(self, invoice=False):
        for move in self:
            vals = {}
            if invoice:

                vals["type"] = invoice.type
                move.type = invoice.type

                vals["invoice_date"] = invoice.date_invoice
                move.invoice_date = invoice.date_invoice

                vals["fiscalyear_id"] = invoice.fiscalyear_id.id
                move.fiscalyear_id = invoice.fiscalyear_id.id

            # end if

            move.check_n_set(vals, layer="post")

            # validation about partner if required
            # raise error (and stop transaction)
            if move.line_ids:
                message = (
                    "Per questo tipo di conto è neccessario impostare " "il partner."
                )
                for line in move.line_ids:

                    if line.check_partner() is False:
                        message = line.account_id.code + " " + message
                        raise UserError(message)
                    # end if

                # end for
            # end if
        return super().post(invoice=invoice)

    # end post

    @api.model
    def create(self, vals):
        is_invoice = False
        if self.env.context.get("type") in (
            "out_invoice",
            "in_invoice",
            "out_refund",
            "in_refund",
        ):
            is_invoice = True
        if self.env.context.get("journal_type") in ("sale", "purchase"):
            is_invoice = True
        if is_invoice:
            if "fiscalyear_id" not in vals or not vals["fiscalyear_id"]:
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

            # vals = self.check_n_set(vals, layer='create')

        res = super().create(vals)
        return res

    # end create

    @api.multi
    def write(self, vals):
        super().write(vals)
        #
        # verrà impostato l'anno fiscale in caso di dato assente nella
        # registrazione
        #
        if not self.env.context.get("StopRecursion_lit_validation"):
            for move in self:
                move = move.with_context(StopRecursion_lit_validation=True)
                if not move.fiscalyear_id:
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
                        # vals['fiscalyear_id'] = fiscalyears[0].id
        # vals = self.check_n_set(vals, layer='write')

    # end write


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def check_partner(self):
        types = self.env["account.account.type"].search(
            [("type", "in", ["receivable", "payable"])]
        )
        return bool(
            # Not payable neither receivable account
            self.account_id.user_type_id not in types
            # or valid partner
            or self.partner_id
            # No fiscal year closing record
            or ("fyc_id" in self.move_id
                and self.move_id.fyc_id)
        )

    @api.onchange("account_id")
    def _onchange_account_id(self):
        if not self.account_id:
            return
        # if self.account_id.is_parent:
        #     self.account_id = False
        #     warning_mess = {
        #         "title": "Tipo non accettabile!",
        #         "message": "Usare solo sottoconti",
        #     }
        #     return {"warning": warning_mess}

        has_partner = self.check_partner()
        if has_partner is False:
            warning_mess = {
                "title": "Partner non impostato!",
                "message": "Per questo tipo di conto è "
                "neccessario impostare il partner.",
            }
            return {"warning": warning_mess}
        # return super()._onchange_account_id()
