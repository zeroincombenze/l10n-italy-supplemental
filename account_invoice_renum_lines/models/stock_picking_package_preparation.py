# -*- coding: utf-8 -*-
#
# Copyright 2019-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from openerp import models, fields, api
from odoo.tools.float_utils import float_compare


class StockPickingPackagePreparation(models.Model):
    _inherit = 'stock.picking.package.preparation'
    
    @api.model
    def do_renum(self, ddt_lines):
        prior_so_ids = []
        last_so = False
        for item in ddt_lines.items():
            if item[1]['so']:
                last_so = item[1]['so']
                for prior_id in prior_so_ids:
                    ddt_lines[prior_id]['so'] = last_so
                prior_so_ids = []
            else:
                prior_so_ids.append(item[0])
        for prior_id in prior_so_ids:
            ddt_lines[prior_id]['so'] = last_so
        sorted_lines = {}
        for item in ddt_lines.items():
            hash = '%16.16s|%6d|%6d|%6d' % (
                item[1]['so'] or '',
                item[1]['sequence'],
                item[1]['so_line'],
                item[0],
            )
            sorted_lines[hash] = item[1]['line']
        sequence = 0
        for item in sorted(sorted_lines.keys()):
            sequence += 10
            line = sorted_lines[item]
            line.write({'sequence': sequence})

    @api.model
    def add_ddt_line(self, ddt_lines, line):
        if line.id not in ddt_lines:
            ddt_lines[line.id] = {}
        ddt_lines[line.id]['line'] = line
        ddt_lines[line.id]['sequence'] = line.sequence
        ddt_lines[line.id]['so'] = False
        ddt_lines[line.id]['so_line'] = False
        # TODO: tis works just with 1 sale order line
        if line.sale_line_id:
            ddt_lines[line.id]['so'] = line.sale_line_id.order_id.name
            ddt_lines[line.id]['so_line'] = line.sale_line_id.id
        return ddt_lines

    @api.multi
    def action_renumber_ddt_lines(self):
        for ddt in self:
            ddt_lines = {}
            for line in ddt.line_ids:
                ddt_lines = self.add_ddt_line(ddt_lines, line)
            self.do_renum(ddt_lines)
        return True
