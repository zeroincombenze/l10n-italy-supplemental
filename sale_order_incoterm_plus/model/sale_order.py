# Copyright 2021-16 Powerp Enterprise Network
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super().onchange_partner_id()

        if self.partner_id and self.partner_id.sale_incoterm_id:
            self.incoterm = self.partner_id.sale_incoterm_id

        elif self.company_id.sale_incoterm_default:
            self.incoterm = self.company_id.sale_incoterm_default

        else:
            self.incoterm = False

        # end if

        return res
# end SaleOrder
