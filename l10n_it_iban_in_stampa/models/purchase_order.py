# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import api, models

from .mixins import OrderMixin


_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model, OrderMixin):
    _inherit = 'purchase.order'

    @api.multi
    def adapt_document(self):
        self.ensure_one()
        adapt_data = {
            'model': 'purchase.order',
            'type':  'purchase_order',
            'fatturapa_pm_id': None,
            'payment_mode_id': None,
            'assigned_bank': None,
            'assigned_income_bank': None,
            'default_company_bank': None,
            'default_counterparty_bank': None
        }

        if self.payment_term_id and self.payment_term_id.fatturapa_pm_id:
            adapt_data['fatturapa_pm_id'] = self.payment_term_id.fatturapa_pm_id
        # end if

        if self.payment_mode_id:
            adapt_data['payment_mode_id'] = self.payment_mode_id
        # end if

        if self.company_id and self.company_id.partner_id:
            pbk = self.company_id.partner_id
            bank = self.env['res.partner.bank']
            # python 3.7
            if pbk.bank_ids:
                for bk in pbk.bank_ids:
                    bank = bk
                    break
                # end for
            # end if
            adapt_data['default_company_bank'] = bank
        # end if

        # Update with counterparty data
        counterparty_bank_infos = self.partner_id.bank_infos()
        adapt_data.update(counterparty_bank_infos)

        return adapt_data
    # end adapt_document

    @api.multi
    def _get_doc_type(self):
        self.ensure_one()
        return ''
    # end _get_doc_type

# end PurchaseOrder
