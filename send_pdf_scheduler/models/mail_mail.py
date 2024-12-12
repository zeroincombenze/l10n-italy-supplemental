# -*- coding: utf-8 -*-
from odoo import models


class MailMail(models.Model):
    _inherit = "mail.mail"

    def _postprocess_sent_message(self, mail_sent=True):
        mails = self.filtered(
            lambda item: item.mail_message_id.model == "account.invoice")
        for mail in mails:
            self.env[mail.model].browse(mail.res_id).write({"to_send_mail": False})
        return super(MailMail, self)._postprocess_sent_message(mail_sent)
