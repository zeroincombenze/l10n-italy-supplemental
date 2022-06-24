# -*- coding: utf-8 -*-
#
# Copyright 2020-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from python_plus import _u
from odoo import models, _

DEFAULT_VALUES = {
    "l10n_it_reverse_charge.account_rc_type_1": {
        "name": "Reverse charge locale",
        "description": "Usare per RC locale (italia)",
        "method": "selfinvoice",
        "partner_type": "other",
        "fiscal_document_type_id": "TD16",
    },
    "l10n_it_reverse_charge.account_rc_type_2": {
        "name": "Reverse charge Extra-EU",
        "description": "Usare per RC estero no EU",
        "method": "selfinvoice",
        "partner_type": "other",
        "fiscal_document_type_id": "TD17",
    },
    "l10n_it_reverse_charge.account_rc_type_3": {
        "name": "Reverse charge EU",
        "description": "Usare per RC interna EU",
        "method": "selfinvoice",
        "partner_type": "supplier",
        "fiscal_document_type_id": "TD18",
    },
}


class AccountRCTypeTax(models.Model):
    _inherit = "account.rc.type"

    def get_def_values(self, xref, rc_type):
        company = self.env.user.company_id
        vals = {}
        for name in ("description", "name", "method", "partner_type"):
            def_name = DEFAULT_VALUES[xref][name]
            if getattr(rc_type, name) != def_name:
                vals[name] = def_name
        def_name = DEFAULT_VALUES[xref]["fiscal_document_type_id"]
        if hasattr(self, "fiscal_document_type_id"):
            td = self.env["italy.ade.invoice.type"].search(
                [
                    ("code", "=", def_name),
                ]
            )
            if td and rc_type.fiscal_document_type_id.id != td[0].id:
                vals["fiscal_document_type_id"] = td[0].id
        journal_model = self.env["account.journal"]
        if not rc_type.journal_id:
            domain = [("type", "=", "sale")]
            if hasattr(journal_model, "rev_charge"):
                domain.append(("rev_charge", "=", True))
            journals = journal_model.search(domain)
            if journals:
                journal_id = journals[0].id
                for journal in journals:
                    if "auto" in journal.name.lower():
                        journal_id = journals[0].id
                        break
                vals["journal_id"] = journal_id
        tmp_account_id = rc_type.transitory_account_id.id
        if not rc_type.transitory_account_id:
            acc_model = self.env["account.account"]
            domain = [
                ("company_id", "=", company.id),
                "|",
                ("code", "=", "490050"),
                ("code", "=", "295000")]
            accs = acc_model.search(domain)
            if accs:
                tmp_account_id = accs[0].id
                vals["transitory_account_id"] = tmp_account_id
        if not rc_type.payment_journal_id:
            domain = [
                ("company_id", "=", company.id),
                ("type", "=", "general"),
                ("default_debit_account_id", "=", tmp_account_id),
            ]
            journals = journal_model.search(domain)
            if journals:
                vals["payment_journal_id"] = journals[0].id
            else:
                domain = [
                    ("company_id", "=", company.id),
                    ("type", "=", "general"),
                    ("code", "=", "GCRC"),
                ]
                journals = journal_model.search(domain)
                if journals:
                    vals["payment_journal_id"] = journals[0].id
                    journals[0].default_debit_account_id = tmp_account_id
                    journals[0].default_credit_account_id = tmp_account_id
        if not rc_type.partner_id:
            vals["partner_id"] = self.env.user.company_id.partner_id.id
        return vals

    def gopher_set_rc_type(self, html_txt=None):
        html = ""
        if html_txt:
            html += html_txt(_("Set RC types"), "h3")
            html += html_txt("", "table")
            html += html_txt("", "tr")
            html += html_txt(_("Code"), "td")
            html += html_txt(_("Description"), "td")
            html += html_txt(_("Action"), "td")
            html += html_txt("", "/tr")

        for xref in ("account_rc_type_1", "account_rc_type_2", "account_rc_type_3"):
            xref = "l10n_it_reverse_charge.%s" % xref
            rc_type = self.env.ref(xref)
            vals = self.get_def_values(xref, rc_type)
            if vals:
                try:
                    rc_type.write(vals)
                    actioned = _("Updated")
                    self._cr.commit()  # pylint: disable=invalid-commit
                except BaseException as e:
                    self._cr.rollback()  # pylint: disable=invalid-commit
                    actioned = _u("** %s **" % e)
                if html_txt and actioned:
                    html += html_txt("", "tr")
                    html += html_txt(rc_type.name, "td")
                    html += html_txt(rc_type.description, "td")
                    html += html_txt(actioned, "td")
                    html += html_txt("", "/tr")
        if html_txt:
            html += html_txt("", "/table")
        return html
