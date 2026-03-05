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


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    conai_exemption_id = fields.Many2one(
        "italy.conai.partner.category", string="CONAI Exemption"
    )
    amount_goods_service = fields.Monetary(
        string="Goods & Service Amount",
        currency_field="company_currency_id",
        store=True,
        readonly=True,
    )
    amount_conai = fields.Monetary(
        string="CONAI Amount",
        currency_field="company_currency_id",
        store=True,
        readonly=True,
    )

    @api.multi
    def action_move_create(self):
        def _calc_conai_value(conai_category, weight):
            conai_amount = conai_category.evaluate_conai_amount(weight)
            conai_summary[conai_category]["amount"] = conai_amount
            conai_summary[conai_category]["weight"] += weight
            return conai_amount

        def _process_category(conai_category, line):
            if not conai_category:
                return
            weight_conv, uom = conai_category.evaluate_weight_conv()
            category2 = weight2 = False
            if conai_category not in conai_summary:
                conai = {
                    "name": conai_category.name,
                    "weight": 0.0,
                    "um": uom,
                    "price_unit": conai_category.get_price(),
                    "amount": 0.0,
                    "account_id": conai_category.account_id.id,
                    "tax": line.invoice_line_tax_ids,
                }
                if not conai["account_id"]:
                    conai["account_id"] = line.account_id.id
                conai_summary[conai_category] = conai
            if line.product_id:
                weight2 = (
                    line.product_id.weight2 or line.product_id.product_tmpl_id.weight2
                ) * line.quantity
                category2 = (
                    line.product_id.conai_category2_id
                    or line.product_id.product_tmpl_id.conai_category2_id
                )
            if weight2 and category2:
                if conai_category == category2:
                    _calc_conai_value(conai_category, weight2)
                else:
                    _calc_conai_value(conai_category, line.weight - weight2)
            else:
                conai_amount = _calc_conai_value(conai_category, line.weight)
                line.write({"conai_amount": conai_amount, "weight": line.weight})

        inv_line_model = self.env["account.invoice.line"]
        for invoice in self:
            if invoice.type not in ("out_invoice", "out_refund"):
                continue
            conai_product = invoice.company_id.conai_product_id
            conai_summary = {}
            if invoice.conai_exemption_id and invoice.conai_exemption_id.conai_percent:
                percent = invoice.conai_exemption_id.conai_percent
                partner_expt_name = invoice.conai_exemption_id.name
                ii = partner_expt_name.lower().find("vs")
                if ii >= 0:
                    partner_expt_name = partner_expt_name[ii:]
                partner_expt_name = "Esenzione %s%% %s" % (percent, partner_expt_name)
            else:
                percent = 0.0
                partner_expt_name = ""
            conai_invoice_lines = {}
            lines_to_delete = []
            for line in invoice.invoice_line_ids:
                if line.conai_summary_line or (
                    line.product_id and line.product_id == conai_product
                ):
                    if line.conai_category_id:
                        conai_invoice_lines[line.conai_category_id] = {
                            "line": line,
                            "remove": True,
                            "conai_manual": line.conai_manual,
                            "manual_price_unit": line.price_unit,
                            "manual_weight": line.weight,
                        }
                    else:
                        lines_to_delete.append(line)
                    continue
                if not line.conai_category_id:
                    continue
                line._compute_weight()
                _process_category(line.conai_category_id, line)
                if line.product_id:
                    _process_category(
                        line.product_id.conai_category2_id
                        or line.product_id.product_tmpl_id.conai_category2_id,
                        line,
                    )

            invoice.amount_conai = 0.0
            for conai_category, conai_item in conai_summary.items():
                if partner_expt_name:
                    conai_name = "Contributo ambientale %s (%s %s)\n%s" % (
                        conai_item["name"],
                        conai_item["weight"],
                        conai_item["um"].name,
                        partner_expt_name,
                    )
                else:
                    conai_name = "Contributo ambientale %s (%s %s)" % (
                        conai_item["name"],
                        conai_item["weight"],
                        conai_item["um"].name,
                    )
                line_vals = {
                    "product_id": conai_product.id,
                    "name": conai_name,
                    "invoice_id": invoice.id,
                    "uom_id": conai_item["um"].id,
                    "quantity": conai_category.get_qty(
                        conai_item["weight"], percent=percent
                    ),
                    "price_unit": conai_item["price_unit"],
                    "account_id": conai_item["account_id"],
                    "invoice_line_tax_ids": [(6, 0, [x.id for x in conai_item["tax"]])],
                    "conai_category_id": conai_category.id,
                    "conai_summary_line": True,
                    "conai_manual": False,
                    "sequence": 99999,
                }
                if conai_category in conai_invoice_lines:
                    inv_line = conai_invoice_lines[conai_category]["line"]
                    if conai_invoice_lines[conai_category]["conai_manual"]:
                        line_vals["conai_manual"] = True
                        for field in ("price_unit", "quantity"):
                            del line_vals[field]
                        line_vals["name"] += " *"
                    inv_line.write(line_vals)
                    inv_line = inv_line_model.browse(inv_line.id)
                    conai_invoice_lines[conai_category]["remove"] = False
                else:
                    inv_line = inv_line_model.create(line_vals)
                invoice.amount_conai += inv_line.price_subtotal
            for conai_category in conai_invoice_lines.keys():
                if conai_invoice_lines[conai_category]["remove"]:
                    conai_invoice_lines[conai_category]["line"].unlink()
            for line in lines_to_delete:
                line.unlink()
            invoice.amount_goods_service = invoice.amount_untaxed - invoice.amount_conai
            if len(conai_summary):
                invoice.compute_taxes()
        return super(AccountInvoice, self).action_move_create()


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    date_invoice = fields.Date(
        string="Date", related="invoice_id.date_invoice", store=True, readonly=True
    )
    conai_category_id = fields.Many2one(
        "italy.conai.product.category", string="CONAI Category"
    )
    conai_amount = fields.Float(
        string="CONAI Amount", digits=dp.get_precision("Product Price")
    )
    conai_exemption_id = fields.Many2one(
        string="CONAI Exemption",
        related="invoice_id.conai_exemption_id",
        store=True,
        readonly=True,
    )
    conai_category2_id = fields.Many2one(
        "italy.conai.product.category", string="CONAI 2nd Category"
    )
    weight2 = fields.Float(
        string="CONAI 2nd Category Weight", digits=dp.get_precision("Stock Weight")
    )
    conai_summary_line = fields.Boolean("CONAI summary line")
    conai_manual = fields.Boolean("Manual CONAI amount")

    @api.depends("product_id", "quantity")
    def _compute_weight(self):
        if self.product_id:
            prod_weight = (
                self.product_id.weight or self.product_id.product_tmpl_id.weight
            )
            line_weight = self.weight = prod_weight * self.quantity
            if (line_weight * 1.5) >= self.weight <= (line_weight * 0.7):
                self.weight = line_weight

    @api.multi
    @api.onchange("product_id")
    def _set_conai_category(self):
        if self.product_id:
            if self.product_id.conai_category_id:
                self.conai_category_id = self.product_id.conai_category_id.id
            elif self.product_id.product_tmpl_id.conai_category_id:
                self.conai_category_id = (
                    self.product_id.product_tmpl_id.conai_category_id.id
                )
            self.evaluate_conai_amount()

    @api.onchange("price_unit", "quantity", "discount", "conai_category_id")
    def evaluate_conai_amount(self):
        self._compute_weight()
        if self.conai_summary_line:
            self.conai_manual = True
        elif self.weight and self.conai_category_id:
            self.conai_amount = self.conai_category_id.evaluate_conai_amount(
                self.weight
            )

    @api.model
    def create(self, vals):
        if "conai_category_id" not in vals and "product_id" in vals:
            weight = vals.get("weight", 0.0)
            conai_category_id = False
            product = self.env["product.product"].browse(vals["product_id"])
            if product.conai_category_id:
                conai_category_id = product.conai_category_id.id
                if not weight:
                    weight = product.weight
            else:
                if (
                    product.product_tmpl_id
                    and product.product_tmpl_id.conai_category_id
                ):
                    conai_category_id = product.product_tmpl_id.conai_category_id.id
                    if not weight:
                        weight = product.weight
            if conai_category_id:
                vals["conai_category_id"] = conai_category_id
            if weight:
                vals["weight"] = weight * vals.get("quantity", 1.0)
        return super(AccountInvoiceLine, self).create(vals)
