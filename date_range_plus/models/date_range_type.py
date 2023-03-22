# Copyright 2016 ACSONE SA/NV <http://acsone.eu>
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import fields, models


class DateRangeType(models.Model):
    _inherit = "date.range.type"
    _name = "date.range.type"
    _description = "Date Range Type"

    parent_type_id = fields.Many2one(
        comodel_name='date.range.type',
        select=-31
    )
