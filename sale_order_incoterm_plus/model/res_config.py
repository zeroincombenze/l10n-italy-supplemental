# Copyright 2020-16 Powerp Enterprise Network
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_incoterm_default = fields.Many2one(
        related='company_id.sale_incoterm_default',
        readonly=False,
    )
# end ResConfigSettings
