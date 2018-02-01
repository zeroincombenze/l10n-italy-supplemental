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

from openerp.osv import osv
from openerp.osv import fields
import re


class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _get_birthday(self, cr, uid, ids, field_names, arg, context=None):
        """ Read string birthday from res.partner """
        res = {}
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.birthdate:
                f = partner.birthdate
                if re.match('[0-9]{4}.[0-9]{2}.[0-9]{2}', f):
                    res[partner.id] = f[0:4] + '-' + f[5:7] + '-' + f[8:10]
                elif re.match('[0-9]{2}.[0-9]{2}.[0-9]{4}', f):
                    res[partner.id] = f[6:10] + '-' + f[3:5] + '-' + f[0:2]
        return res

    def _set_birthday(self, cr, uid, partner_id, name, value, arg,
                      context=None):
        """ Write string birthday to res.partner """
        self.write(cr,
                   uid,
                   [partner_id],
                   {'birthdate': value or False},
                   context=context)
        return True

    _columns = {
        'birthday': fields.function(_get_birthday,
                                    fnct_inv=_set_birthday,
                                    type='date',
                                    string='Birth date')
    }
