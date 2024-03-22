# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later
# (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps)
#
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class WizardConfirmDepreciation(models.TransientModel):
    _name = "wizard.confirm.depreciation"

    wizard_id = fields.Many2one('wizard.generate.balance', string="Bilancio")
    message = fields.Text(
        string='Anomalie'
    )

    def conferma_anomalie(self):
        return self.wizard_id.do_generate()
    # end conferma_anomalie

