# -*- coding: utf-8 -*-

from odoo import models, fields


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    task_id = fields.Many2one(
        'project.task',
        string="Task",
        help="Reference to Project Task",
    )