# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging

from odoo.exceptions import UserError

from odoo import api, models

from .mixins import OrderMixin

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model, OrderMixin):
    _inherit = 'sale.order'

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """
        Override action_invoice_create checking for payment
        terms consistency before creating the invoice.
        """

        payment_terms = {
            sale_order.payment_term_id
            for sale_order in self
        }

        if len(payment_terms) > 1:
            raise UserError(
                'Impossibile create un\'unica fattura da ordini'
                ' di vendita con Termini di Pagamento diversi.'
            )
        # end if

        return super().action_invoice_create(grouped, final)
    # end action_invoice_create

    @api.multi
    def adapt_document(self):
        self.ensure_one()
        adapt_data = {
            'model': 'sale.order',
            'type': 'sale_order',
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

        if self.partner_id and self.partner_id.assigned_bank:
            adapt_data['assigned_bank'] = self.partner_id.assigned_bank
        # end if

        if self.partner_id and self.partner_id.assigned_income_bank:
            adapt_data[
                'assigned_income_bank'] = self.partner_id.assigned_income_bank
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

        if self.partner_id and self.partner_id.bank_ids:
            pbk = self.partner_id
            bank = self.env['res.partner.bank']
            # python 3.7
            if pbk.bank_ids:
                for bk in pbk.bank_ids:
                    bank = bk
                    break
                # end for
            # end if
            adapt_data['default_counterparty_bank'] = bank
        # end if

        return adapt_data

    # end adapt_document

    @api.multi
    def _prepare_invoice(self):

        # Call superclass method implementation
        invoice_vals = super()._prepare_invoice()

        # Set bank accounts related infos
        invoice_vals['bank_2_print_selector'] = self.bank_2_print_selector
        invoice_vals['company_bank_id'] = self.company_bank_id and self.company_bank_id.id
        invoice_vals['counterparty_bank_id'] = self.counterparty_bank_id and self.counterparty_bank_id.id

        if self.company_bank_id:
            invoice_vals['partner_bank_id'] = self.company_bank_id.id
        # end if

        # Return the description of the invoice to be created
        return invoice_vals

    # end _prepare_invoice

    @api.multi
    def _get_doc_type(self):
        self.ensure_one()
        return ''
    # end _get_doc_type

# end SaleOrder
