from odoo import api, models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):

        # Call superclass method implementation
        invoice_vals = super()._create_invoice(order, so_line, amount)

        # Set bank accounts related infos
        invoice_vals['bank_2_print_selector'] = self.bank_2_print_selector
        invoice_vals['company_bank_id'] = self.company_bank_id and self.company_bank_id.id
        invoice_vals['counterparty_bank_id'] = self.counterparty_bank_id and self.counterparty_bank_id.id

        if self.company_bank_id:
            invoice_vals['partner_bank_id'] = self.company_bank_id.id
        # end if

        # Return the description of the invoice to be created
        return invoice_vals

    # end _create_invoice

# end SaleAdvancePaymentInv
