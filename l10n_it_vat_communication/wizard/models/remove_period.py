# -*- coding: utf-8 -*-
#    Copyright (C) 2017    SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# [2017: SHS-AV s.r.l.] First version
#

from odoo import _, api, exceptions, fields, models


class RemovePeriod(models.TransientModel):

    _name = "remove.period.from.vat.commitment"

    @api.model
    def _get_period_ids(self):
        res = []
        context = self.env.context
        if "active_id" in context:
            commitment_obj = self.env["account.vat.communication"].search(
                [("id", "=", context["active_id"])]
            )
            for period in commitment_obj.period_ids:
                res.append((period.id, period.name))

        return res

    period_id = fields.Selection(_get_period_ids, "Period", required=True)

    @api.multi
    def remove_period(self):
        context = self.env.context

        if "active_id" not in context:
            raise exceptions.UserError(_("Current commitment not found"))

        for record in self:
            rec = self.env["date.range"].search([("id", "=", int(record.period_id))])
            rec.write({"vat_commitment_id": None})
        self.env["account.vat.communication"].compute_amounts(context["active_id"])

        return {
            "type": "ir.actions.act_window_close"
            # 'type': 'ir.actions.client',
            # 'tag': 'reload',
        }
