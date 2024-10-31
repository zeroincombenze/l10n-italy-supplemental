# -*- coding: utf-8 -*-
from odoo import models


class MailMail(models.Model):
    _inherit = "mail.mail"

    def _postprocess_sent_message(self, mail_sent=True):
        if mail_sent:
            self.filtered(
                lambda item: item.mail_message_id.model == "account.invoice").write(
                    {"to_send_mail": False}
            )
        return super(MailMail, self)._postprocess_sent_message(mail_sent)
