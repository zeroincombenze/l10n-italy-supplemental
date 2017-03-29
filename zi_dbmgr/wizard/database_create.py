# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
#    All Rights Reserved
#
#    Written by Alessando Camilli (alessandrocamilli@openforce.it).
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


from osv import fields, osv


class wizard_database_create(osv.osv_memory):

    _name = "zi.dbmgr.db.create.database.wizard"
    _description = 'Use this wizard to create a new database'
    _columns = {
        'name': fields.char('Name', readonly=True),
        'user_password': fields.char('User Password Admin', required=True),
        'lang': fields.many2one('res.lang', 'Language', required=True),
        'demo': fields.boolean('Load Demo Data'),
    }
    _defaults = {
    }

    def execute(self, cr, uid, ids, data, context=None):

        zi_dbmgr_db_obj = self.pool['zi.dbmgr.db']
        res_lang_obj = self.pool['res.lang']

        for wiz_obj in self.read(cr, uid, ids):

            lang = res_lang_obj.browse(cr, uid, wiz_obj['lang'][0])
            params = {
                'name': wiz_obj['name'],
                'user_password':  wiz_obj['user_password'],
                'lang': lang.code,
                'demo': wiz_obj['demo']
            }

            zi_dbmgr_db_obj.create_database(cr, uid, params, context)

        return {'type': 'ir.actions.act_window_close'}

    def default_get(self, cr, uid, fields, context=None):

        service_db_config_obj = self.pool['zi.dbmgr.db.config']

        res = super(wizard_database_create, self).default_get(
            cr, uid, fields, context=context)

        config = service_db_config_obj.get_config(cr, uid, context=None)

        res.update({'name': config.new_db_name})
        res.update({'user_password': config.new_db_user_password})
        res.update({'lang': config.new_db_lang.id})
        res.update({'demo': config.new_db_demo})

        return res
