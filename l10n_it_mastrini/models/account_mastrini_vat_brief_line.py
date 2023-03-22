# Copyright 2021-2022 LibrERP enterprise network <https://www.librerp.it>
#
# License OPL-1 or later
#   https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps)
#
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class VATBriefLine(models.TransientModel):
    _name = "account.mastrini.vat.brief.line"

    fiscal_year = fields.Many2one(
        comodel_name="account.fiscal.year",
        string="Esercizio",
    )

    line_type = fields.Selection(
        selection=[
            # Acquisti
            ("in_invoice", "Fattura acquisto"),
            ("in_refund", "Nota di Credito Fornitore"),
            # Vendite
            ("out_invoice", "Fattura vendita"),
            ("out_refund", "Nota di Credito Cliente"),
            # Totale
            ("totals", "Totali"),
            # Spaces
            ("spacer", ""),
        ],
        readonly=True,
        string="Tipo",
    )

    is_spacer = fields.Boolean(compute="_compute_is_spacer")

    description = fields.Text(string="Descrizione", readonly=True)

    base_amount = fields.Float(
        "Imponibile", digits=dp.get_precision("Account"), readonly=True
    )

    tax_amount = fields.Float(
        "Imposta", digits=dp.get_precision("Account"), readonly=True
    )

    total_amount = fields.Float(
        "Totale", digits=dp.get_precision("Account"), readonly=True
    )

    sign = fields.Selection(
        selection=[
            (1, "+"),
            (-1, "-"),
        ],
        string="Segno",
    )

    wizard_id = fields.Many2one(comodel_name="account.mastrini.wizardmodel")

    @api.multi
    @api.depends("line_type")
    def _compute_is_spacer(self):
        for line in self:
            line.is_spacer = line.line_type == "spacer"
        # end for

    # end _compute_is_spacer


# end VATBriefLine
