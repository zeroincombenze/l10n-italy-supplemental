from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    espresso = fields.Boolean(
        string='Espresso',
        default=False,
        help="If flagged this product will be automatically insert into DDT "
             "from delivery note.")


class ProductProduct(models.Model):
    _inherit = "product.product"

    espresso = fields.Boolean(
        string='Espresso',
        related='product_tmpl_id.espresso',
    )
