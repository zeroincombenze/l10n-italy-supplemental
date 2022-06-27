# -*- coding: utf-8 -*-
#
# Copyright 2018-21 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    assosoftware_id = fields.Many2one(
        'italy.ade.tax.assosoftware',
        string='Assosoftware Code',
        help='Tax Assosoftware classification')
