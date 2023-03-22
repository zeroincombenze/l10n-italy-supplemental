# Copyright 2018 Silvio Gregorini <silviogregorini@openforce.it>
# Copyright (c) 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright (c) 2019 Matteo Bilotta
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sp_description = fields.Char(
        related='company_id.sp_description',
        string="Description for period end statements",
        readonly=False
    )
