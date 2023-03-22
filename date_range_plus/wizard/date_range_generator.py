# Copyright 2016 ACSONE SA/NV <http://acsone.eu>
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import fields, models


class DateRangeGenerator(models.TransientModel):
    _name = 'date.range.generator'
    _inherit = 'date.range.generator'
    _description = 'Date Range Generator'

    date_start = fields.Date(strint='Start date', required=True)
