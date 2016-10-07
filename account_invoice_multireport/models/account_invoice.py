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

from openerp.osv import orm, fields
from openerp import api


# class account_invoice(models.Model):
class account_invoice(orm.Model):
    _inherit = "account.invoice"

    _columns = {
        'invoice_reportname_id': fields.many2one(
            'account.invoice.reportname',
            'Report model',
            help="Report model to print this invoice"),
    }

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
            return super(account_invoice, self).invoice_print()
