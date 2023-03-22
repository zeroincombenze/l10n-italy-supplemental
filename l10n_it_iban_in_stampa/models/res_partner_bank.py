# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import api, fields, models


_logger = logging.getLogger(__name__)


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    is_company_bank = fields.Boolean(
        comodel_name='res.users',
        compute='_compute_is_company_bank'
    )

    part_of_default_banks_2_print = fields.Boolean(
        string='Fa parte delle banche di default',
        help='Il conto bancario fa parte di quelli inseriti nella stampa di fatture e '
             'ordini nel caso in cui il campo "Tipo di IBAN" sia impostato ad '
             '"Azienda", ma non sia indicata la banca da utilizzare '
             '(campo "Bancaziendale" vuoto)'
    )

    @api.multi
    def _compute_is_company_bank(self):
        for bnk in self:
            is_cmp_bnk = self.env.user.company_id.partner_id.id == self.partner_id.id
            bnk.is_company_bank = is_cmp_bnk
        # end for
    # end _compute_is_company_bank

# end ResPartnerBank
