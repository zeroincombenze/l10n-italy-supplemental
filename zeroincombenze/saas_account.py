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
#
#    Check for SaaS users accounting
#    Zeroincombenze® users pay for use SaaS. They can record thei own invoices
#    just for reconciled (payed) months.
#
##############################################################################

from openerp import SUPERUSER_ID
from openerp.osv import fields, osv, orm
# from datetime import date
from openerp.tools.translate import _


class saas_account(orm.Model):
    #
    # Reconciliation record of table 'res.saas_account' has 13 boolean values.
    # 1.st is full year; next 12 values are 1 for every month
    #
    _name = "res.saas_account"
    _description = "Cliente Attivo"

    _columns = {
        'name': fields.char('ID Cliente', required=True, size=8),
        'year': fields.integer('Anno', required=True),
        'period_0': fields.boolean('Tutto'),
        'period_1': fields.boolean('Gennaio'),
        'period_2': fields.boolean('Febbraio'),
        'period_3': fields.boolean('Marzo'),
        'period_4': fields.boolean('Aprile'),
        'period_5': fields.boolean('Maggio'),
        'period_6': fields.boolean('Giugno'),
        'period_7': fields.boolean('Luglio'),
        'period_8': fields.boolean('Agosto'),
        'period_9': fields.boolean('Settembre'),
        'period_10': fields.boolean('Ottobre'),
        'period_11': fields.boolean('Novembre'),
        'period_12': fields.boolean('Dicembre'),
    }

    _order = "name asc,year desc"

    _sql_constraints = [
        ('name_year_uniq', 'unique (name,year)',
         'ID Cliente e Anno sono i campi chiave !')
    ]


class account_invoice(osv.osv):
    #
    # Check for writable invoice
    #
    _inherit = 'account.invoice'

    def create(self, cr, uid, vals, context=None):
        if vals.get('date_invoice'):
            data_da_verificare = vals.get('date_invoice')
            self.cliente_pagante_mese(
                cr, uid, data_da_verificare, 'Data Fattura', context=None)
        return super(account_invoice, self).create(cr,
                                                   uid,
                                                   vals,
                                                   context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('date_invoice'):
            data_da_verificare = vals.get('date_invoice')
            self.cliente_pagante_mese(
                cr, uid, data_da_verificare, 'Data Fattura', context=None)
        return super(account_invoice, self).write(cr,
                                                  uid,
                                                  ids,
                                                  vals,
                                                  context=context)

    def cliente_pagante_mese(self, cr, uid, data_da_controllare, nome_data,
                             context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid)
        if uid != SUPERUSER_ID:
            user_login = user.login[0:8]
            if data_da_controllare:
                year_invoice = int(data_da_controllare[0:4])
                # Before 2014, records are permitted
                if year_invoice > 2013:
                    month_invoice = data_da_controllare[5:7]
                    user_acc_obj = self.pool.get('res.saas_account')
                    user_acc_ids = user_acc_obj.search(
                        cr, uid, [('name', '=', user_login),
                                  ('year', '=', year_invoice)])
                    if user_acc_ids:
                        cli = user_acc_obj.browse(cr, uid, user_acc_ids)[0]
                        if not cli.period_0:
                            msgerr = 'Registrazioni non permesse in %s %s!'
                            if month_invoice == '01' and not cli.period_1:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Gennaio', year_invoice))
                            elif month_invoice == '02' and not cli.period_2:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Febbraio', year_invoice))
                            elif month_invoice == '03' and not cli.period_2:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Marzo', year_invoice))
                            elif month_invoice == '04' and not cli.period_2:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Aprile', year_invoice))
                            elif month_invoice == '05' and not cli.period_2:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Maggio', year_invoice))
                            elif month_invoice == '06' and not cli.period_2:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Giugno', year_invoice))
                            elif month_invoice == '07' and not cli.period_2:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Luglio', year_invoice))
                            elif month_invoice == '08' and not cli.period_2:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Agosto', year_invoice))
                            elif month_invoice == '09' and not cli.period_2:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Settembre', year_invoice))
                            elif month_invoice == '10' and not cli.period_2:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Ottobre', year_invoice))
                            elif month_invoice == '11' and not cli.period_2:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Novembre', year_invoice))
                            elif month_invoice == '12' and not cli.period_2:
                                raise orm.except_orm(
                                    _('Errore %s') % nome_data,
                                    _(msgerr) % ('Dicembre', year_invoice))
                    else:
                        pass
                        # raise orm.except_orm(_('Errore %s') % nome_data,
                        # _('Registrazioni non permesse!'))
        return True


class res_users(osv.Model):
    _name = 'res.users'
    _inherits = {
        'res.partner': 'partner_id',
    }
    _inherit = ['res.users']

    def __init__(self, pool, cr):
        super(res_users, self).__init__(pool, cr)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
