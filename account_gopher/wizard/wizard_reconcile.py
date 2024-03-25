# -*- coding: utf-8 -*-
#
# Copyright 2020-24 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from odoo import _, api, fields, models


class GopherReconcileWizard(models.TransientModel):
    """No yet documented"""

    _name = "gopher.reconcile.wizard"
    _description = "Account Reconciliation Assistant"

    account_id = fields.Many2one(
        "account.account",
        "Account to reconcile",
        domain=[("reconcile", "=", True)],
        required=True,
        help="Account to reconcile automatically. Must be reconcilable account",
    )
    partner_id = fields.Many2one(
        "res.partner",
        "Reconcile only partner",
        help="Select partner if you want reconcile only one specific partner",
    )
    reconcile_anonymous = fields.Boolean(
        "Reconcile anonymous moves",
        default=False,
        help="Reconcile moves without partner"
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

    def reconcile_moves(self, reconcile_anonymous=False):
        Partner = self.env["res.partner"]
        Line = self.env["account.move.line"]
        html = ""
        query = (
            "SELECT p.name,l.partner_id"
            " FROM account_account a,account_move_line l,res_partner p"
            " WHERE a.id=l.account_id AND p.id=l.partner_id AND a.reconcile is true")
        if self.partner_id:
            query += " AND p.id=%d" % self.partner_id.id
        else:
            query += " AND l.partner_id is not null"
        query += " GROUP BY p.name,l.partner_id ORDER BY p.name"
        self._cr.execute(query)
        for result in self._cr.fetchall():
            partner = Partner.browse(result[1])
            if not partner.name and not partner.commercial_partner_id.name:
                continue
            header = False
            for line in Line.search([
                ("account_id", "=", self.account_id.id),
                ("partner_id", "=", partner.id),
                ("reconciled", '=', False),
            ], order="date"):
                line_to_reconcile = False
                if line.credit:
                    line_to_reconcile = Line.search([
                        ("account_id", "=", self.account_id.id),
                        ("partner_id", "=", partner.id),
                        ("reconciled", '=', False),
                        ("debit", "=", line.credit),
                    ], limit=1)
                elif line.debit:
                    line_to_reconcile = Line.search([
                        ("account_id", "=", self.account_id.id),
                        ("partner_id", "=", partner.id),
                        ("reconciled", '=', False),
                        ("credit", "=", line.debit),
                    ], limit=1)
                if not line_to_reconcile:
                    if line.credit:
                        line_to_reconcile = Line.search([
                            ("account_id", "=", self.account_id.id),
                            ("partner_id", "=", False),
                            ("reconciled", '=', False),
                            ("debit", "=", line.credit),
                        ], limit=1)
                    elif line.debit:
                        line_to_reconcile = Line.search([
                            ("account_id", "=", self.account_id.id),
                            ("partner_id", "=", False),
                            ("reconciled", '=', False),
                            ("credit", "=", line.debit),
                        ], limit=1)
                    if line_to_reconcile:
                        line_to_reconcile.write({"partner_id": partner.id})
                if line_to_reconcile:
                    if not header:
                        html += self.html_txt(
                            partner.commercial_partner_id.name[:60], "h3"
                        )
                        header = True
                    Line.reconcile([line, line_to_reconcile])
                    html += self.html_txt(
                        "%s -> %s (%.2f)" % (
                            line.move_id.name,
                            line_to_reconcile.move_id.name,
                            line.debit or line.credit), "p"
                    )
        return html

    @api.multi
    def reconcile_wizard(self):
        tracelog = self.html_txt(_("Result"), "h2")

        tracelog += self.reconcile_moves()
        if self.reconcile_anonymous:
            tracelog += self.reconcile_moves(
                reconcile_anonymous=self.reconcile_anonymous)

        self.tracelog = tracelog
        return {
            "name": "Reconciliation result",
            "type": "ir.actions.act_window",
            "res_model": "gopher.reconcile.wizard",
            "view_type": "form",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
            "context": {"active_id": self.id},
            "view_id": self.env.ref("account_gopher.result_wizard_reconcile_view").id,
            "domain": [("id", "=", self.id)],
        }

    def close_window(self):
        return {"type": "ir.actions.act_window_close"}
