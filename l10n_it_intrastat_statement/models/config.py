# Copyright 2019 Simone Rubino - Agile Business Group
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License AGPL-3 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    intrastat_custom_id = fields.Many2one(
        comodel_name='account.intrastat.custom',
        string="Customs Section")
