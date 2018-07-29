# -*- coding: utf-8 -*-
#
# Copyright 2017-2018, Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
import time

from openerp.report import report_sxw


class AccountInvoice(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(AccountInvoice, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })


report_sxw.report_sxw(
    'report.account_invoice',
    'account.invoice',
    'z0_invoice_report/report/account_invoice.rml',
    parser=AccountInvoice
)
