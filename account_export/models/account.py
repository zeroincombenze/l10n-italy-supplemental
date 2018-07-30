# -*- coding: utf-8 -*-
# Copyright 2018 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
import logging
from datetime import date

import odoo.release as release
from odoo import models, fields, api


class AccountMoveExport(models.Model):

    _name = "account.move.export"

    name = fields.Char('Name')
    company_id = fields.Many2one('res.company', 'Company')
    state = fields.Selection([('draft', 'Draft'),
                              ('open', 'Open'),
                              ('confirmed', 'Confirmed'),],
                             'State', readonly=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    move_export_customer_ids = fields.One2many(
        'account.move.export.customer', 'move_export_id',
        'Sale invoices',
        help='Sale invoices to export',
        states={'draft': [('readonly', False)],
                'open': [('readonly', False)],
                'confirmed': [('readonly', True)]})
    move_export_supplier_ids = fields.One2many(
        'account.move.export.supplier', 'move_export_id',
        'Purchase invoices',
        help='Purchase invoices to export',
        states={'draft': [('readonly', False)],
                'open': [('readonly', False)],
                'confirmed': [('readonly', True)]})


class AccountMoveExportLine(models.AbstractModel):
    _name = 'account.move.export.line'


class AccountMoveExportLineCustomer(models.Model):
    _name = 'account.move.export.customer'
    _inherit = 'account.move.export.line'

    move_export_id = fields.Many2one(
        'account.move.export', 'Account Export ID')
    invoice_id = fields.Many2one(
        'account.invoice', 'Invoice')


class AccountMoveExportLineSupplier(models.Model):
    _name = 'account.move.export.supplier'
    _inherit = 'account.move.export.line'

    move_export_id = fields.Many2one(
        'account.move.export', 'Account Export ID')
    invoice_id = fields.Many2one(
        'account.invoice', 'Invoice')
