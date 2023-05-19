# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    calendar_ids = fields.One2many(
        "calendar.event",
        inverse_name="task_id",
        string="Meetings",
        help="Reference to Calendar Events",
    )
    meeting_count = fields.Integer('# Meetings', compute='_compute_meeting_count')

    @api.multi
    def _compute_meeting_count(self):
        meeting_data = self.env["calendar.event"].read_group(
            [("task_id", "in", self.ids)],
            ["task_id"],
            ["task_id"])
        mapped_data = {m["task_id"][0]: m["task_id_count"] for m in meeting_data}
        for task in self:
            task.meeting_count = mapped_data.get(task.id, 0)

    @api.multi
    def action_schedule_meeting(self):
        self.ensure_one()
        action = self.env.ref("calendar.action_calendar_event").read()[0]
        partner_ids = self.env.user.partner_id.ids
        if self.partner_id:
            partner_ids.append(self.partner_id.id)
        action['context'] = {
            'default_partner_id': self.partner_id.id,
            'default_partner_ids': partner_ids,
            # 'default_team_id': self.team_id.id,
            'default_name': self.name,
        }
        return action
