#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.org>)
#    All Rights Reserved
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

from osv import osv, fields
from tndb.tndb import tndb


class account_check_wizard(osv.TransientModel):

    _name = "wizard.account.check"

    _columns = {
        'state': fields.selection([('step1', 'step1'), ('step2', 'step2')]),
        'log1': fields.text('Log1'),
    }
    _defaults = {
        'state': 'step1'
    }

    def account_check(self, cr, uid, ids, context=None):

        tndb.wlog('account_check_wizard.account_check')
        check_obj = self.pool.get('z0_account_check.Check4Account')

        log1 = u"Passed"
        if context.get('company_id', False):
            company_id = context['company_id']
        else:
            company_id = self.pool.get('res.users').browse(
                cr, uid, uid, context=context).company_id.id

        params = {'company_id': company_id,
                  'periodo': 'anno',
                  'anno': 2013}
        check_obj.account_check(cr, uid, params, context=None)

        self.write(cr, uid, ids, {'state': 'step2',
                                  'log1': log1})
        wiz = self.browse(cr, uid, ids, context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.account.check',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz[0].id,
            'views': [(False, 'form')],
            'target': 'new',
            'context': context}
