# -*- coding: utf-8 -*-
#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import api, models


class MultireportMixin(models.AbstractModel):
    _name = "multireport.mixin"
    _description = "Multireport common functions"

    # product_code = fields.Char("Code", compute="_set_code", copy=False)
    # description = fields.Char("Description", compute="_set_description", copy=False)

    @api.model
    def code_2_print(self, style_mode=None):
        if not style_mode:
            style_mode = self.company_id.report_model_style.description_mode
        return (
            self.product_id.default_code
            if self.product_id and style_mode == "print"
            else ""
        )

    # @api.depends("product_id")
    # @api.multi
    # def _set_code(self):
    #     for line in self:
    #         line.product_code = (
    #             line.product_id.default_code if line.product_id else False
    #         )

    @api.model
    def description_2_print(self, style_mode=None):
        if not style_mode:
            style_mode = self.company_id.report_model_style.description_mode
        value = self.name
        if style_mode in ("line1", "nocode1"):
            value = value.split("\n")[0]
        if style_mode in ("nocode", "nocode1"):
            i = value.find("]")
            if value[0] == "[" and i >= 0:
                value = value[i + 1:].lstrip()
        return value
    #
    # @api.depends("product_id", "name")
    # def _set_description(self):
    #     for line in self:
    #         line.description = line.description_2_print()
