# Copyright 2019-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License LGPL-3 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
#
import logging
from odoo import models, fields, api
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class ResCompany(models.Model):
    _inherit = 'res.company'
    account_profile_id = fields.Many2one(
        'italy.profile.account',
        string='Account Profile',
        help='Select the account profile with account configuration values.')


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    account_profile_id = fields.Many2one(
        related='company_id.account_profile_id',
        string='Account Profile',
        help='Select the account profile with account configuration values.',
        readonly=False,
    )

    @api.onchange('account_profile_id')
    def onchange_account_profile_id(self):
        self.ensure_one()
        if not self.account_profile_id.id and \
                self.company_id.account_profile_id.id:
            raise Warning('Attenzione! '
                          'Profilo contabile impostato e non modificabile.\n')

        if self.account_profile_id.id \
                and self.company_id.account_profile_id.id \
                and (self.account_profile_id.id !=
                     self.company_id.account_profile_id.id):

            accounts = self.env['account.account']. \
                search([('company_id', '=', self.company_id.id)])
            _logger.info('account.account len: %s' % len(accounts))
            if len(accounts) > 0:
                raise Warning('Attenzione! '
                              'Profilo contabile non modificabile.\n')
