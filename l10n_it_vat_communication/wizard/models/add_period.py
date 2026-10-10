# -*- coding: utf-8 -*-
#    Copyright (C) 2011-12 Domsense s.r.l. <http://www.domsense.com>.
#    Copyright (C) 2012-15 Agile Business Group sagl <http://www.agilebg.com>
#    Copyright (C) 2013-15 LinkIt Spa <http://http://www.linkgroup.it>
#    Copyright (C) 2013-17 Associazione Odoo Italia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import _, api, exceptions, fields, models


class AddPeriod(models.TransientModel):

    _name = "add.period.to.vat.commitment"

    period_id = fields.Many2one("date.range", "Period", required=True)

    @api.multi
    def add_period(self):
        if "active_id" not in self.env.context:
            raise exceptions.UserError(_("Current commitment not found"))

        context = self.env.context

        wizard = self.browse(self.id)

        if wizard.period_id.vat_commitment_id:
            raise exceptions.UserError(
                _("Period %s is already associated to commitment")
                % wizard.period_id.name
            )

        for record in self:
            record.period_id.write({"vat_commitment_id": context["active_id"]})

        self.env["account.vat.communication"].compute_amounts([context["active_id"]])

        return {"type": "ir.actions.act_window_close"}
