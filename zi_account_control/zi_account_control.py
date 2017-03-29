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

from openerp.osv import orm
from openerp.tools.translate import _


class account_account(orm.Model):

    _inherit = 'account.account'

    def create(self, cr, uid, vals, context=None):
        if 'code' in vals:
            if vals['code'][-1] == '0' and uid != 1:
                raise orm.except_orm(_('Errore'), _(
                    'Non puoi creare conti che finiscono per zero'))
        return super(account_account, self).create(cr,
                                                   uid,
                                                   vals,
                                                   context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'code' in vals:
            if vals['code'][-1] == '0' and uid != 1:
                raise orm.except_orm(_('Errore'), _(
                    'Non puoi creare conti che finiscono per zero'))
        return super(account_account, self).write(cr,
                                                  uid,
                                                  ids,
                                                  vals,
                                                  context=context)
