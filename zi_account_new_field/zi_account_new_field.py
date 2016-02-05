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

class account_account_zi(orm.Model):
    _inherit = "account.account"

    _columns = {
        'zi_iv_dir': fields.char('IV dir.', size=8),
        'zi_remark': fields.char('Istruzioni per l\'uso', size=1024),
    }

class account_account_template_zi(orm.Model):
    _inherit = "account.account.template"

    _columns = {
        'zi_iv_dir': fields.char('IV dir.', size=8),
        'zi_remark': fields.char('Istruzioni per l\'uso', size=1024),
    }


class account_tax_zi(orm.Model):
    _inherit = "account.tax"

    _columns = {
        'zi_remark': fields.char('Istruzioni per l\'uso', size=1024),
    }

class account_tax_template_zi(orm.Model):
    _inherit = "account.tax.template"

    _columns = {
        'zi_remark': fields.char('Istruzioni per l\'uso', size=1024),
    }