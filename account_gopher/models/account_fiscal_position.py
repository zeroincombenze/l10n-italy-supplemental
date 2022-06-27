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
    "l10n_it_fiscal.intra": {
        "rc_type_id": "l10n_it_reverse_charge.account_rc_type_3",
    },
    "l10n_it_fiscal.extra": {
        "rc_type_id": "l10n_it_reverse_charge.account_rc_type_2",
    },
    "l10n_it.intra": {
        "rc_type_id": "l10n_it_reverse_charge.account_rc_type_3",
    },
    "l10n_it.extra": {
        "rc_type_id": "l10n_it_reverse_charge.account_rc_type_2",
    },
}


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    def gopher_configure_fiscalpos(self, html_txt=None):
        company = self.env.user.company_id
        html = ""
        if html_txt:
            html += html_txt(_("Set fiscal position"), "h3")
            html += html_txt("", "table")
            html += html_txt("", "tr")
            html += html_txt(_("Description"), "td")
            html += html_txt(_("Action"), "td")
            html += html_txt("", "/tr")

        fiscalpos_model = self.env["account.fiscal.position"]

        for xref in ("extra", "intra"):
            xref = "l10n_it_fiscal.%s" % xref
            tmpl = self.env.ref(xref, raise_if_not_found=False)
            if not tmpl:
                xref = "l10n_it.%s" % xref
                tmpl = self.env.ref(xref, raise_if_not_found=False)
            if not tmpl:
                continue
            fiscalpos = fiscalpos_model.search(
                [("company_id", "=", company.id), ("name", "=", tmpl[0].name)]
            )
            if fiscalpos:
                vals = {
                    "rc_type_id": self.env.ref(DEFAULT_VALUES[xref]["rc_type_id"]).id
                }
                try:
                    fiscalpos[0].write(vals)
                    actioned = _("Updated")
                    self._cr.commit()  # pylint: disable=invalid-commit
                except BaseException as e:
                    self._cr.rollback()  # pylint: disable=invalid-commit
                    actioned = _u("** %s **" % e)
                if html_txt and actioned:
                    html += html_txt("", "tr")
                    html += html_txt(fiscalpos[0].name, "td")
                    html += html_txt(actioned, "td")
                    html += html_txt("", "/tr")

        for fiscalpos in fiscalpos_model.search([]):
            actioned = ""
            for tax_line in fiscalpos.tax_ids:
                if not tax_line.tax_src_id or not tax_line.tax_dest_id:
                    actioned = "Different tax companies"
                elif (
                    tax_line.tax_src_id.type_tax_use
                    != tax_line.tax_dest_id.type_tax_use
                ):
                    actioned = "Different tax uses"
                if (
                    hasattr(fiscalpos, "rc_type")
                    and fiscalpos.rc_type
                    and tax_line.tax_dest_id.rc_type != fiscalpos.rc_type
                ):
                    actioned = "Invalid RC type for target tax"
                elif hasattr(fiscalpos, "split_payment") and fiscalpos.split_payment:
                    if tax_line.tax_dest_id.payability != "S":
                        actioned = "Invalid SP flag for target tax"
                else:
                    if (
                        hasattr(fiscalpos, "rc_type")
                        and not fiscalpos.rc_type
                        and tax_line.tax_dest_id.rc_type
                    ):
                        actioned = "RC tax for no RC fiscal position"
                    elif (
                        hasattr(fiscalpos, "payability")
                        and tax_line.tax_dest_id.payability == "S"
                    ):
                        actioned = "SP tax for no SP fiscal position"
            if actioned and html_txt:
                html += html_txt("", "tr")
                html += html_txt(fiscalpos.name, "td")
                html += html_txt(actioned, "td")
                html += html_txt("", "/tr")

        if html_txt:
            html += html_txt("", "/table")
        return html
