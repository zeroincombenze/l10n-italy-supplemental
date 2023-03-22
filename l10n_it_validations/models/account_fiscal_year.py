# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import api, fields, models


class AccountFiscalYear(models.Model):
    _inherit = "account.fiscal.year"

    date_range_id = fields.Many2one("date.range", string="Date range")

    @api.onchange("state")
    def _onchange_state_closed(self):
        fy_moded = self.env["account.move"].search(
            [("fiscalyear_id", "=", self.id)]
        ) or self.env["account.move"].search([("fiscalyear_id", "=", self.id)])
        if self.state == "done":
            if not fy_moded:
                warning_mess = {
                    "title": "Operazione irreversibile!",
                    "message": "Attenzione! " "Confermando si blocca l'esercizio",
                }
                return {"warning": warning_mess}
            self.state = "draft"
            warning_mess = {
                "title": "Periodo contabile!",
                "message": "Periodo movimentato",
            }
            return {"warning": warning_mess}
        return
