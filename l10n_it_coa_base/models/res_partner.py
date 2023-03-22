# Copyright (c) 2020
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License LGPL-3 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
#
from odoo import models, api
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _set_default_account_payable(self):
        account = self.env['italy.profile.account']. \
            search([('id', '=',
                     self.env.user.company_id.account_profile_id.id)])
        if account:
            return account.default_account_payable.id
        else:
            raise UserError('Attenzione!\nConto di debito non impostato.')

    def _set_default_account_receivable(self):
        account = self.env['italy.profile.account']. \
            search([('id', '=',
                     self.env.user.company_id.account_profile_id.id)])
        if account:
            return account.default_account_receivable.id
        else:
            raise UserError('Attenzione!\nConto di credito non impostato.')

    @api.model
    def default_get(self, fields_list):
        res = super(ResPartner, self).default_get(fields_list)
        res['property_account_payable_id'] = \
            self._set_default_account_payable()
        res['property_account_receivable_id'] = \
            self._set_default_account_receivable()
        return res
