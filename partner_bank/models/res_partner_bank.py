# -*- coding: utf-8 -*-
#
# Copyright 2018-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import api, fields, models


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    active = fields.Boolean(default=True)
    acc_type = fields.Selection([
        ('bank', 'Bank'),
        ('iban', 'Iban'),
        ('normal', 'Normal')],
        string='Bank Account Type')

    @api.multi
    @api.depends('bank_id', 'acc_number')
    def name_get(self):
        result = []
        for bank in self:
            if bank.bank_id.name:
                name = '%s *%s ' % (bank.bank_id.name, bank.acc_number[-4:])
            else:
                name = bank.acc_number
            result.append((bank.id, name))
        return result

