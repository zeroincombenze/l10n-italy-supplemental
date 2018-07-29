# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
#                Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    preferred_invoice_model_id = fields.Many2one(
        'account.invoice.reportname',
        'Preferred report',
        help="Report model to print this invoice")

    @api.multi
    def invoice_print(self):
        self.ensure_one()
        reportname, invoice_reportname_id = self.env[
            'account.invoice.reportname'].get_reportname(self[0])
        if not self[0].invoice_reportname_id and invoice_reportname_id:
            self.write({'invoice_reportname_id': invoice_reportname_id})
        if reportname:
            return self.env['report'].get_action(self, reportname)
        else:
            return super(AccountInvoice, self).invoice_print()
