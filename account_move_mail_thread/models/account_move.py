# -*- coding: utf-8 -*-
# Copyright 2017 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
#                Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from osv import osv


class account_move(osv.Model):
    _name = "account.move"
    _inherit = ['account.move',
                'mail.thread',
                'ir.needaction_mixin']
