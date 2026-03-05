#
# Copyright 2019-23 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import api, fields, models

import odoo.addons.decimal_precision as dp


class ItalyConaiStatement(models.Model):
    _name = "italy.conai.statement"
    _description = "CONAI statement"

    name = fields.Char(string="Name", required=True)
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.user.company_id.id,
        required=True,
    )
    conai_line_ids = fields.One2many(
        comodel_name="italy.conai.statement.line",
        inverse_name="statement_id",
        string="Sales",
    )
    conai_category_ids = fields.One2many(
        comodel_name="italy.conai.statement.category",
        inverse_name="statement_id",
        string="Categories",
    )

    @api.multi
    def compute_statement(self):
        def manage_invoice_line(
            statement, invoice, inv_line, conai_category_id, weight, statement_line_ids
        ):
            line_model = self.env["italy.conai.statement.line"]
            conai_amount = conai_category_id.evaluate_conai_amount(weight)
            vals = {
                "statement_id": statement.id,
                "invoice_id": invoice.id,
                "invoice_line_id": inv_line.id,
                "date_invoice": invoice.date_invoice,
                "conai_category_id": conai_category_id.id,
                "conai_exemption_id": invoice.conai_exemption_id
                and invoice.conai_exemption_id.id,
                "conai_amount": conai_amount
                if not inv_line.conai_summary_line
                else 0.0,
                "weight": weight if not inv_line.conai_summary_line else 0.0,
                "conai_amount_due": inv_line.price_subtotal
                if inv_line.conai_summary_line
                else 0.0,
                "weight_due": inv_line.quantity if inv_line.conai_summary_line else 0.0,
                "conai_price_unit": conai_category_id.conai_price_unit,
                "conai_summary_line": inv_line.conai_summary_line,
            }
            if len(statement_line_ids):
                statement_line = line_model.browse(statement_line_ids.pop())
                statement_line.write(vals)
            else:
                line_model.create(vals)
            return statement_line_ids

        line_model = self.env["italy.conai.statement.line"]
        for statement in self:
            statement_line_ids = sorted([x.id for x in statement.conai_line_ids])
            journal_ids = [
                x.id
                for x in self.env["account.journal"].search(
                    [("type", "in", ("sale", "sale_refund"))]
                )
            ]
            domain = [
                ("date_invoice", ">=", statement.date_from),
                ("date_invoice", "<=", statement.date_to),
                ("company_id", "=", statement.company_id.id),
                ("journal_id", "in", journal_ids),
            ]
            for invoice in self.env["account.invoice"].search(domain, order="number"):
                for invLine in invoice.invoice_line_ids:
                    if not invLine.conai_category_id and not invLine.conai_category2_id:
                        continue
                    if invLine.conai_category_id:
                        weight2 = 0.0
                        category2 = False
                        if invLine.product_id:
                            weight2 = (
                                invLine.product_id.weight2
                                or invLine.product_id.product_tmpl_id.weight2
                            ) * invLine.quantity
                            category2 = (
                                invLine.product_id.conai_category2_id
                                or invLine.product_id.product_tmpl_id.conai_category2_id
                            )
                        statement_line_ids = manage_invoice_line(
                            statement,
                            invoice,
                            invLine,
                            invLine.conai_category_id,
                            invLine.weight - weight2,
                            statement_line_ids,
                        )
                        if weight2 and category2:
                            statement_line_ids = manage_invoice_line(
                                statement,
                                invoice,
                                invLine,
                                category2,
                                weight2,
                                statement_line_ids,
                            )
            while statement_line_ids:
                line_model.unlink(statement_line_ids.pop())
        self.compute_category_total()

    @api.multi
    def compute_category_total(self):
        category_model = self.env["italy.conai.statement.category"]
        for statement in self:
            category_total = {}
            category_line_ids = sorted([x for x in statement.conai_category_ids])
            for line in statement.conai_line_ids:
                hash = "%s-%s" % (
                    line.conai_category_id.code,
                    line.invoice_id.conai_exemption_id.code,
                )
                if hash not in category_total:
                    category_total[hash] = {
                        "conai_category_id": line.conai_category_id,
                        "conai_exemption_id": line.invoice_id.conai_exemption_id,
                        "conai_amount": 0.0,
                        "weight": 0.0,
                        "conai_amount_due": 0.0,
                        "weight_due": 0.0,
                        "conai_price_unit": line.conai_category_id.conai_price_unit,
                    }
                if line.conai_summary_line:
                    category_total[hash]["conai_amount_due"] += line.conai_amount_due
                    category_total[hash]["weight_due"] += line.weight_due
                else:
                    category_total[hash]["conai_amount"] += line.conai_amount
                    category_total[hash]["weight"] += line.weight
            for category in category_total.keys():
                vals = {
                    "statement_id": statement.id,
                    "conai_category_id": category_total[category][
                        "conai_category_id"
                    ].id,
                    "conai_exemption_id": category_total[category][
                        "conai_exemption_id"
                    ].id,
                    "conai_amount": category_total[category]["conai_amount"],
                    "weight": category_total[category]["weight"],
                    "conai_amount_due": category_total[category]["conai_amount_due"],
                    "weight_due": category_total[category]["weight_due"],
                    "conai_price_unit": category_total[category]["conai_price_unit"],
                }
                if len(category_line_ids):
                    category_line = category_line_ids.pop()
                    category_line.write(vals)
                else:
                    category_model.create(vals)
            while category_line_ids:
                category_line_ids.pop().unlink()


class ItalyConaiStatementLine(models.Model):
    _name = "italy.conai.statement.line"
    _description = "CONAI statement line"
    _order = "statement_id, date_invoice, id"

    statement_id = fields.Many2one("italy.conai.statement", string="CONAI statement")
    invoice_id = fields.Many2one("account.invoice", string="Invoice")
    invoice_line_id = fields.Many2one("account.invoice.line", string="Invoice Line")
    date_invoice = fields.Date(string="Date")
    conai_category_id = fields.Many2one(
        "italy.conai.product.category", string="CONAI Category"
    )
    conai_exemption_id = fields.Many2one(string="CONAI Exemption")
    conai_amount = fields.Float(
        string="CONAI Amount", digits=dp.get_precision("Product Price")
    )
    weight = fields.Float(
        string="CONAI Weight", digits=dp.get_precision("Stock Weight")
    )
    conai_amount_due = fields.Float(
        string="Due CONAI Amount", digits=dp.get_precision("Product Price")
    )
    weight_due = fields.Float(
        string="Due CONAI Weight", digits=dp.get_precision("Stock Weight")
    )
    conai_price_unit = fields.Float(
        string="Unit Price", digits=dp.get_precision("Product Price")
    )
    conai_summary_line = fields.Boolean("CONAI summary line")
    conai_manual = fields.Boolean("Manual CONAI amount")

    @api.onchange("conai_amount", "weight", "conai_amount_due", "weight_due")
    def _revaluate_totals(self):
        self.statement_id.compute_category_total()


class ItalyConaiStatementCategory(models.Model):
    _name = "italy.conai.statement.category"
    _description = "CONAI statement category"
    _order = "statement_id, conai_category_id, id"

    statement_id = fields.Many2one("italy.conai.statement", string="CONAI statement")
    conai_category_id = fields.Many2one(
        "italy.conai.product.category", string="CONAI Category"
    )
    conai_exemption_id = fields.Many2one(string="CONAI Exemption")
    conai_amount = fields.Float(
        string="CONAI Amount", digits=dp.get_precision("Product Price")
    )
    conai_amount_due = fields.Float(
        string="Due CONAI Amount", digits=dp.get_precision("Product Price")
    )
    weight_due = fields.Float(
        string="Due CONAI Weight", digits=dp.get_precision("Stock Weight")
    )
    conai_price_unit = fields.Float(
        string="Unit Price", digits=dp.get_precision("Product Price")
    )
    weight = fields.Float(
        string="CONAI Weight", digits=dp.get_precision("Stock Weight")
    )
