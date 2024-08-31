from datetime import datetime
import holidays

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def _get_to_send_mail(self):
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
        template = template = (
            self.company_id.invoice_mail_template_id
            or self.env.ref("account.email_template_edi_invoice")
        )
        template.send_mail(self.id)
        self.to_send_mail = False

    @api.multi
    def cron_send_all_invoice_mail(self):
        if (
            datetime.today().date().weekday() < 5
            and datetime.today().date() not in holidays.IT()
        ):
            for inv in self.search([("to_send_mail", "=", True)]):
                inv.action_auto_send_invoice_mail()
