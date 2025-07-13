# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def do_print_picking(self):
        action = super(Picking, self).do_print_picking()
        reportname = self.env["report"].select_reportname(self)
        if reportname:
            action["reportname"] = reportname
        return action
