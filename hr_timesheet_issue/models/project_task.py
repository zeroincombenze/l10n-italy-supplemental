from odoo import api, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.onchange("partner_id")
    def onchange_issue_from_partner(self):
        if self.partner_id:
            for anline in self.timesheet_ids:
                anline.write({"other_partner_id": self.partner_id.id})
