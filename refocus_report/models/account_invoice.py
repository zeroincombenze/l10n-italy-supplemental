# -*- coding: utf-8 -*-

from odoo import api, models, fields


class AccountInvoiceModel(models.AbstractModel):
    name = 'report.account.report_invoice_document'
    # _inherit = 'account.invoice'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'refocus_report.report_invoice_document')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('refocus_report.report_invoice_document',
                                 docargs)