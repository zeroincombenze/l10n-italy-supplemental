# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import models, api


class StockPickingPackagePreparation(models.Model):

    _inherit = 'stock.picking.package.preparation'

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        res = super()._prepare_invoice()
        # shipping address
        if self.partner_shipping_id and self.partner_shipping_id.id:
            country = self.partner_shipping_id.country_id
            if country.code != 'IT':
                res.update({
                    'intrastat': True
                })
            # end if
        # end if
        return res
