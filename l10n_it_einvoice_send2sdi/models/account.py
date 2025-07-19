# -*- coding: utf-8 -*-
#
# Copyright 2018-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import api, fields, models

fatturapa_attachment_state_mapping = {
    # "ready": "ready",
    # "sent": "sent",
    "validated": "delivered",
    "sender_error": "error",
    "recipient_error": "error",
    "rejected": "error",
    "discarted": "error",
}


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_state = fields.Selection(
        [
            ("ready", "Ready to Send"),
            ("sent", "Sent"),
            ("delivered", "Delivered"),
            ("accepted", "Accepted"),
            ("error", "Error"),
        ],
        string="E-invoice State",
        translate=True,
        compute="_compute_fatturapa_state",
        store="true",
    )

    @api.multi
    @api.depends("fatturapa_attachment_out_id.state")
    def _compute_fatturapa_state(self):
        for record in self:
            fatturapa_state = fatturapa_attachment_state_mapping.get(
                record.fatturapa_attachment_out_id.state,
                record.fatturapa_attachment_out_id.state
            )
            if fatturapa_state == "delivered" and record.state == "paid":
                fatturapa_state = "accepted"
            record.fatturapa_state = fatturapa_state

    @api.multi
    def send_einvoice(self):
        for record in self:
            record.fatturapa_attachment_out_id.send_einvoice()
