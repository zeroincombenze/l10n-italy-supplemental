# -*- coding: utf-8 -*-
#    Copyright 2017-18 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    copy_sale_price = fields.Boolean(
        "Copy Price from Sale",
        default=False,
        help="Copy Sale Price when create Purchase Order Line",
    )
