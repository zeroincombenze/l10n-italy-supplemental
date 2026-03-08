#
# Copyright 2020-26 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#

from odoo import models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def check_rc(self):
        value = ''
        if self.kind_id:
            if self.kind_id.code.startswith('N3'):
                if self.kind_id.code != 'N3.5':
                    value = 'local'
            elif self.kind_id.code.startswith('N6'):
                value = 'self'

        return value
