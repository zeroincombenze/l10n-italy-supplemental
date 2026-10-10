# -*- coding: utf-8 -*-
#
# Copyright 2019-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from datetime import datetime

from odoo import api, fields, models


class ItalyLetteraIntento(models.Model):
    _name = "italy.lettera.intento"

    @api.depends("plafond")
    def _used_plafond(self):
        for lett in self:
            if lett.partner_id and lett.company_id and isinstance(lett.id, (int, long)):
                partner_id = lett.partner_id.id
                company_id = lett.company_id.id
                query = """SELECT SUM(credit) - SUM(debit)
                FROM account_move_line l, account_invoice i
                WHERE
                i.id=l.invoice_id AND
                i.lettera_intento_id=%(lett)d AND
                i.partner_id = %(partner_id)d AND
                i.company_id = %(company_id)d AND
                i.journal_id in (SELECT id FROM account_journal WHERE
                               type='sale' AND company_id=%(company_id)d) AND
                l.account_id in (SELECT id FROM account_account WHERE
                               internal_type='receivable')
                """ % {
                    "company_id": company_id,
                    "partner_id": partner_id,
                    # "date": lett.customer_date,
                    "lett": lett.id,
                }
                self.env.cr.execute(query)
                res = self.env.cr.fetchall()
                amount = 0
                if res[0][0]:
                    amount = -res[0][0]
                lett.plafond_used = amount
                lett.plafond_avaiable = lett.plafond - amount

    name = fields.Char("Name", copy=False)
    date = fields.Date(string="Date")
    date_start = fields.Date()
    date_end = fields.Date()
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.user.company_id
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        domain=["|",
                ("property_account_position_id.lettera_intento", "=", True),
                ("property_account_position_id", "=", False),
                ]
    )
    customer_ref = fields.Char("Customer Ref.")
    customer_date = fields.Date(string="Customer Date")
    customer_autmin = fields.Char("Autorizzazione ministeriale")
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    plafond = fields.Monetary(string="Plafond")
    plafond_used = fields.Monetary(string="Used Plafond", compute=_used_plafond)
    plafond_avaiable = fields.Monetary(string="Avaiable Plafond", compute=_used_plafond)
    active = fields.Boolean(string="Active", default=True)

    @api.multi
    def name_get(self):
        res = []
        for item in self:
            res.append(
                (
                    item.id,
                    "%s - %s"
                    % (item.partner_id and item.partner_id.name or "", item.name),
                )
            )
        return res

    @api.model
    def fiscal_pos_values(self, partner, partner_vals, lett):
        params = {}
        for tgt, src in (("vs.data", "customer_date"), ("ns.data", "date")):
            params[tgt] = ""
            if partner_vals.get(src):
                params[tgt] = datetime.strptime(partner_vals[src], "%Y-%m-%d").strftime(
                    "%d-%m-%Y"
                )
            elif lett:
                params[tgt] = datetime.strptime(lett[src], "%Y-%m-%d").strftime(
                    "%d-%m-%Y"
                )
        for tgt, src in (
            ("vs.prot", "customer_ref"),
            ("ns.prot", "name"),
            ("aut.min", "customer_autmin"),
        ):
            params[tgt] = ""
            if partner_vals.get(src):
                params[tgt] = partner_vals[src]
            elif lett:
                params[tgt] = lett[src]
        return {
            "name": "Lettera intento %s" % partner.name,
            "company_id": partner.company_id.id,
            "lettera_intento": True,
            "note": self.env.user.company_id.text_lettera_intento % params,
        }

    @api.model
    def create_fiscal_pos(self, partner, partner_vals):
        vals = self.fiscal_pos_values(partner, partner_vals, False)
        return self.env["account.fiscal.position"].create(vals)

    @api.model
    def write_fiscal_pos(self, fiscalpos, partner, partner_vals, lett):
        vals = self.fiscal_pos_values(partner, partner_vals, lett)
        return fiscalpos.write(vals)

    @api.model
    def set_fiscalpos_customer(self, vals, lett):
        partner = False
        if vals.get("partner_id"):
            partner = self.env["res.partner"].browse(int(vals["partner_id"]))
        elif lett:
            partner = lett.partner_id
        if partner:
            fiscalpos = partner.property_account_position_id
            if not fiscalpos:
                fiscalpos = self.create_fiscal_pos(partner, vals)
                partner.write({"property_account_position_id": fiscalpos.id})
            else:
                self.write_fiscal_pos(fiscalpos, partner, vals, lett)

    @api.model
    def create(self, vals):
        if not vals.get("name"):
            vals["name"] = (
                self.env["ir.sequence"]
                .with_context(force_company=vals["company_id"])
                .next_by_code("italy.lettera.intento")
            )
        self.set_fiscalpos_customer(vals, False)
        return super(ItalyLetteraIntento, self).create(vals)

    @api.multi
    def write(self, vals):
        self.set_fiscalpos_customer(vals, self)
        return super(ItalyLetteraIntento, self).write(vals)
