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
#    Zeroincombenze(R) users pay for use SaaS. They can record their own invoices
#    just for reconciled (payed) months. 
#
##############################################################################

from openerp import SUPERUSER_ID
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _



class ZIClienteAttivo(orm.Model):
#
# Reconciliation record of table 'res.cliente_attivo' has 13 boolean values.
# 1.st is full year; next 12 values are 1 for every month 
#
    _name = "res.cliente_attivo"
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
        ('name_year_uniq', 'unique (name,year)', 'ID Cliente e Anno sono i campi chiave !')
    ]



class account_invoice(osv.osv):
#
# Check for writable invoice
#
    _inherit = 'account.invoice'

    def create(self, cr, uid, vals, context=None):
        if vals.get('date_invoice'):
            data_da_verificare = vals.get('date_invoice')
            self.cliente_pagante_mese(cr, uid, data_da_verificare, 'Data Fattura', context=None)
        return super(account_invoice, self).create(cr, uid, vals, context=context)


    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('date_invoice'):
            data_da_verificare = vals.get('date_invoice')
            self.cliente_pagante_mese(cr, uid, data_da_verificare, 'Data Fattura', context=None)
        return super(account_invoice, self).write(cr, uid, ids, vals, context=context)


    def cliente_pagante_mese(self, cr, uid, data_da_controllare, nome_data, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid)
#        if user.login[1]=='0':        # [antoniov 2014-07-14 chanded with SUPERUSER_ID
        if uid != SUPERUSER_ID:
            user_login = user.login[0:8]
            if data_da_controllare:
                year_invoice = int(data_da_controllare[0:4])
                if year_invoice > 2013 :                        # Before 2014, records are permitted
                    month_invoice = data_da_controllare[5:7]
                    user_acc_obj = self.pool.get('res.cliente_attivo')
                    user_acc_ids = user_acc_obj.search(cr, uid, [('name','=',user_login),('year','=',year_invoice)])
                    if user_acc_ids :
                        cli = user_acc_obj.browse(cr,uid,user_acc_ids)[0]
                        if  cli.period_0 == False:
                            if month_invoice == '01' and cli.period_1 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Gennaio %s.') % year_invoice)
                            if month_invoice == '02' and cli.period_2 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Febbraio %s.') % year_invoice)
                            if month_invoice == '03' and cli.period_3 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Marzo %s.') % year_invoice)
                            if month_invoice == '04' and cli.period_4 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Aprile %s.') % year_invoice)
                            if month_invoice == '05' and cli.period_5 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Maggio %s.') % year_invoice)
                            if month_invoice == '06' and cli.period_6 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Giugno %s.') % year_invoice)
                            if month_invoice == '07' and cli.period_7 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Luglio %s.') % year_invoice)
                            if month_invoice == '08' and cli.period_7 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Agosto %s.') % year_invoice)
                            if month_invoice == '09' and cli.period_7 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Settembre %s.') % year_invoice)
                            if month_invoice == '10' and cli.period_10 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Ottobre %s.') % year_invoice)
                            if month_invoice == '11' and cli.period_11 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Novembre %s.') % year_invoice)
                            if month_invoice == '12' and cli.period_12 == False:
                                raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare in Dicembre %s.') % year_invoice)
                    else :
                        raise orm.except_orm(_('Errore %s') % nome_data, _('Il tuo utente non è abilitato a registrare!'))
        return True



class res_users(osv.Model):
    _name = 'res.users'
    _inherit = ['res.users']
    
    
    def create(self, cr, uid, data, context=None):
#
# Add accounting record for every new user
#
        user_id = super(res_users, self).create(cr, uid, data, context=context)
        user_obj = self.browse(cr, uid, user_id, context=context)
        user_login = user_obj.login[0:8]
        if user_login[1]=='0':
            user_acc_obj = self.pool.get('res.cliente_attivo')
            user_acc_obj.create(cr, uid, {
                                         'name': user_login,
                                         'year': 2014,
                                         'period_0' : False,
                                         'period_1' : False,
                                         'period_2' : False,                
                                         'period_3' : False,
                                         'period_4' : False,
                                         'period_5' : False,
                                         'period_6' : False,
                                         'period_7' : False,
                                         'period_8' : False,
                                         'period_9' : False,                
                                         'period_10': False,
                                         'period_11': False,
                                         'period_12': False,
                                        }, context=context)
        return user_id


