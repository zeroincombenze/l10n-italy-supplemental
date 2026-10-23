# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from odoo import api, models
from odoo.tools.float_utils import float_is_zero


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
    def _is_free_line(self, ddt_line):
        """Return True when nothing was to be billed for this line.

        Only a product whose policy is "Only if 0" is looked at: a price of
        0 does not always mean a free line - the amount of a product such as
        CONAI is evaluated again at invoice level - so the product has to
        declare it.

        Both prices are read: the delivery note one is what was agreed, the
        invoice one is what the user saw when dropping the line. When either
        carries an amount, dropping the line drops a charge, which still has
        to be billed.
        """
        self.ensure_one()
        if ddt_line.product_id.auto_line_invoiced != "only0":
            return False
        precision = self.env["decimal.precision"].precision_get(
            "Product Price")
        return (float_is_zero(self.price_unit, precision_digits=precision)
                and float_is_zero(ddt_line.price_unit,
                                  precision_digits=precision))

    @api.multi
    def unlink(self):
        """Give back to be invoiced the DdT lines these lines were holding.

        A free line of a product whose policy is "Only if 0", i.e. the
        carriage charge of a free delivery, is the exception: the user drops
        it from the invoice because there is nothing to bill, so giving it
        back to be invoiced would leave its delivery note and its sale order
        open for ever. That line is declared invoiced instead, as the user
        would do by hand.
        """
        ddt_line_model = self.env["stock.picking.package.preparation.line"]
        ddt_lines = ddt_line_model.search([("invoice_line_id", "in", self.ids)])
        free_lines = ddt_line_model
        for ddt_line in ddt_lines:
            if ddt_line.invoice_line_id._is_free_line(ddt_line):
                free_lines |= ddt_line
        res = super(AccountInvoiceLine, self).unlink()
        ddt_lines._resync_invoiced()
        free_lines.action_declare_invoiced()
        return res
