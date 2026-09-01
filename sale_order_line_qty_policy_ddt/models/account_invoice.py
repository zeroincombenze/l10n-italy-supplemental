# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def unlink(self):
        """Give back to be invoiced the DdT lines this invoice was holding.

        The lines of an invoice are dropped by the database, because
        account.invoice.line.invoice_id cascades, so unlink() of the line is
        never called: the delivery note lines have to be collected here,
        while the invoice still exists.
        """
        ddt_lines = self.env["stock.picking.package.preparation.line"].search(
            [("invoice_line_id.invoice_id", "in", self.ids)])
        res = super(AccountInvoice, self).unlink()
        ddt_lines._resync_invoiced()
        return res


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    def unlink(self):
        """Give back to be invoiced the DdT lines these lines were holding."""
        ddt_lines = self.env["stock.picking.package.preparation.line"].search(
            [("invoice_line_id", "in", self.ids)])
        res = super(AccountInvoiceLine, self).unlink()
        ddt_lines._resync_invoiced()
        return res
