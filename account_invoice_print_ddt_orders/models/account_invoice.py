# Copyright 2019-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def get_sale_order_references(self):
        references = list()
        if self.type in ('in_refund', 'in_invoice'):
            return references
        for line in self.invoice_line_ids:
            if line.sale_line_ids:
                for sale in line.sale_line_ids:
                    order_ref = sale.order_id.display_name
                    if order_ref not in references:
                        references.append(order_ref)
                    # end if
                # end for
            # end if
        # end for
        return references

