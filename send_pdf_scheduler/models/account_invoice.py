from datetime import datetime
import logging
import holidays

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


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
        _logger.info("action_auto_send_invoice_mail(%s)" % self.id)
        template = (
            self.company_id.invoice_mail_template_id
            or self.env.ref("account.email_template_edi_invoice")
        )
        _logger.info("template = %s (%s)" % (template.id, template.name))
        mailbox = self.company_id.partner_id.email
        _logger.info("mailbox = %s " % mailbox)
        # Post message on chatter
        # self.message_post(body=_("Invoice sent"))
        # Send mail
        _logger.info(
            "sending template.with_context(lang='%s').send_mail("
            "self.id, force_send=True, email_values={'email_cc': mailbox})"
            % self.company_id.partner_id.lang)
        template.with_context(lang=self.company_id.partner_id.lang).send_mail(
            self.id, force_send=True, email_values={"email_cc": mailbox})
        _logger.info("SENT")

    @api.multi
    def cron_send_all_invoice_mail(self):
        if (
            datetime.today().date().weekday() < 5
            and datetime.today().date() not in holidays.IT()
        ):
            _logger.info("cron_send_all_invoice_mail()")
            for inv in self.search([("to_send_mail", "=", True),
                                    ("state", "not in", ["draft", "cancelled"]),
                                    ("type", "in", ["out_invoice", "out_refund"])]):
                _logger.info("Sending invoice %s" % inv.number)
                inv.action_auto_send_invoice_mail()
        else:
            _logger.info("Cannnot send pdf invocie because holiday")
