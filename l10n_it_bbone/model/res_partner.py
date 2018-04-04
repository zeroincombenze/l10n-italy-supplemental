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
import string
#import pdb
from openerp import models
from openerp import api
from openerp import fields
from openerp.osv import fields
from openerp import pooler
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


_ERR_ZIP_STATE_ID = 'Inconsistent District/State with selected ZIP code.'
_ERR_STATE_ID = 'Inconsistent Country with selected District/State.'


class ResRegion(models.Model):
    _name = 'res.region'
    _description = 'Region'
    _columns = {
        'name': fields.char(
            'Region Name', size=64, help='The full name of the region.',
            required=True),
        'country_id': fields.many2one('res.country', 'Country'),
    }


ResRegion()


# Deprecated: used just for previous version of Italian localization
class ResProvince(models.Model):
    _name = 'res.province'
    _description = 'Province'
    _columns = {
        'name': fields.char(
            'Province Name', size=64, help='The full name of the province.',
            required=True),
        'code': fields.char(
            'Province Code', size=2, help='The province code in two chars.',
            required=True),
        'region': fields.many2one('res.region', 'Region'),
    }


ResProvince()


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    _columns = {
        'eurostat_code': fields.char('EUROSTAT Code', size=16,
                                     help='EUROSTAT Code.'),
    }


ResCountryState()


class ResCity(models.Model):
    _name = 'res.city'
    _description = 'City'
    _columns = {
        'name': fields.char('City',
                            size=64,
                            help='Official city name.',
                            required=True),
        'province_id': fields.many2one('res.province', 'Province'),
        'zip': fields.char('CAP',
                           size=16,
                           help='City\'s ZIP code. (Country dependent).'),
        'phone_prefix': fields.char('Telephone Prefix', size=16),
        'istat_code': fields.char('ISTAT code', size=16),
        'cadaster_code': fields.char('Cadaster Code', size=16),
        'web_site': fields.char('Web Site', size=64),
        'region': fields.related(
            'province_id', 'region', type='many2one', relation='res.region',
            string='Region', readonly=True),
        'country_id': fields.many2one('res.country',
                                      'Country',
                                      help='Country encoded by ISO-3166.',
                                      required=True),
        'state_id': fields.many2one(
            'res.country.state',
            'District',
            help='Upper administration (Province, District or Federal State).',
            domain="[('country_id', '=', country_id)]"),
        'nuts': fields.integer('NUTS', size=1),
    }

    def on_change_state(self, cr, uid, ids, state_id):
        # state is sublevel of country
        # in Italy is called province
        # in order to keep back compatibility with Italian Localization
        # field state is copied into province (just for Italy)
        # [antoniov] context.update({'periods': period_ids})
        # [antoniov] ctx = context.copy()
        res = {'value': {}}
        if(state_id):
            state_obj = self.pool.get('res.country.state').browse(
                cr, uid, state_id)
            prov_id = self.pool.get('res.province').search(
                cr, uid, [('code', '=ilike', state_obj.code)])
            if prov_id:
                prov_obj = self.pool.get('res.province').browse(
                    cr, uid, prov_id[0])
                res = {'value': {
                    'province_id': prov_obj.id and prov_obj.id or False
                }
                }
            else:
                res = {'value': {'province_id': None, }}
        else:
            res = {'value': {'province_id': None, }}

        return res


ResCity()


class ResUsers(models.Model):
    _inherit = 'res.users'

    _columns = {
        'partner_warning_messages': fields.boolean(
            'Address Warning Messages',
            help='This user can/can\'t see all the address warning messages'),
    }


ResUsers()


class ResCountry(models.Model):
    _inherit = 'res.country'

    _columns = {
        'ufficioiva': fields.char(
            'VAT Office Code', size=4,
            help='VAT Office Code'),
        'inue': fields.boolean(
            'Member of EU',
            help='This country is member of the European Union.'),
        'inue_date': fields.date(
            'Member of EU from',
            help='This country is member of the European Union since'),
        'blacklist': fields.boolean(
            'Blacklist',
            help='This country is in blacklist.'),
        'blacklist_date': fields.date(
            'Blacklist from',
            help='This country is in blacklist since this date.'),
        'insepa': fields.boolean(
            'Use SEPA',
            help='This country use SEPA standard.'),
        'insepa_date': fields.date(
            'Use SEPA from',
            help='This country use SEPA standard since this date.'),
        'ean': fields.char(
            'GTIN Code', size=3,
            help='GTIN Code. (EAN Code).'),
        'lingua': fields.char(
            'Language', size=2,
            help='Official language of this country.'),
        'chk4addr': fields.integer(
            'Check on address', size=1,
            help='Enable or disable check on address.'),
        'chk4zip': fields.integer(
            'Multizone ZIP code', size=1,
            help='Number of digits in multizone ZIP code by this country'),
    }


ResCountry()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    _columns = {
        'province': fields.many2one('res.province', string='Province'),
        'region': fields.many2one('res.region', string='Region'),
        'state_id': fields.many2one('res.country.state',
                                    'State',
                                    domain="[('country_id', '=', country_id)]")
    }

# Disable built-in automatic field positioning on web page
    def fields_view_get_address(self, cr, uid, arch, context=None):
        return arch

# In order to keep compatibilities with italian localization modules
# set province_id as copy of state_id (if country is Italy)
# Deprecated: to remove in future implementation
    def on_change_state(self, cr, uid, ids, state_id):
        res = {}
        if(state_id):
            state_obj = self.pool.get('res.country.state').browse(
                cr, uid, state_id)
            if state_obj.country_id.code == 'IT':
                prov_id = self.pool.get('res.province').search(
                    cr, uid, [('code', '=ilike', state_obj.code)])
                if prov_id:
                    prov_obj = self.pool.get('res.province').browse(
                        cr, uid, prov_id[0])
                    res = {'value':
                           {'province': prov_obj.id and prov_obj.id or False,
                            'region': prov_obj.region and prov_obj.region.id or
                            False}}

            else:
                res = {'value': {'province': None, 'region': None, }}
        else:
            res = {'value': {'province': None, 'region': None, }}
        return res

# Returns the website lowercase upon changing the website textbox
    @api.onchange('website')
    def on_change_website(self):
        self.website = self.website.lower()

# Call zip code validate and load values in city and state_id
# Based on table res.city
    def on_change_zip(self, cr, uid, ids, country_id, zip_code, city):
        return on_change_zip(cr, uid, ids, country_id, zip_code, city)

# Call city validate and load values in city and state_id.
# Based on table res.city but city can be changed by user.
    def on_change_city(self, cr, uid, ids, country_id, zip_code, city):
        return on_change_city(cr, uid, ids, country_id, zip_code, city)

    def _set_vals_city_data2(self, cr, uid, ids, vals):
        if 'country_id' in vals or\
                'zip' in vals or\
                'state_id' in vals or\
                'city' in vals:
            verif_country_id = set_def_country(cr, uid, vals, ids)
            if verif_country_id:
                vals['country_id'] = verif_country_id
            if verif_country_id:
                country_obj = pooler.get_pool(cr.dbname)\
                    .get('res.country').browse(cr, uid, verif_country_id)
                if country_obj.chk4addr > 0:
                    verif_zip = vals.get('zip', None)
                    if verif_zip and not zip_in_state_id(cr, uid, vals):
                        raise UserError(_('Error!'),         # pragma: no cover
                                        _(_ERR_ZIP_STATE_ID))
                    verif_state_id = vals.get('state_id', None)
                    if verif_state_id:
                        state_obj = self.pool.get('res.country.state').\
                            browse(cr, uid, int(verif_state_id))
                        if int(verif_country_id) != int(state_obj.country_id):
                            raise UserError(_('Error!'),     # pragma: no cover
                                            _(_ERR_STATE_ID))

    def create(self, cr, uid, vals, context=None):
        self._set_vals_city_data2(cr, uid, None, vals)
        return super(ResPartner, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        self._set_vals_city_data2(cr, uid, ids, vals)
        return super(ResPartner, self).write(cr, uid, ids, vals, context)

    def partner_update_wizard(self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'partner.update.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': context,
        }


ResPartner()


class ResCompany(models.Model):

    _inherit = 'res.company'
    _columns = {
        'it_partner_updated': fields.boolean(
            'Partner Updated',
            help='Your partners are updated by Italian localization'),
    }

# Call zip code validate and load values in city and state_id
# Based on table res.city
    def on_change_zip(self, cr, uid, ids, country_id, zip_code, city):
        return on_change_zip(cr, uid, ids, country_id, zip_code, city)

# Call city validate and load values in city and state_id.
# Based on table res.city but city can be changed by user.
    def on_change_city(self, cr, uid, ids, country_id, zip_code, city):
        return on_change_city(cr, uid, ids, country_id, zip_code, city)


ResCompany()


def set_def_country(cr, uid, vals, ids):
    """If not country id in vals, set country_id of current user"""
    if 'country_id' in vals:
        return vals['country_id']
    country_id = None
    if ids is not None:
        for i in ids:
            p_obj = pooler.get_pool(cr.dbname).\
                get('res.partner').browse(cr, uid, i)
            if p_obj.country_id.id:
                country_id = p_obj.country_id.id
                break
    if not country_id:
        p_obj = pooler.get_pool(cr.dbname).\
            get('res.users').browse(cr, uid, uid)
        country_id = p_obj.country_id.id
    return country_id


def zip_in_state_id(cr, uid, vals):
    verif_country_id = vals.get('country_id', None)
    if not verif_country_id:
        return True
    verif_zip = vals.get('zip', None)
    if not verif_zip:
        return True
    verif_state_id = vals.get('state_id', None)
    if not verif_state_id:
        return False
    verif_city = vals.get('city', None)
    if verif_city:
        city_ids = city_from_zip(cr,
                                 uid,
                                 verif_country_id,
                                 verif_zip,
                                 verif_city)
        if not city_ids:
            country_obj = pooler.get_pool(cr.dbname).\
                get('res.country').browse(cr, uid, verif_country_id)
            if country_obj.chk4addr > 0:
                zip_len = len(verif_zip) - country_obj.chk4zip
                xstr = 'x' * country_obj.chk4zip
                zip_big_city = verif_zip[0:zip_len] + xstr
                city_ids = city_from_zip(cr,
                                         uid,
                                         verif_country_id,
                                         zip_big_city,
                                         verif_city)
        if city_ids:
            for city_id in city_ids:
                valid_state_id = False
                city_obj = pooler.get_pool(cr.dbname).\
                    get('res.city').browse(cr, uid, city_id)
                if int(city_obj.state_id.id) == int(verif_state_id):
                    valid_state_id = True
                    break
            return valid_state_id
        return True
    return True


# Get ids from res.city for a given zip code. city (if passed) is used for
# query.
def city_from_zip(cr, uid, country_id, zip_code, city):
    if zip_code:
        vals = {}
        vals['country_id'] = country_id
        country_id = set_def_country(cr, uid, vals, [])
        if city:
            tofind = string.replace(city, '.', '%') + '%'
            city_ids = pooler.get_pool(cr.dbname)\
                .get('res.city').search(cr,
                                        uid,
                                        [('country_id', '=', country_id),
                                         ('zip', '=', zip_code),
                                         ('name', '=ilike', tofind),
                                         ('nuts', '<', 9)])
            if not city_ids and len(zip_code) == 5:
                zipx = zip_code[0:3] + "%%"
                city_ids = pooler.get_pool(cr.dbname)\
                    .get('res.city').search(cr,
                                            uid,
                                            [('country_id', '=', country_id),
                                             ('zip', '=ilike', zipx),
                                             ('name', '=ilike', tofind),
                                             ('nuts', '<', 9)])
            if not city_ids:
                city_ids = pooler.get_pool(cr.dbname)\
                    .get('res.city').search(cr,
                                            uid,
                                            [('country_id', '=', country_id),
                                             ('zip', '=ilike', zip_code),
                                             ('nuts', '<', 9)])
        else:
            city_ids = pooler.get_pool(cr.dbname)\
                .get('res.city').search(cr,
                                        uid,
                                        [('country_id', '=', country_id),
                                         ('zip', '=ilike', zip_code),
                                         ('nuts', '<', 9)])
        return city_ids
    else:
        return False


# Get ids from res.city for a given city. zip_code (if passed) is used for
# query.
def city_validate(cr, uid, ids, country_id, zip_code, city):
    if city:
        if not zip_code:
            zip_code = '%'
        if not country_id:
            user_obj = pooler.get_pool(cr.dbname)\
                .get('res.users').browse(cr, uid, uid)
            country_id = user_obj.country_id.id
        tofind = string.replace(city, '.', '%')
        city_ids = pooler.get_pool(cr.dbname)\
            .get('res.city').search(cr,
                                    uid,
                                    [('country_id', '=', country_id),
                                     ('zip', '=ilike', zip_code),
                                     ('name', '=ilike', tofind),
                                     ('nuts', '<', 9)])
        if not city_ids:
            tofind = tofind + '%'
            city_ids = pooler.get_pool(cr.dbname)\
                .get('res.city').search(cr,
                                        uid,
                                        [('country_id', '=', country_id),
                                         ('zip', '=ilike', zip_code),
                                         ('name', '=ilike', tofind),
                                         ('nuts', '<', 9)])
        return city_ids
    else:
        return False


# Return True if given zip_code is 'multizona' (big cities like Turin
# where zeroincombenze was born)
def zip_mlzone(cr, uid, country_id, zip_code):
    res = False
    if zip_code and country_id:
        country_obj = pooler.get_pool(cr.dbname).get(
            'res.country').browse(cr, uid, country_id)
        if country_obj.chk4addr > 0:
            i = 1
            while i <= country_obj.chk4zip:
                zip_len = len(zip_code) - i
                xstr = 'x' * i
                zip_big_city = zip_code[0:zip_len] + xstr
                city_ids = pooler.get_pool(cr.dbname)\
                    .get('res.city').search(cr,
                                            uid,
                                            [('zip', '=ilike', zip_big_city),
                                             ('country_id', '=', country_id),
                                             ('nuts', '<', 9)])
                if city_ids:
                    break
                i += 1
            if city_ids:
                res = True
            else:
                res = False
    return res


def on_change_zip(cr, uid, ids, country_id, zip_code, city):
    res = {}
    user_obj = pooler.get_pool(cr.dbname)\
        .get('res.users').browse(cr, uid, uid)
    if not country_id:
        country_id = user_obj.country_id.id
    if zip_code and country_id:
        city_ids = city_from_zip(cr, uid, country_id, zip_code, city)
        if city_ids:
            city_obj = pooler.get_pool(cr.dbname)\
                .get('res.city').browse(cr, uid, city_ids[0])
            res = {'value': {
                'city': city_obj.name,
                'state_id': (city_obj.state_id and
                             city_obj.state_id.id or False),
            }
            }
            if len(city_ids) > 1 and user_obj.partner_warning_messages:
                msg = _('More cities with this ZIP code.')
                res['warning'] = {'title': 'Info', 'message': msg}
        else:
            # Check for validation country depended
            country_obj = pooler.get_pool(cr.dbname)\
                .get('res.country').browse(cr, uid, country_id)
            if country_obj.chk4addr > 0:
                i = 1
                while i <= country_obj.chk4zip:
                    zip_len = len(zip_code) - i
                    xstr = 'x' * i
                    zip_big_city = zip_code[0:zip_len] + xstr
                    city_ids = city_from_zip(cr,
                                             uid,
                                             country_id,
                                             zip_big_city,
                                             city)
                    if city_ids:
                        break
                    i += 1
                if city_ids:
                    city_obj = pooler.get_pool(cr.dbname)\
                        .get('res.city').browse(cr,
                                                uid,
                                                city_ids[0])
                    res = {'value': {
                        'city': city_obj.name,
                        'state_id': (
                            city_obj.state_id and
                            city_obj.state_id.id or False
                        ),
                    }
                    }
                else:
                    raise UserError(_('Error!'),             # pragma: no cover
                                    _('No City with selected ZIP code.'))
            else:
                if user_obj.partner_warning_messages:
                    msg = _('Unknown ZIP code')
                    res['warning'] = {'title': 'Info', 'message': msg}
    return res


def on_change_city(cr, uid, ids, country_id, zip_code, city):
    res = {}
    user_obj = pooler.get_pool(cr.dbname)\
        .get('res.users').browse(cr, uid, uid)
    if not country_id:
        country_id = user_obj.country_id.id
    if city and country_id:
        city_ids = city_validate(cr, uid, ids, country_id, zip_code, city)
        if city_ids:
            city_obj = pooler.get_pool(cr.dbname)\
                .get('res.city').browse(cr, uid, city_ids[0])
            res = {'value': {
                'city': city_obj.name,
                'state_id': (city_obj.state_id and
                             city_obj.state_id.id or False),
            }
            }
# Found unique city name and zip code is empty -> Load zip code.
            if len(city_ids) == 1 and not zip_code:
                city_ids = city_validate(cr,
                                         uid,
                                         ids,
                                         country_id,
                                         zip_code,
                                         city)
                if city_ids:
                    city_obj = pooler.get_pool(cr.dbname)\
                        .get('res.city').browse(cr, uid, city_ids[0])
                    res = {'value': {'zip': city_obj.zip}}
# If warning messages enabled by user show warnings
            elif len(city_ids) > 1 and user_obj.partner_warning_messages:
                msg = _('More cities like this one.')
                res['warning'] = {'title': 'Info', 'message': msg}
        else:
            if not zip_mlzone(cr, uid, country_id, zip_code) and\
                    user_obj.partner_warning_messages:
                msg = _('Unknown county.')
                res['warning'] = {'title': 'Info', 'message': msg}
    return res
