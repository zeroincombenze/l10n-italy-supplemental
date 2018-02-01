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

# This wizard update partners entered using the old italian localization.


from osv import fields, osv
from openerp import pooler
from tools.translate import _


class partner_update_wizard(osv.TransientModel):
    _name = 'partner.update.wizard'
    _columns = {
        'state': fields.selection([('step1', 'step1'), ('step2', 'step2')]),
        'log': fields.text('Log')
    }

    _defaults = {
        'state': 'step1'
    }

# It looks for partners to update and update them.
# It returns a log file with evidence of operations done.
    def partner_update(self, cr, uid, ids, context=None):
        log = ''
        user = pooler.get_pool(cr.dbname).get('res.users').browse(cr, uid, uid)
        italy = pooler.get_pool(cr.dbname).get('res.country').search(
            cr, uid, [('code', '=', 'IT')])
        partners = pooler.get_pool(
            cr.dbname).get(
            'res.partner').search(cr,
                                  uid,
                                  [('province', '!=', None),
                                   ('state_id', '=', None),
                                   '|',
                                   ('company_id.id', '=', user.company_id.id),
                                   ('company_id.id', 'child_of',
                                    user.company_id.id)])
        n_partners = len(partners)
        if n_partners > 0:
            p = pooler.get_pool(cr.dbname).get('res.partner')
            for i in range(n_partners):
                partner_obj = pooler.get_pool(
                    cr.dbname).get('res.partner').browse(
                    cr, uid, partners[i])
                if partner_obj:
                    if partner_obj.country_id:
                        country_to_find = partner_obj.country_id.id
                        update_country = False
                    else:
                        country_to_find = italy[0]
                        update_country = True

                    state_id = self.pool.get('res.country.state').search(
                        cr, uid, [('code', '=', partner_obj.province.code),
                                  ('country_id', '=', country_to_find)])
                    if state_id:
                        state_obj = pooler.get_pool(
                            cr.dbname).get('res.country.state').browse(
                            cr, uid, state_id[0])
                        if state_obj:
                            if update_country:
                                vals = {
                                    'state_id': state_obj.id,
                                    'country_id': country_to_find}
                            else:
                                vals = {'state_id': state_obj.id}
                            id_upd = [partner_obj.id]
                            p.write(cr, uid, id_upd, vals, context=context)
                            log += _('Updated: ') + partner_obj.name
                            log += ' ' + partner_obj.zip + ' '
                            log += partner_obj.city + ' '
                            log += state_obj.code + ' \n'

            log += _('Updated Partners: ') + str(n_partners)

            cpy = pooler.get_pool(cr.dbname).\
                get('res.company').search(cr,
                                          uid,
                                          ['|',
                                           ('id', '=',
                                            user.company_id.id),
                                           ('id', 'child_of',
                                            user.company_id.id)])
            c = pooler.get_pool(cr.dbname).get('res.company')
            for i in range(len(cpy)):
                c.write(cr, uid, cpy[i],
                        {'it_partner_updated': True},
                        context=context)

        else:
            log += _('No Partner needs to be updated.')

        self.write(cr, uid, ids,
                   {'state': 'step2', 'log': log},
                   context=context)
        wiz = self.browse(cr, uid, ids, context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'partner.update.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz[0].id,
            'views': [(False, 'form')],
            'target': 'new',
            'context': context,
        }
