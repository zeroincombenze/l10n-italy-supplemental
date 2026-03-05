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


class SaleOrder(models.Model):
    _inherit = "sale.order"

    conai_exemption_id = fields.Many2one(
        "italy.conai.partner.category", string="CONAI Exemption"
    )
    amount_goods_service = fields.Monetary(
        string="Goods & Service Amount",
        currency_field="company_id",
        store=True,
        readonly=True,
    )
    amount_conai = fields.Monetary(
        string="CONAI Amount", currency_field="company_id", store=True, readonly=True
    )

    @api.multi
    def action_confirm(self):
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
                    "tax": line.tax_id,
                }
                conai_summary[conai_category] = conai
            if line.product_id:
                weight2 = (
                    line.product_id.weight2 or line.product_id.product_tmpl_id.weight2
                ) * line.product_uom_qty
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

        order_line_model = self.env["sale.order.line"]
        for order in self:
            conai_product = order.company_id.conai_product_id
            conai_summary = {}
            if order.conai_exemption_id and order.conai_exemption_id.conai_percent:
                percent = order.conai_exemption_id.conai_percent
                partner_expt_name = order.conai_exemption_id.name
                ii = partner_expt_name.lower().find("vs")
                if ii >= 0:
                    partner_expt_name = partner_expt_name[ii:]
                partner_expt_name = "Esenzione %s%% %s" % (percent, partner_expt_name)
            else:
                percent = 0.0
                partner_expt_name = ""
            conai_order_lines = {}
            lines_to_delete = []
            for line in order.order_line:
                if line.conai_summary_line or (
                    line.product_id and line.product_id == conai_product
                ):
                    if line.conai_category_id:
                        conai_order_lines[line.conai_category_id] = {
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

            # order.amount_conai = 0.0
            if conai_product:
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
                        "order_id": order.id,
                        "product_uom": conai_item["um"].id,
                        "product_uom_qty": conai_category.get_qty(
                            conai_item["weight"], percent=percent
                        ),
                        "price_unit": conai_item["price_unit"],
                        "tax_id": [(6, 0, [x.id for x in conai_item["tax"]])],
                        "conai_category_id": conai_category.id,
                        "conai_summary_line": True,
                        "conai_manual": False,
                        "sequence": 99999,
                    }
                    if conai_category in conai_order_lines:
                        order_line = conai_order_lines[conai_category]["line"]
                        if conai_order_lines[conai_category]["conai_manual"]:
                            line_vals["conai_manual"] = True
                            for field in ("price_unit", "quantity"):
                                del line_vals[field]
                            line_vals["name"] += " *"
                        order_line.write(line_vals)
                        # order_line = order_line_model.browse(order_line.id)
                        conai_order_lines[conai_category]["remove"] = False
                    else:
                        order_line_model.create(line_vals)
                    # order.amount_conai += order_line.price_subtotal
                for conai_category in conai_order_lines.keys():
                    if conai_order_lines[conai_category]["remove"]:
                        conai_order_lines[conai_category]["line"].unlink()
                for line in lines_to_delete:
                    line.unlink()
                if len(conai_summary):
                    order._amount_all()
        return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_order = fields.Datetime(
        string="Date", related="order_id.date_order", store=True, readonly=True
    )
    conai_category_id = fields.Many2one(
        "italy.conai.product.category", string="CONAI Category"
    )
    conai_amount = fields.Float(
        string="CONAI Amount", digits=dp.get_precision("Product Price")
    )
    conai_exemption_id = fields.Many2one(
        string="CONAI Exemption",
        related="order_id.conai_exemption_id",
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

    @api.depends("product_id", "product_uom_qty")
    def _compute_weight(self):
        if self.product_id:
            prod_weight = (
                self.product_id.weight or self.product_id.product_tmpl_id.weight
            )
            line_weight = self.weight = prod_weight * self.product_uom_qty
            if (line_weight * 1.5) >= self.weight <= (line_weight * 0.7):
                self.weight = line_weight

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

    # @api.multi
    @api.onchange("price_unit", "product_uom_qty", "discount", "conai_category_id")
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
                vals["weight"] = weight * vals.get("product_uom_qty", 1.0)
        return super(SaleOrderLine, self).create(vals)
