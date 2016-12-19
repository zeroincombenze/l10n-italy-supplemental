# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://ww.zeroincombenze.it>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either versiofn 3 of the
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
# from tools.translate import _


class res_partner(osv.osv):
    _inherit = 'res.partner'

    def check_4_fiscalcode(self, cr, uid, ids, context=None):

        context = {} if context is None else context
        for partner in self.browse(cr, uid, ids):
            if not partner.fiscalcode:
                return True
            elif len(partner.fiscalcode) != 16 and partner.individual:
                return False
            else:
                return True

    _columns = {
        'fiscalcode': fields.char('Fiscal Code',
                                  size=16,
                                  help="Italian Fiscal Code"),
    }

    _constraints = [(check_4_fiscalcode,
                     "The fiscal code doesn't seem to be correct.",
                     ["fiscalcode"])]


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
