# -*- coding: utf-8 -*-

from odoo import models, api


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.onchange("name", "date")
    def onchange_name_date(self):
        if not self.other_partner_id:
            if self.issue_id.partner_id:
                self.other_partner_id = self.issue_id.partner_id
            elif self.task_id.partner_id:
                self.other_partner_id = self.task_id.partner_id
            elif self.partner_id:
                self.other_partner_id = self.partner_id

    @api.onchange("task_id")
    def onchange_task(self):
        if self.task_id.partner_id:
            self.other_partner_id = self.task_id.partner_id

    @api.onchange("issue_id")
    def onchange_issue(self):
        if self.issue_id.partner_id:
            self.other_partner_id = self.issue_id.partner_id

    @api.model
    def create(self, vals):
        if not vals.get("other_partner_id"):
            if vals.get("issue_id"):
                vals["other_partner_id"] = self.env["project.issue"].browse(
                    vals["issue_id"]).partner_id.id
            elif vals.get("task_id"):
                vals["other_partner_id"] = self.env["project.task"].browse(
                    vals["task_id"]).partner_id.id
            elif vals.get("partner_id"):
                vals["other_partner_id"] = vals["partner_id"]
        res = super(AccountAnalyticLine, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        if not vals.get("other_partner_id") and not self.other_partner_id:
            if vals.get("issue_id"):
                vals["other_partner_id"] = self.env["project.issue"].browse(
                    vals["issue_id"]).partner_id.id
            elif self.issue_id:
                vals["other_partner_id"] = self.issue_id.partner_id.id
            elif vals.get("task_id"):
                vals["other_partner_id"] = self.env["project.task"].browse(
                    vals["task_id"]).partner_id.id
            elif self.task_id.partner_id:
                vals["other_partner_id"] = self.task_id.partner_id.id
            elif vals.get("partner_id"):
                vals["other_partner_id"] = vals["partner_id"]
            elif self.partner_id:
                vals["other_partner_id"] = self.partner_id.id
        res = super(AccountAnalyticLine, self).write(vals)
        return res
