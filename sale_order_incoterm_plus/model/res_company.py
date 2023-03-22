# Copyright 2020-16 Powerp Enterprise Network
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_incoterm_default = fields.Many2one(
        string='Default Incoterm per le vendite',
        comodel_name='account.incoterms'
    )
# end ResCompany
