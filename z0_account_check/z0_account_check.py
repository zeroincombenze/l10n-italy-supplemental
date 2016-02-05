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

from osv import orm
from openerp.tools.translate import _
import datetime
import calendar
# import time
from tndb.tndb import tndb


class Check4Account(orm.Model):

    _name = "z0.account.check"
    _description = "Check for accounting data"

    def _get_date_start_stop(self, cr, uid, ids, context=None):
        tndb.wlog('Check4Account._get_date')
        y = int(ids.get('anno'))
        if ids.get('periodo') == 'anno':
            period_date_start = datetime.date(y, 1, 1)
            period_date_stop = datetime.date(y, 12, 31)
        elif ids.get('periodo') == 'mese':
            m = int(ids.get('mese'))
            l = calendar.monthrange(y, m)[1]
            period_date_start = datetime.date(y, m, 1)
            period_date_stop = datetime.date(y, m, l)
        elif ids.get('periodo') == 'trimestre':
            t = int(ids.get('trimestre'))
            l = calendar.monthrange(y, t * 3)[1]
            m = (t - 1) * 3 + 1
            period_date_start = datetime.date(y, m, 1)
            period_date_stop = datetime.date(y, t * 3, l)
        else:
            raise orm.except_orm(_('Param error!'),
                                 _("Invalid period"))
        return period_date_start, period_date_stop

    def account_check(self, cr, uid, ids, context=None):
        # Get account periods
        # @periodo: selection period, may be 'anno', 'mese', 'trimestre'
        # @anno: year of selection period
        # @mese: if 'periodo'=='mese' is month of selection period
        # @trimestre: if 'periodo'=='trimestre' is quarter of selection period
        # @return: account periods in selecion
        def _get_periods(cr, uid, ids, context=None):
            # sql_select = "SELECT p.id FROM account_period p"
            # sql_where = " WHERE p.special = False"
            # sql_where += " AND p.company_id = %(company_id)s"
            # sql_where += " AND p.date_start >= date(%(period_date_start)s)"
            # sql_where += " AND p.date_stop <=date(%(period_date_stop)s) "
            # search_params = {'period_date_start': period_date_start,
            #                  'period_date_stop': period_date_stop,
            #                  'company_id': ids.get('company_id')}
            # sql = sql_select + sql_where
            # cr.execute(sql, search_params)

            tndb.wlog('Check4Account._get_periods')
            period_date_start, period_date_stop = self._get_date_start_stop(
                cr,
                uid,
                ids,
                context=None)
            company_id = ids['company_id']
            period_obj = self.pool.get('account.period')
            period_search = [('company_id', '=', company_id),
                             ('date_start', '>=', period_date_start),
                             ('date_stop', '<=', period_date_stop)]
            period_ids = period_obj.search(cr,
                                           uid,
                                           period_search,
                                           context=context)
            return period_ids

        tndb.wlog('Check4Account.account_check')
        period_ids = _get_periods(cr, uid, ids, context=None)
        company_id = ids['company_id']
        date_start, date_stop = self._get_date_start_stop(
            cr,
            uid,
            ids,
            context=None)
        tndb.wlog('params', company_id, date_start, date_stop)

        # journal (sezionali)
        journal_obj = self.pool.get('account.journal')
        journal_search = [('company_id', '=', company_id)]
        journal_ids = journal_obj.search(cr,
                                         uid,
                                         journal_search,
                                         context=context)
        tndb.wlog('p', period_ids)
        tndb.wlog('j', journal_ids)

        # move (rec.contabili)
        move_obj = self.pool.get('account.move')
        move_search = [('company_id', '=', company_id),
                       ('date', '>=', date_start),
                       ('date', '<=', date_stop)]
        move_ids = move_obj.search(cr,
                                   uid,
                                   move_search,
                                   context=context)
        tndb.wlog('m', move_ids)
        for move_rec in self.pool.get('account.move').browse(cr,
                                                             uid,
                                                             move_ids):
            tndb.wlog('move', move_rec.id)

        # invoice_obj = self.pool.get('account.invoice')
        # partner_obj = self.pool.get('res.partner')
        # account_move_obj = self.pool.get('account.move')
        # invoice_obj = self.pool.get('account.invoice')
