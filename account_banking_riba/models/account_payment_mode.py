# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#

from odoo import models, fields, api
from .common import sia_code_valid
from odoo.exceptions import ValidationError


class AccountPaymentMode(models.Model):
    _inherit = "account.payment.mode"

    sia_code = fields.Char(
        string="Codice SIA",
        size=5,
        help="Inserire il codice SIA attribuito all'azienda. Il codice SIA "
        "è composta da una lettera seguita da un numero di 4 cifre.",
    )

    @api.multi
    @api.constrains("sia_code")
    def _check_sia_code(self):
        for pay_mode in self:
            if pay_mode.sia_code and not sia_code_valid(pay_mode.sia_code):
                raise ValidationError(
                    f'Il codice SIA "{pay_mode.sia_code}"' f" non è valido."
                )
            # end if
        # end for

    # end _check_sia_code
