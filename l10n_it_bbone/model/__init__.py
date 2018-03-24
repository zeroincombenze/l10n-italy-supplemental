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

from . import res_partner
# Due to some incompatbility, check for Italian base module installation
# if pool.get('ir.module.module').search(cr, uid, [('name',
# '=ilike', 'l10n_it_base')]):
#    L10N_IT_BASE_INSTALLED = True
# else:
#    L10N_IT_BASE_INSTALLED = False
# enable wizard if you have to convert old data of l10n_it_base
# into new OCA standard
# import wizard
