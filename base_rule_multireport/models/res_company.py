# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
#                Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    preferred_invoice_model_id = fields.Many2one(
        'account.invoice.reportname',
        'Preferred report',
        help="Default customer-invoice model")
    custom_header = fields.Boolean('Custom Header')
    cf_in_header = fields.Boolean(
        'Fiscalcode in Header',
        help='Print customer fiscalcode in Header, if set, after vatnumber')
