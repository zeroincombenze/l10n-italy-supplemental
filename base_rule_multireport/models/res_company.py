# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
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
