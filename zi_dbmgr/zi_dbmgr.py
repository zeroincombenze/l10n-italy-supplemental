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

from openerp.osv import fields, orm
from openerp.tools.translate import _
from service.web_services import db
from openerp import addons
import ConfigParser

# from tndb import tndb


class zi_dbmgr_db_config(orm.Model):

    _name = 'zi.dbmgr.db.config'

    def _init_conf(self):
        cfg_obj = ConfigParser.SafeConfigParser()
        s = "Environment"
        cfg_obj.add_section(s)
        cfg_obj.set(s, 'store_into_db', '0')
        cfg_obj.set(s, 'new_db_name_prefix', 'zi')
        cfg_obj.set(s, 'new_db_name_count_lenght', '8')
        cfg_obj.set(s, 'new_db_name_rule', 'GTIN')
        cfg_obj.set(s, 'new_db_name_suffix', '')
        s = "Local"
        cfg_obj.add_section(s)
        cfg_obj.set(s, 'new_db_name_next_count', '1')
        conf_file = addons.get_module_resource(
            'zi_dbmgr', 'conf', 'zi_dbmgr.ini')
        if conf_file:
            cfg_obj.read(conf_file)
        return cfg_obj

    def _new_db_name_get(self, cr, uid, ids, field_names, args, context=None):
        cfg_obj = self._init_conf()
        s = "Environment"
        if cfg_obj.getboolean(s, "store_into_db"):
            res = {}
            for conf in self.browse(cr, uid, ids, context=None):
                if conf.new_db_name_prefix:
                    name = conf.new_db_name_prefix
                else:
                    name = ''
                if conf.new_db_name_rule == 'GTIN':
                    name = name + \
                        self.eval_GTIN(
                            cr, uid, conf.new_db_name_next_count, context)
                else:
                    name = name + \
                        str(conf.new_db_name_next_count).zfill(
                            conf.new_db_name_count_lenght)
                if conf.new_db_name_suffix:
                    name = name + conf.new_db_name_suffix
                res[conf.id] = name
        else:
            res = {}
            i = cfg_obj.getint("Local", "new_db_name_next_count")
            l = cfg_obj.getint(s, "new_db_name_count_lenght")
            name = cfg_obj.get(s, "new_db_name_prefix")
            if cfg_obj.get(s, "new_db_name_prefix") == 'GTIN':
                name = name + self.eval_GTIN(i)
            else:
                name = name + str(i).zfill(l)
            name = name + cfg_obj.get(s, "new_db_name_suffix")
            res[1] = name
        return res

    _columns = {
        'sequence': fields.integer('Sequence'),
        'active': fields.boolean('Active'),
        'new_db_name_prefix': fields.char('Name - Prefix', required=False),
        'new_db_name_count_lenght':
            fields.integer('Name - Lengh Count', required=True),
        'new_db_name_next_count': fields.integer('Name - Next Count'),
        'new_db_name_suffix': fields.char('Name - Suffix', required=False),
        'new_db_name_rule': fields.char('Name - Rule', required=True),
        'new_db_name':
            fields.function(_new_db_name_get,
                            type='char',
                            string='Name Next Database', readonly=True),
        'new_db_user_password': fields.char('User Password', required=True),
        'new_db_lang': fields.many2one('res.lang', 'Language', required=True),
        'new_db_name_email': fields.char('User - Email', required=True),
        'new_db_demo': fields.boolean('Load Demo Data'),
    }
    _defaults = {
        'new_db_name_prefix': 'zi',
        'active': True,
        'new_db_name_count_lenght': 8,
        'new_db_name_next_count': 1,
        'new_db_name_rule': 'GTIN',
    }
    _order = "sequence"

    def eval_GTIN(self, cr, uid, last_accid, context=None):
        # pad 7 digits
        user_acc = '%07d' % last_accid
        chkdgt = 0
        for i in range(7):
            n = int(user_acc[i])
            if (i % 2):
                chkdgt = chkdgt + n
            else:
                chkdgt = chkdgt + n * 3
        chkdgt = chkdgt % 10
        if chkdgt:
            chkdgt = 10 - chkdgt
        user_acc = user_acc + str(chkdgt)

        return user_acc

    def get_config(self, cr, uid, context=None):
        config = False
        domain = [('active', '=', True)]
        conf_ids = self.search(cr, uid, domain, limit=1)
        if not conf_ids:
            raise orm.except_orm(_('Any Database Configuration'))
        config = self.browse(cr, uid, conf_ids[0])

        return config

    def increase_count(self, cr, uid, ids, context=None):

        for config in self.browse(cr, uid, ids):
            val = {
                'new_db_name_next_count':
                    config.new_db_name_next_count + 1 or False
            }
            self.write(cr, uid, [config.id], val)

        return True


class zi_dbmgr_db(orm.Model):

    _name = 'zi.dbmgr.db'

    def create_database(self, cr, uid, params=False, context=None):
        '''
        Create a new database
        @params:
            - name :
            - user_password :
            - lang :
            - demo :
        '''
        service_db_config_obj = self.pool['zi.dbmgr.db.config']
        config = service_db_config_obj.get_config(cr, uid, context=None)

        # Configuration setting
        if not params:
            params = {}
        if 'name' not in params or \
                not params['name']:
            params['name'] = config.new_db_name
        if 'user_password' not in params or \
                not params['user_password']:
            params['user_password'] = config.new_db_user_password
        if 'lang' not in params or \
                not params['lang']:
            params['lang'] = config.new_db_lang.code
        if 'demo' not in params or \
                not params['demo']:
            params['demo'] = config.new_db_demo

        # Creation
        service_db = db()
        db_name = params.get('name')
        db_pwd = params.get('user_password')
        # db_login = 'admin'
        try:
            #            service_db.exp_create_database(params.get('name'),
            #                                           params.get('demo'),
            #                                           params.get('lang'),
            #                                           params.get('user_password'))
            service_db.exp_create_database(db_name,
                                           params.get('demo'),
                                           params.get('lang'),
                                           db_pwd)
        except Exception, e:
            raise orm.except_orm(_('Error Creation Database'), _("%s") % (e))

        # Increase Count
        service_db_config_obj.increase_count(
            cr, uid, [config.id], context=None)
        # db = sql_db.db_connect(db_name)
        # cr = db.cursor()
        # security.login(db_name, db_login, db_pwd)

        return True
