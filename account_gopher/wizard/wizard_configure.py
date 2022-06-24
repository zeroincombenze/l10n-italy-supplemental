# -*- coding: utf-8 -*-
#
# Copyright 2020-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from odoo import api, fields, models, _


class GopherConfigureWizard(models.TransientModel):
    """No yet documented"""

    _name = "gopher.configure.wizard"
    _description = "Configure Account Environment"

    def _default_fiscal_position(self):
        return self.env["fatturapa.fiscal_position"].search([("code", "=", "RF01")])[0]

    fiscal_position_id = fields.Many2one(
        "fatturapa.fiscal_position",
        "Fiscal Position",
        default=_default_fiscal_position,
        required=True,
        help="Fiscal position used by electronic invoice",
    )
    reload_from_coa = fields.Selection(
        [
            ("tax", "Tax codes"),
            ("coa", "Chart of Account"),
            ("both", "Tax & CoA codes"),
        ],
        "Reload CoA and Tax codes",
    )
    set_rc_config = fields.Boolean(
        "Set reverse charge configuration",
    )
    tax_config = fields.Boolean(
        "Set tax configuration",
    )
    tracelog = fields.Html("Result History")

    @api.multi
    def html_txt(self, text, tag):
        if tag:
            if tag in ("table", "/table", "tr", "/tr"):
                if not text and tag == "table":
                    text = 'border="2px" cellpadding="2px" style="padding: 5px"'
                if text:
                    html = "<%s %s>" % (tag, text)
                elif tag.startswith("/"):
                    html = "<%s>\n" % tag
                else:
                    html = "<%s>" % tag
            else:
                html = "<%s>%s</%s>" % (tag, text, tag)
        else:
            html = text
        return html

    @api.multi
    def account_wizard(self):
        tracelog = self.html_txt(_("Result"), "h2")
        if (
            self.env.user.company_id.fatturapa_fiscal_position_id
            != self.fiscal_position_id
        ):
            self.env.user.company_id.fatturapa_fiscal_position_id = (
                self.fiscal_position_id
            )
            tracelog += self.html_txt(
                "Set fiscal position %s" % self.fiscal_position_id.code, "div"
            )
        if self.reload_from_coa in ("coa", "both"):
            tracelog += self.env["account.account"].gopher_reload_coa(
                html_txt=self.html_txt
            )
        if self.reload_from_coa in ("tax", "both"):
            tracelog += self.env["account.tax"].gopher_reload_taxes(
                html_txt=self.html_txt
            )
        if self.set_rc_config:
            tracelog += self.env["account.rc.type"].gopher_set_rc_type(
                html_txt=self.html_txt)
            tracelog += self.env["account.fiscal.position"].gopher_set_fiscal_position(
                html_txt=self.html_txt)
        if self.tax_config:
            tracelog += self.env["account.tax"].gopher_configure_tax(
                html_txt=self.html_txt)
        self.tracelog = tracelog
        return {
            "name": "Configuration result",
            "type": "ir.actions.act_window",
            "res_model": "gopher.configure.wizard",
            "view_type": "form",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
            "context": {"active_id": self.id},
            "view_id": self.env.ref("account_gopher.result_wizard_configure_view").id,
            "domain": [("id", "=", self.id)],
        }

    def close_window(self):
        return {"type": "ir.actions.act_window_close"}
