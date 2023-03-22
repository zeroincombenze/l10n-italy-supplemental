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


class AddPeriod(models.TransientModel):

    _name = 'add.period.to.vat.statement'
    _description = "Add period to VAT Statement"

    def _set_statement_type(self):
        if 'active_id' not in self.env.context:
            return False

        active_id = self.env.context.get('active_id')
        statement = self.env['account.vat.period.end.statement'].browse(
            active_id)
        return statement.statement_type

    period_id = fields.Many2one(
        'date.range', 'Period', required=True)
    statement_type = fields.Selection(
        [('recur', 'Liquidazione periodica'),
         ('year', 'Liquidazione annuale'),
         ('eu', 'Liquidazione EU-OSS')],
        string='Tipo liquidazione',
        default=_set_statement_type
    )

    @api.multi
    def add_period(self):
        self.ensure_one()
        if 'active_id' not in self.env.context:
            raise UserError(_('Current statement not found'))
        statement_env = self.env['account.vat.period.end.statement']
        wizard = self
        # if wizard.period_id.vat_statement_id and wizard.period_id.vat_statement_id.statement_type == wizard.statement_type:
        #     raise UserError(
        #         _('Period %s is associated to statement %s yet') %
        #         (
        #             wizard.period_id.name,
        #             wizard.period_id.vat_statement_id.date)
        #     )
        statement_id = self.env.context['active_id']
        # wizard.period_id.vat_statement_id = statement_id
        statement = statement_env.browse(statement_id)
        if statement.date_range_ids:
            period_id = statement.date_range_ids[0]
            raise UserError(
                    _('Period %s is associated to statement %s yet') %
                    (
                        period_id.name,
                        statement.date)
                )
        if wizard.period_id:
            statement.write({
                'date_range_ids': [(6, 0, [wizard.period_id.id])]
            })
        statement.set_fiscal_year()
        statement.compute_amounts()
        return {
            'type': 'ir.actions.act_window_close',
        }
