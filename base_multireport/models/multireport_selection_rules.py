# -*- coding: utf-8 -*-
#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import api, fields, models

RPT_ACTION = [
    ("odoo", "odoo"),
    ("report", "report"),
    ("company", "company"),
    ("customer", "customer"),
]


@api.model
def _lang_get(self):
    languages = self.env["res.lang"].search([])
    return [(language.code, language.name) for language in languages]


class MultireportSelectionRules(models.Model):
    _name = "multireport.selection.rules"
    _description = "Rules to select report name"
    _order = "sequence"

    name = fields.Char(
        "Rule Name", required=True, help="Brief name of document to print"
    )
    model_id = fields.Many2one(
        "ir.model",
        "Related Document Model",
        # domain=[('osv_memory', '=', False)],
        domain=[("transient", "=", False)],
        help="Model to apply this rule",
    )
    model_name = fields.Char(
        "Related Document Model", help="Model to apply this rule (no matches if exists)"
    )
    report_id = fields.Many2one(
        "ir.ui.view",
        "Report to print",
        domain=[("type", "=", "qweb"), ("inherit_id", "=", False)],
        help="Report to print if action is 'report'",
    )
    purpose = fields.Char("Purpose", help="Report purpose: why, when use this report.")
    sequence = fields.Integer(
        "sequence",
        help="Rules are evaluated starting from lower sequence. "
        "Please, use values above 100 for default rules, "
        "from 10 to 100 for ordinary rules."
        "Sequences below 10 must be very important!",
    )
    action = fields.Selection(
        RPT_ACTION,
        "report action",
        help="Set 'report' to get the internal report name field,"
        " 'company' to get preferred model of company (if any),"
        " 'customer' to get preferred model of customer (if any),"
        " 'odoo' to execute Odoo standard document printing.",
    )
    journal_id = fields.Many2one(
        "account.journal",
        "If journal",
        help="Apply rule only if journal matches document;"
        " may be useful to print commercial invoices"
        " like Italian 'Fattura Accompagnatoria'.",
    )
    partner_id = fields.Many2one(
        "res.partner",
        "If partner",
        help="Apply rule only if document of partner;"
        " may be useful to print specific model for partner.",
    )
    lang = fields.Selection(
        _lang_get,
        "If language",
        help="Apply rule only if language matches customer;"
        " may be useful to print untranslated report models.",
    )
    position_id = fields.Many2one(
        "account.fiscal.position",
        "If fiscal position",
        help="Apply rule only if fiscal position matches"
        " invoice position; may be useful to print"
        " models to satisfy some fiscal law.",
    )
    since_date = fields.Date("From date")
    until_date = fields.Date("To date")
    active = fields.Boolean("Active", help="Rule is evaluated only if is active.")
