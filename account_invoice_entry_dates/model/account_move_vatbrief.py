# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import models, fields, api
# from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp


class VATBrief(models.Model):
    _name = 'account.move.vatbrief'
    _description = 'Prima nota - Somma movimenti contabili fattura raggruppati per contro e date di competenza'

    # TODO: definire ordinamento
    # _order = 'due_date'

    move_id = fields.Many2one(
        comodel_name='account.move',
        domain=[('journal_id.type', 'in', ['sale', 'sale_refund', 'purchase', 'purchase_refund'])],
        string='Registrazione contabile',
        requred=True
    )

    tax_id = fields.Many2one(
        comodel_name='account.tax',
        string='Tassa',
        requred=True
    )

    # Tax base amount
    base_amount_total = fields.Float(
        string='Imponibile',
        digits=dp.get_precision('Account'),
        required=True
    )

    # Tax amount
    vat_total = fields.Float(
        string='Imposta',
        digits=dp.get_precision('Account'),
        required=True
    )

    vat_det = fields.Float(
        string='Imposta detraibile',
        digits=dp.get_precision('Account'),
        required=True
    )

    vat_no_det = fields.Float(
        string='Imposta non detraibile',
        digits=dp.get_precision('Account'),
        compute='_compute_vat_no_det'
    )

    vat_code_rel = fields.Char(
        string='Codice IVA',
        related='tax_id.description'
    )

    display_name_rel = fields.Char(
        string='Descrizione codice IVA',
        related='tax_id.display_name'
    )

    @api.multi
    def _compute_vat_no_det(self):
        for line in self:
            line.vat_no_det = line.vat_total - line.vat_det
        # end for
    # end _compute_vat_no_det

# end VATBrief
