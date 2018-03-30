# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
#                Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.osv import osv, fields


class midea_partner(osv.Model):
    _name = 'midea.partner'

    _columns = {
        'name': fields.char('Title',
                            size=64,
                            required=True,
                            translate=True),
        'active': fields.boolean('Active'),
        'state': fields.selection([('draft', 'Draft'),
                                   ('confirmed', 'Confirmed')],
                                  'State',
                                  required=True,
                                  readonly=True),
    }

    _defaults = {
        'active': True,
        'state': 'draft',
    }
