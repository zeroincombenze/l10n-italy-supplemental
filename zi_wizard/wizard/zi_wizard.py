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

from osv import fields, osv 
from openerp import pooler

class cleanup_wizard(osv.TransientModel): 
    _name = 'idea.cleanup.wizard'
    _columns = { 
    'idea_age': fields.integer('Age (in days)'), 
    }

    def cleanup(self,cr,uid,ids,context=None): 
        partners = pooler.get_pool(cr.dbname).get('res.partner').search(cr, uid, 
            [('province', '!=', None),
            ('state_id', '=', None)])
        n_partners = len(partners)
#        raise osv.except_osv('UserError','Trovati %d' % n_partners) 
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'idea.cleanup.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'target': 'new',
             }