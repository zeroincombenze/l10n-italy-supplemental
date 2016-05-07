# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time

from openerp.report import report_sxw
from openerp import pooler


class AccountInvoice_Report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(AccountInvoice_Report, self).__init__(cr,
                                                    uid,
                                                    name,
                                                    context=context)
        self.localcontext.update({
            'time': time,
            'cr': cr,
            'uid': uid,
            'company_vat': self._get_company_vat,
        })

    def _get_company_vat(self):
        res_users_obj = pooler.get_pool(self.cr.dbname).get('res.users')
        company_vat = res_users_obj.browse(self.cr,
                                           self.uid,
                                           self.uid).company_id.partner_id.vat
        if company_vat:
            return company_vat
        else:
            return False

report_sxw.report_sxw('report.invoice_wht',
                      'account.invoice',
                      'zi_invoice_wht/report/account.report_invoice_wht.mako',
                      parser=AccountInvoice_Report)
