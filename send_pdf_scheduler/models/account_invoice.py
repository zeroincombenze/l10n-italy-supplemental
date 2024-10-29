from datetime import datetime
import holidays

from odoo import models, fields, api, _


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
        template = (
            self.company_id.invoice_mail_template_id
            or self.env.ref("account.email_template_edi_invoice")
        )
        self.message_post(body=_("Invoice sent"))
        template.send_mail(self.id, force_send=True)

    @api.multi
    def cron_send_all_invoice_mail(self):
        if (
            datetime.today().date().weekday() < 5
            and datetime.today().date() not in holidays.IT()
        ):
            for inv in self.search([("to_send_mail", "=", True),
                                    ("type", "in", ["out_invoice", "out_refund"])]):
                inv.action_auto_send_invoice_mail()


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.multi
    def send_mail(self, auto_commit=False):
        context = self._context
        if (
                context.get("default_model") == "account.invoice"
                and context.get("default_res_id")
                and context.get("mark_invoice_as_sent")
        ):
            invoice = self.env["account.invoice"].browse(context["default_res_id"])
            invoice.to_send_mail = False
        return super(MailComposeMessage, self).send_mail(auto_commit=auto_commit)

