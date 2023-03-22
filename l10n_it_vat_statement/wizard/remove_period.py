# Copyright 2012 Domsense s.r.l. <http://www.domsense.com>.
# Copyright 2012-15 Agile Business Group sagl <http://www.agilebg.com>
# Copyright 2015 Associazione Odoo Italia <http://www.odoo-italia.org>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class RemovePeriod(models.TransientModel):

    def _get_period_ids(self):
        statement_model = self.env['account.vat.period.end.statement']
        res = []
        if 'active_id' in self.env.context:
            statement = statement_model.browse(self.env.context['active_id'])
            for period in statement.date_range_ids:
                res.append((period.id, period.name))
        return res

    _name = 'remove.period.from.vat.statement'
    _description = "Remove period from VAT Statement"

    period_id = fields.Selection(_get_period_ids, 'Period', required=True)

    @api.multi
    def remove_period(self):
        self.ensure_one()
        if 'active_id' not in self.env.context:
            raise UserError(_('Current statement not found'))
        # period = self.env['date.range'].browse(int(self.period_id))
        # period.vat_statement_id = False
        statement = self.env['account.vat.period.end.statement'].browse(
            self.env.context['active_id'])
        statement.write({
            'date_range_ids': [(5, 0)]
        })
        statement.set_fiscal_year()
        statement.compute_amounts()
        return {
            'type': 'ir.actions.act_window_close',
        }
