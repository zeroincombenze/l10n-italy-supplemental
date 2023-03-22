# -*- coding: utf-8 -*-
# © 2019-2020 Andrei Levin - Didotech srl (www.didotech.com)

from odoo import models, fields


class FatturapaAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment.in"

    sdi_id = fields.Char('IdSdi', readonly=True)
    sdi_date = fields.Datetime('DataSdi', readonly=True)
