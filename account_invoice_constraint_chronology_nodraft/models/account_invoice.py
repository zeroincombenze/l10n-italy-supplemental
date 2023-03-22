# Copyright (c) 2020
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

import datetime

from odoo import models, api, fields, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def _prepare_later_invoices_domain(self, invoice):
        return [
            ('state', 'in', ['open', 'in_payment', 'paid']),
            ('date', '>', invoice.date),
            ('journal_id', '=', invoice.journal_id.id),
            ('fiscalyear_id', '=', invoice.fiscalyear_id.id),
        ]

    @api.multi
    def action_move_create(self):
        # collect invoice at least in open state (has move_name)
        # previously_validated = self.filtered(lambda inv: inv.move_name)
        res = super(AccountInvoice, self).action_move_create()
        for inv in self:
            # if flag in False go to next invoice
            if not inv.journal_id.check_chronology:
                continue
            if inv.move_name:
                continue
            # if inv is not at least open
            # search if exists for that journal
            # an invoice with date_invoice > the actual one
            # removed optimization so we can catch all invoice
            # if inv not in previously_validated:

            invoices = self.search(
                self._prepare_later_invoices_domain(inv), limit=1)
            # if any (the first one found)
            # raise UserError
            if invoices:
                date_format = datetime.datetime(
                    year=inv.date.year,
                    month=inv.date.month,
                    day=inv.date.day,
                )
                date_tz = format_date(
                    self.env, fields.Date.context_today(
                        self, date_format))
                raise UserError(_(
                    "Chronology Error. There exist at least one invoice "
                    "with a later date to {date}.").format(
                    date=date_tz))
        return res
