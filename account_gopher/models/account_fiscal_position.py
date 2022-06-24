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
    "l10n_it.intra": {
        "rc_type_id": "l10n_it_reverse_charge.account_rc_type_3",
    },
    "l10n_it.extra": {
        "rc_type_id": "l10n_it_reverse_charge.account_rc_type_2",
    },
}


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    def gopher_set_fiscal_position(self, html_txt=None):
        html = ""
        if html_txt:
            html += html_txt(_("Set fiscal position"), "h3")
            html += html_txt("", "table")
            html += html_txt("", "tr")
            html += html_txt(_("Description"), "td")
            html += html_txt(_("Action"), "td")
            html += html_txt("", "/tr")

        for xref in ("extra", "intra"):
            xref = "l10n_it_fiscal.%s" % xref
            tmpl = self.env.ref(xref, raise_if_not_found=False)
            if not tmpl:
                xref = "l10n_it.%s" % xref
                tmpl = self.env.ref(xref, raise_if_not_found=False)
            if not tmpl:
                continue
            fpos = self.env["account.fiscal.position"].search(
                [("name", "=", tmpl.name)]
            )
            if fpos:
                vals = {
                    "rc_type_id": self.env.ref(DEFAULT_VALUES[xref]["rc_type_id"]).id
                }
                try:
                    fpos[0].write(vals)
                    actioned = _("Updated")
                    self._cr.commit()  # pylint: disable=invalid-commit
                except BaseException as e:
                    self._cr.rollback()  # pylint: disable=invalid-commit
                    actioned = _u("** %s **" % e)
            if html_txt and actioned:
                html += html_txt("", "tr")
                html += html_txt(fpos.name, "td")
                html += html_txt(actioned, "td")
                html += html_txt("", "/tr")
        if html_txt:
            html += html_txt("", "/table")
        return html
