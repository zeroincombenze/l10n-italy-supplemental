# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2010 Odoo Italian Community (<http://www.odoo-italia.org>).
#    Copyright (C) SHS-AV s.r.l. (<http://ww.zeroincombenze.it>)
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

from openerp.osv import osv, orm
from openerp.osv import fields


FLDS_LIST = ['country_id', 'state_id', 'province_id', 'region_id']


class res_config_settings(orm.TransientModel):
    _inherit = 'res.config.settings'
    _columns = {
        'zip': fields.many2one('res.city'),
        'city': fields.many2one('res.city',
                                domain="[('country_id', '=', country_id)]"),
        'state_id':
            fields.many2one('res.country.state',
                            domain="[('country_id', '=', country_id)]"),
        'province_id': fields.many2one('res.province', string='Province'),
        'region_id': fields.many2one('res.region', string='Region'),
    }

    def fld_in_model(self, model, f, name):
        if f in model._columns:
            return f
        elif name in model._columns:
            return name
        return False

    def fill_geocity(self, cr, uid, ids, name, value, context=None):
        """Set values of geolocalization from country, zip, city
        and other fields."""
        # tndb.wstamp(name, value)
        context = {} if context is None else context
        res_obj = self.pool.get('res.partner')
        city_obj = self.pool.get('res.city')
        state_obj = self.pool.get('res.country.state')
        province_obj = self.pool.get('res.province')
        search_in_it = False
        is_updated = False
        flds = FLDS_LIST
        names = {}
        for f in flds:
            if f[-3:] == '_id':
                names[f] = f[0: -3]
            else:
                names[f] = f
        fix = {}
        for f in flds:
            fix[f] = False
            if f != name:
                if not hasattr(self, f) and f in context and context[f]:
                    setattr(self, f, context[f])
                    # tndb.wlog(f, '=ctx(', context[f], ')')
                elif hasattr(self, f) and \
                        f not in context and f != 'country_id':
                    delattr(self, f)
                    # tndb.wlog('del', f)
        fix[name] = True
        if not hasattr(self, name) or value != getattr(self, name):
            is_updated = True
            # tndb.wlog(name, 'is updated')
            if value:
                res = False
                for i, f in enumerate(flds):
                    if f == name and i < 3:
                        res = True
                    elif res:
                        fix[f] = True
                        if hasattr(self, f):
                            delattr(self, f)
                        # tndb.wlog('clear ', f)
                if value:
                    setattr(self, name, value)
                    # tndb.wlog(name, '=', value)
                else:
                    delattr(self, name)
                    # tndb.wlog('del', name)
        # This module is for Italy so country is supposed to be Italy
        if not hasattr(self, 'country_id'):
            country_id = self.pool.get(
                'res.country').search(cr,
                                      uid,
                                      [('code', '=', 'IT')])
            if len(country_id):
                f = 'country_id'
                setattr(self, f, country_id[0])
                # tndb.wlog(f, '=', country_id[0])
                fix[f] = True
                # tndb.wlog('fix[', f, '] = True')
        # prepare city where
        where = []
        for f in flds:
            tbl_f = self.fld_in_model(city_obj, f, names[f])
            # tndb.wlog(tbl_f, '= self.fld_in_model(city_obj,', f,
            #          ', names[f]);', names[f])
            # tndb.wlog('123>if hasattr(self, ', f, ') and tbl_f:',
            #           hasattr(self, f), tbl_f)
            if hasattr(self, f) and tbl_f:
                if f[-3:] == '_id':
                    where.append((tbl_f, '=', getattr(self, f)))
                else:
                    tofind = getattr(self, f).replace('.', '%') + '%'
                    where.append((tbl_f, '=ilike', tofind))
                    if tofind.find('%') < 0:
                        fix[f] = False
                        # tndb.wlog('fix[', f, '] = False')
                    else:
                        fix[f] = True
                        # tndb.wlog('fix[', f, '] = True')
        if hasattr(self, 'country_id'):
            if self.pool.get(
                    'res.country').browse(cr,
                                          uid,
                                          self.country_id).code == 'IT':
                search_in_it = True
                # tndb.wlog('search_in_it =', search_in_it)
        res = True
        f = 'country_id'
        tbl_f = self.fld_in_model(city_obj, f, names[f])
        # tndb.wlog(tbl_f, '= self.fld_in_model(city_obj,', f, ', names[f]);',
        #           names[f])
        # tndb.wlog('150>if (search_in_it or tbl_f) and '
        #           'is_updated and len(where):',
        #           search_in_it, tbl_f,
        #           is_updated, '(', where, ')')
        if (search_in_it or tbl_f) and is_updated and len(where):
            city_ids = city_obj.search(cr, uid, where)
            # tndb.wlog('search(city,', where, ')=', city_ids)
            if not len(city_ids):
                for i, x in enumerate(where):
                    if x[0] == 'zip':
                        tofind = getattr(self, 'zip')[0:3] + '%'
                        y = (x[0], x[1], tofind)
                        where[i] = y
                        fix['zip'] = False
                    elif x[0] == 'name':
                        tofind = getattr(self, 'city').replace('.', '%')
                        y = (x[0], 'ilike', tofind)
                        where[i] = y
                        if tofind.find('%') < 0:
                            fix[f] = False
                        else:
                            fix[f] = True
                city_ids = city_obj.search(cr, uid, where)
                # tndb.wlog('search(city,', where, ')=', city_ids)
            if len(city_ids):
                city = city_obj.browse(cr, uid, city_ids[0])
                r = {}
                for f in flds:
                    res_f = self.fld_in_model(res_obj, f, names[f])
                    tbl_f = self.fld_in_model(city_obj, f, names[f])
                    # tndb.wlog(tbl_f, '= self.fld_in_model(city_obj,', f,
                    #           ', names[f]);', names[f])
                    # tndb.wlog('172>if tbl_f and hasattr(city, tbl_f) and',
                    #           '(not hasattr(self, ', f, ') or',
                    #           '(fix[f] and len(city_ids) == 1)):',
                    #           tbl_f,
                    #           hasattr(city, tbl_f or 'NA'),
                    #           hasattr(self, f), fix[f],
                    #           city_ids)
                    if tbl_f and hasattr(city, tbl_f) and \
                            (not hasattr(self, f) or
                             (fix[f] and len(city_ids) == 1)):
                        if f[-3:] == '_id':
                            r[res_f] = getattr(city, tbl_f).id
                        else:
                            r[res_f] = getattr(city, tbl_f)
                        # tndb.wlog('r[', res_f, '] = ', r[res_f])
                    if res_f in r:
                        setattr(self, f, r[res_f])
                        # tndb.wlog(f, '=', r[res_f])
                f = 'province_id'
                f1 = 'state_id'
                # tndb.wlog('201>if', hasattr(self, f1), 'and (not',
                #           hasattr(self, f), 'or(', fix[f],
                #           'and len(city_ids)==', city_ids, '))')
                if hasattr(self, f1) and \
                        (not hasattr(self, f) or
                         (fix[f] and len(city_ids) == 1)):
                    state = state_obj.browse(cr,
                                             uid,
                                             getattr(self, f1))
                    w = []
                    res_f = self.fld_in_model(res_obj, f, names[f])
                    tbl_f = self.fld_in_model(province_obj,
                                              'country_id',
                                              names['country_id'])
                    # tndb.wlog(tbl_f, '= self.fld_in_model(city_obj,', f,
                    #           ', names[f]);', names[f])
                    if tbl_f:
                        w.append((tbl_f, '=', getattr(self, 'country_id')))
                    w.append(('code', '=', state.code))
                    state_ids = province_obj.search(cr,
                                                    uid,
                                                    w)
                    # tndb.wlog('search(province,', w, ')=', state_ids)
                    if len(state_ids) == 1:
                        r[res_f] = state_ids[0]
                        # tndb.wlog('r[', res_f, '] = ', state_ids[0])
                        setattr(self, f, r[res_f])
                        # tndb.wlog(f, '=', r[res_f])
                f = 'state_id'
                f1 = 'province_id'
                # tndb.wlog('228>if', hasattr(self, f1), 'and (not',
                #           hasattr(self, f), 'or(', fix[f],
                #           'and len(city_ids)==', city_ids, '))')
                if hasattr(self, f1) and \
                        (not hasattr(self, f) or
                         (fix[f] and len(city_ids) == 1)):
                    province = province_obj.browse(cr,
                                                   uid,
                                                   getattr(self, f1))
                    w = []
                    res_f = self.fld_in_model(res_obj, f, names[f])
                    tbl_f = self.fld_in_model(state_obj,
                                              'country_id',
                                              names['country_id'])
                    # tndb.wlog(tbl_f, '= self.fld_in_model(city_obj,', f,
                    #           ', names[f]);', names[f])
                    if tbl_f:
                        w.append((tbl_f, '=', getattr(self, 'country_id')))
                    w.append(('code', '=', province.code))
                    state_ids = state_obj.search(cr,
                                                 uid,
                                                 w)
                    # tndb.wlog('search(state,', w, ')=', state_ids)
                    if len(state_ids) == 1:
                        r[res_f] = state_ids[0]
                        # tndb.wlog('r[', res_f, '] = ', state_ids[0])
                        setattr(self, f, r[res_f])
                        # tndb.wlog(f, '=', r[res_f])
                f = 'country_id'
                if fix[f] and f not in r:
                    r[f] = getattr(self, f)
                res = {'value': r}
                # tndb.wlog('fix', fix)
                # tndb.wlog('res =', res)
        return res


class res_city(osv.osv):
    _inherit = 'res.city'


    def new_ctx(self,
                country_id, zip, city, state_id, province_id, region_id,
                context=None):
        context = {} if context is None else context
        if country_id:
            context['country_id'] = country_id
        if state_id:
            context['state_id'] = state_id
        if province_id:
            context['province_id'] = province_id
        if region_id:
            context['region_id'] = region_id
        return context

    def on_change_country(self, cr, uid, ids,
                          country_id, state_id, province, region,
                          context=None):
        context = self.new_ctx(country_id, state_id,
                               province, region, context=context)
        config_obj = self.pool.get('res.config.settings')
        return config_obj.fill_geocity(cr, uid, ids, 'country_id', country_id,
                                       context=context)

    def on_change_state(self, cr, uid, ids,
                        country_id, state_id, province, region,
                        context=None):
        context = self.new_ctx(country_id, state_id,
                               province, region, context=context)
        config_obj = self.pool.get('res.config.settings')
        return config_obj.fill_geocity(cr, uid, ids, 'state_id', state_id,
                                       context=context)

    def on_change_province(self, cr, uid, ids,
                           country_id, state_id, province, region,
                           context=None):
        context = self.new_ctx(country_id, state_id,
                               province, region, context=context)
        config_obj = self.pool.get('res.config.settings')
        return config_obj.fill_geocity(cr, uid, ids, 'province_id', province,
                                       context=context)

    def on_change_region(self, cr, uid, ids,
                         country_id, state_id, province, region,
                         context=None):
        context = self.new_ctx(country_id, state_id,
                               province, region, context=context)
        config_obj = self.pool.get('res.config.settings')
        return config_obj.fill_geocity(cr, uid, ids, 'region_id', region,
                                       context=context)
