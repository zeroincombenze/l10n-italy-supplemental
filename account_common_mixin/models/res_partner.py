#
# Copyright 2020-24 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-24 Didotech s.r.l. <https://www.didotech.com>
#
import logging
from odoo import api, models


_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def bank_infos(self):

        bank_infos = {
            "assigned_bank": None,
            "assigned_income_bank": None,
            "default_counterparty_bank": None,
        }

        if not self:
            return bank_infos

        self.ensure_one()

        real_partner = self.commercial_partner_id

        if real_partner.id:

            if real_partner.assigned_bank:
                bank_infos["assigned_bank"] = real_partner.assigned_bank

            if real_partner.assigned_income_bank:
                bank_infos["assigned_income_bank"] = real_partner.assigned_income_bank

            if real_partner.bank_ids:
                bank_infos["default_counterparty_bank"] = real_partner.bank_ids[0]

        return bank_infos
