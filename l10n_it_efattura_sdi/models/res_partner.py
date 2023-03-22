# -*- coding: utf-8 -*-
# © 2020 Andrei Levin - Didotech srl (www.didotech.com)

from odoo import models, fields
# from odoo.tools.translate import _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_email = fields.Char(
        string="Invoice Email",
        help='If set a copy of Invoice will be sent to this address '
             'after sending to SDI'
    )
