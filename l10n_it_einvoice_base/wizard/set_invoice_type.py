# -*- coding: utf-8 -*-
#
# Copyright 2018-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import api, models


class WizardSetInvoiceType(models.TransientModel):
    _name = "wizard.set.invoice.type"

    @api.multi
    def set_einvoice_type(self):
        self.ensure_one()
        invoices = self.env[self.env.context["active_model"]].browse(
            self.env.context["active_ids"]
        )
        return invoices.set_einvoice_type()
