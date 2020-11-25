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


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def do_renum(self, inv_lines):
        prior_so_ids = []
        prior_ddt_ids = []
        last_so = False
        last_ddt = False
        for item in inv_lines.items():
            if item[1]['so']:
                last_so = item[1]['so']
                for prior_id in prior_so_ids:
                    inv_lines[prior_id]['so'] = last_so
                prior_so_ids = []
            else:
                prior_so_ids.append(item[0])
            if item[1]['ddt']:
                last_ddt = item[1]['ddt']
                for prior_id in prior_ddt_ids:
                    inv_lines[prior_id]['ddt'] = last_ddt
                prior_ddt_ids = []
            else:
                prior_ddt_ids.append(item[0])
        for prior_id in prior_so_ids:
            inv_lines[prior_id]['so'] = last_so
        for prior_id in prior_ddt_ids:
            inv_lines[prior_id]['ddt'] = last_ddt
        sorted_lines = {}
        for item in inv_lines.items():
            if item[1]['line'].name.startswith('Contributo ambientale'):
                hash = '%16.16s|%16.16s|%6d|%6d|%6d|%6d' % (
                    '~~~~~~',
                    '',
                    item[1]['sequence'],
                    0,
                    0,
                    item[0],
                )
            else:
                hash = '%16.16s|%16.16s|%6d|%6d|%6d|%6d' % (
                    item[1]['so'] or '',
                    item[1]['ddt'] or '',
                    item[1]['sequence'],
                    item[1]['ddt_line'],
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
    def add_inv_line(self, inv_lines, line):
        if line.id not in inv_lines:
            inv_lines[line.id] = {}
        inv_lines[line.id]['line'] = line
        inv_lines[line.id]['sequence'] = line.sequence
        inv_lines[line.id]['so'] = False
        inv_lines[line.id]['so_line'] = False
        # TODO: tis works just with 1 sale order line
        for sale_line_id in line.sale_line_ids:
            inv_lines[line.id]['so'] = sale_line_id.order_id.name
            inv_lines[line.id]['so_line'] = sale_line_id.id
        inv_lines[line.id]['ddt'] = False
        inv_lines[line.id]['ddt_line'] = False
        if line.ddt_line_id:
            inv_lines[line.id][
                'ddt'] = line.ddt_line_id.package_preparation_id.ddt_number
            inv_lines[line.id]['ddt_line'] = line.ddt_line_id.id
        return inv_lines

    @api.multi
    def action_renumber_invoice_lines(self):
        for invoice in self:
            inv_lines = {}
            for line in invoice.invoice_line_ids:
                inv_lines = self.add_inv_line(inv_lines, line)
            self.do_renum(inv_lines)
        return True
