# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
#                Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MideaPartner(models.Model):
    _name = 'midea.partner'

    name = fields.Char('Title',
                       size=64,
                       required=True,
                       translate=True)
    active = fields.Boolean('Active',
                            default=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed')],
                             'State',
                             required=True,
                             readonly=True,
                             default='draft')
