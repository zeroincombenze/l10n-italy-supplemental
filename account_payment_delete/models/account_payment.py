from odoo import api, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def unlink(self):
        if self.journal_id.update_posted:
            for rec in self:
                rec.move_name = ''
        return super(AccountPayment, self).unlink()
