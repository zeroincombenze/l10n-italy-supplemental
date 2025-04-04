# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import holidays

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def _get_to_send_mail(self):
        if self.type in ("in_invoice", "in_refund"):
            return False
        res = self.env["ir.config_parameter"].get_param("default_to_send_mail")
        modifier = []
        if self.partner_id.to_send_mail:
            modifier.append(self.partner_id.to_send_mail != "disable")
        if self.fiscal_position_id and self.fiscal_position_id.to_send_mail:
            modifier.append(self.fiscal_position_id.to_send_mail != "disable")
        return all(modifier) if res else any(modifier)

    to_send_mail = fields.Boolean(
        string="To send mail",
        default=_get_to_send_mail,
        help="Automatically send invoice mail",
    )

    @api.multi
    def action_auto_send_invoice_mail(self):
        template = self.company_id.invoice_mail_template_id or self.env.ref(
            "account.email_template_edi_invoice"
        )
        mailbox = self.company_id.partner_id.email
        # Post message on chatter
        # self.message_post(body=_("Invoice sent"))
        # Send mail
        template.with_context(
            lang=self.company_id.partner_id.lang).send_mail(
                self.id,
                force_send=True,
                email_values={
                    "email_cc": mailbox, "notification": True, "auto_delete": False})

    @api.multi
    def cron_send_all_invoice_mail(self):
        time_limit = datetime.now() + timedelta(10)
        if (
            datetime.today().date().weekday() < 5
            and datetime.today().date() not in holidays.IT()
        ):
            if any(
                [
                    int(start) <= datetime.now().hour <= int(stop)
                    for start, stop in [
                        interval.split("-")
                        for interval in self.env["ir.config_parameter"]
                        .get_param("default_time_interval")
                        .split(" ")
                    ]
                ]
            ):
                for inv in self.search(
                    [
                        ("to_send_mail", "=", True),
                        ("state", "not in", ["drfat", "cancelled"]),
                        ("type", "in", ["out_invoice", "out_refund"]),
                    ]
                ):
                    inv.action_auto_send_invoice_mail()
                    if datetime.now() > time_limit:
                        break
