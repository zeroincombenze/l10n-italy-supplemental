# Copyright (c) 2021
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import models, fields
from odoo.addons import decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    cost_delivery_amount = fields.Float(
        string='Costo spedizioni',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    cost_packaging_amount = fields.Float(
        string='Costo imballo',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    cost_payment_amount = fields.Float(
        string='Costo pagamenti',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    cost_other_amount = fields.Float(
        string='Costo diversi',
        digits=dp.get_precision('Product Price'),
        default=0.0)

    cost_discount_amount = fields.Float(
        string='Ripartizione sconto globale',
        digits=dp.get_precision('Product Price'),
        default=0.0)
