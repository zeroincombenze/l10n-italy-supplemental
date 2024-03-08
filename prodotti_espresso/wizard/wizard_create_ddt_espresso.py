# -*- coding: utf-8 -*-
#
#    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#

from odoo import models, _, fields


class WizardCreateDdtEspresso(models.TransientModel):
    _name = "wizard.create.ddt.espresso"

    validate_ddt = fields.Boolean(
        string="Validate DdT",
        default=True)

    to_send_mail = fields.Boolean(
        string="To send mail",
        help="Automatically send mail",
        default=True)

    def create_ddt_espresso(self):
        orders = self.env["sale.order"]
        for sale_id in self.env.context['active_ids']:
            orders += self.env["sale.order"].browse(sale_id)
        ddt_ids = orders.generate_ddt_espresso(
            validate=self.validate_ddt, to_send_mail=self.to_send_mail)
        # ----- Show new DdTs
        if ddt_ids:
            ir_model_data = self.env["ir.model.data"]
            form_res = ir_model_data.get_object_reference(
                "l10n_it_ddt", "sppp_line_stock_picking_package_preparation_form_ddt")
            form_id = form_res and form_res[1] or False
            tree_res = ir_model_data.get_object_reference(
                "l10n_it_ddt", "ddt_stock_picking_package_preparation_tree")
            tree_id = tree_res and tree_res[1] or False
            return {
                "name": _("DdT espresso"),
                "view_type": "form",
                "view_mode": "form,tree",
                "res_model": "stock.picking.package.preparation",
                "domain": [("id", "in", ddt_ids)],
                "view_id": False,
                "views": [(tree_id, "tree"), (form_id, "form")],
                "type": "ir.actions.act_window",
            }
