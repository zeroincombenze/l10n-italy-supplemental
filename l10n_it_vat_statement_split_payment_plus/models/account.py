# Copyright 2018 Silvio Gregorini <silviogregorini@openforce.it>
# Copyright (c) 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright (c) 2019 Matteo Bilotta
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def group_by_account_and_tax(self):
        grouped_lines = {}

        for line in self:
            group_key = (line.account_id, line.tax_line_id)
            if group_key not in grouped_lines:
                grouped_lines.update({group_key: []})

            grouped_lines[group_key].append(line)

        return grouped_lines
