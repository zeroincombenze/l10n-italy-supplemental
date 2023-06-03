# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging

from odoo import models, api, fields


_logger = logging.getLogger(__name__)


class WizardInsoluto(models.TransientModel):
    _name = "wizard.account.banking.common.insoluto"
    _description = "Gestione insoluti"

    def _get_bank_expenses_account(self):
        return [
            "|",
            (
                "user_type_id",
                "=",
                self.env.ref("account.data_account_type_expenses").id,
            ),
            (
                "user_type_id",
                "=",
                self.env.ref("account.data_account_type_direct_costs").id,
            ),
        ]

    expenses_account = fields.Many2one(
        "account.account",
        string="Conto Spese",
        domain=_get_bank_expenses_account,
    )

    expenses_amount = fields.Float(string="Importo spese")

    charge_client = fields.Boolean(
        string="Addebito spese a cliente",
        default=False,
    )

    @api.multi
    def registra_insoluto(self):
        """Create on new account.move for each line of insoluto"""
        ids = self._context["active_ids"]
        model = self.env["account.move.line"]
        recordset = model.browse(ids)
        recordset.with_context(
            {
                "expenses_account_id": self.expenses_account.id,
                "expenses_amount": self.expenses_amount,
                "charge_client": self.charge_client,
                "active_ids": ids,
            }
        ).registra_insoluto()

    # end registra_insoluto
