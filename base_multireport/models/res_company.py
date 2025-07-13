# -*- coding: utf-8 -*-
#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    report_model_style = fields.Many2one(
        "multireport.style",
        "Multi-report style",
        help="Select multi-report style",
    )


class ReportConfigSettings(models.TransientModel):
    _inherit = ["base.config.settings"]

    report_model_style = fields.Many2one(
        related="company_id.report_model_style",
        string="Multi-report style",
        help="Select multi-report style",
    )
