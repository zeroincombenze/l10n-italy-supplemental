# -*- coding: utf-8 -*-
#
# Copyright 2018-24 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import fields, models, api


class ItalyAdeInvoiceType(models.Model):
    _name = "italy.ade.invoice.type"
    _description = "Fiscal document type"
    _order = "code, priority asc"

    _sql_constraints = [("code", "unique(code)", "Code already exists!")]

    code = fields.Char(
        string="Code", size=5, required=True, help="Code assigned by Tax Authority"
    )
    name = fields.Char(string="Name", size=100, required=True)
    help = fields.Text(string="Help")
    out_invoice = fields.Boolean(string="Customer Invoice")
    in_invoice = fields.Boolean(string="Vendor Bill")
    out_refund = fields.Boolean(string="Customer Credit Note")
    in_refund = fields.Boolean(string="Vendor Credit Note")
    priority = fields.Integer(string="Priority", default="3")
    scope = fields.Char(string="Scope", help="Reserved to specific scope")
    active = fields.Boolean(string="Active", default=True)
    is_self_invoice = fields.Boolean(string="It is self invoice")

    @api.multi
    def name_get(self):
        res = []
        for doc_type in self:
            res.append(
                (doc_type.id, '[%s] %s' % (doc_type.code, doc_type.name)))
        return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            records = self.search([
                '|', ('name', operator, name), ('code', operator, name)
                ] + args, limit=limit)
        else:
            records = self.search(args, limit=limit)
        return records.name_get()
