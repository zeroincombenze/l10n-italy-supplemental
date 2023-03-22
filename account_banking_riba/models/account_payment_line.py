# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#

from odoo import api, models


class AccountPaymentLine(models.Model):
    _inherit = 'account.payment.line'

    @api.multi
    def draft2open_payment_line_check(self):
        res = super().draft2open_payment_line_check()
        riba_lines = self.filtered(
            lambda l: l.order_id.payment_method_id.code == 'riba_cbi')
        riba_lines._check_riba_cbi_ready()
        return res

    @api.multi
    def _check_riba_cbi_ready(self):
        """
        This method checks whether the payment line(s) are ready to be used
        in the RiBa CBI file generation.
        :raise: UserError if a line does not fulfils all requirements
        """
        for _rec in self:
            # Al momento non è necessario effettuare nessun controllo in
            # questo contesto, sono sufficienti i controlli eseguiti
            # dalla libreria di generazione dei CBI
            pass
    # end _check_riba_cbi_ready
