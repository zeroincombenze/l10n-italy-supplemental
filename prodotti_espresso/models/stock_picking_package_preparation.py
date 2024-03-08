# -*- coding: utf-8 -*-
#
#    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
#
from odoo import api, fields, models
# from odoo.tools.safe_eval import safe_eval


class StockPickingPackagePreparation(models.Model):

    _inherit = "stock.picking.package.preparation"

    to_send_mail = fields.Boolean(
        string="To send mail",
        help="Automatically send mail",
    )

    @api.multi
    def action_auto_send_ddt_mail(self):
        # act_windows = self.action_send_ddt_mail()
        # template_obj = self.env['mail.mail'].browse(
        #     act_windows["context"]['default_template_id'])
        # template_data = {
        #     'email_from': self.company_id.partner_id.email,
        #     'reply_to': self.company_id.partner_id.email,
        #     'subject': 'Test',
        #     'body_html': 'Hello'
        # }
        # template_id = template_obj.create(template_data)
        # template_id.send()
        template = self.env.ref('l10n_it_ddt.email_template_edi_ddt')
        template.send_mail(self.id)
        self.to_send_mail = False

    @api.multi
    def cron_send_all_ddt_mail(self):
        for ddt in self.search([("to_send_mail", "=", True)]):
            ddt.action_auto_send_ddt_mail()
