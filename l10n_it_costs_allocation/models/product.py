# Copyright (c) 2021
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cost_type = fields.Selection(
        selection=[
            ('delivery', 'Spese di spedizione'),
            ('packaging', 'Spese di imballo'),
            ('payment', 'Spese all\'incasso'),
            ('other', 'Spese di altra natura'),
            ('discount', 'Sconto globale'),
        ],
        string='Tipo di costo',
        default='')

    @api.onchange('cost_type')
    def on_change_cost_type(self):
        if self.cost_type:
            self.type = 'service'
        # end if
    # end on_change_cost_type


class ProductProduct(models.Model):
    _inherit = 'product.product'

    cost_type = fields.Selection(
        related='product_tmpl_id.cost_type',
        string='Tipo di costo')
