# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).

from odoo import models, fields


class AccountTaxGroup(models.Model):
    _inherit = 'account.tax.group'

    country_id = fields.Many2one(
        'res.country',
        string='Country',
        default=lambda self: self.env.user.company_id.country_id,
    )

