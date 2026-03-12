#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def verify_all_notifications(self):
        for company in self.env["res.company"].search([]):
            if (
                company.sdi_channel_id
                and company.sdi_channel_id.channel_type == "evolve"
            ):
                company.sdi_channel_id.verify_all_notifications()

    @api.model
    def acquire_all_einvoices(self):
        for company in self.env["res.company"].search([]):
            if (
                company.sdi_channel_id
                and company.sdi_channel_id.channel_type == "evolve"
            ):
                company.sdi_channel_id.acquire_all_einvoices()
