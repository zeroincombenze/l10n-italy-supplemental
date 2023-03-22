# Copyright 2021-22 librERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
from odoo import models, fields


class AssetGenerateWarning(models.TransientModel):
    _name = "asset.generate.warning"
    _description = "Warning before generate depreciations"

    wizard_id = fields.Many2one(
        "wizard.asset.generate.depreciation", string="Asset Wizard"
    )
    reason_lines = fields.One2many(
        comodel_name="asset.confirm.reason.line",
        inverse_name="confirm_id",
        string="Elenco",
    )

    def do_generate(self):
        return self.wizard_id.do_generate()


class AssetConfirmReasonLine(models.TransientModel):
    _name = "asset.confirm.reason.line"
    _description = "Confirmation before generate depreciations"

    confirm_id = fields.Many2one("asset.generate.warning", string="Numero elenco")
    reason = fields.Char(string="Avviso", size=255, readonly=True)
