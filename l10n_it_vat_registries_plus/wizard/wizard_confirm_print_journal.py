# Copyright (c) 2021
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import models, fields


class WizardConfirmPrintJournal(models.TransientModel):
    _name = "wizard.confirm.print.journal"

    wizard_id = fields.Many2one('wizard.registro.iva', string="Stampa")
    reason_lines = fields.One2many(
        comodel_name="wizard.confirm.reason.line",
        inverse_name="confirm_id",
        string="Elenco")

    def conferma_anomalie(self):
        return self.wizard_id.print_registro_super()


class WizardConfirmReasonLine(models.TransientModel):
    _name = "wizard.confirm.reason.line"

    confirm_id = fields.Many2one('wizard.confirm.print.journal',
                                 string="Numero elenco")
    number = fields.Char(string="Numero documento", size=64, readonly=True)
    date_document = fields.Char(string="Data documento", size=64, readonly=True)
    reason = fields.Char(string="Motivo", size=64, readonly=True)
