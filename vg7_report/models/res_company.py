# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    custom_header = fields.Boolean('Custom Header')
    qweb_header = fields.Text('Header (QWeb)')
    cf_in_header = fields.Boolean('Codice Fiscale in Header')
