# -*- coding: utf-8 -*-
# © 2020 Andrei Levin - Didotech srl (www.didotech.com)

from odoo import models, fields
from odoo.addons.l10n_it_efattura_sdi.models.attachment import e_invoice_state  # pylint: disable=W7950



class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sdi_state = fields.Selection(
        related='fatturapa_attachment_out_id.sdi_state',
        string='Stato invio', selection=e_invoice_state, readonly=True)
    sdi_id = fields.Char(
        related='fatturapa_attachment_in_id.sdi_id',  string='Id SDI')
    sdi_date = fields.Datetime(
        related='fatturapa_attachment_in_id.sdi_date', string='Data SDI')
