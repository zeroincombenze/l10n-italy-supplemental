# Copyright 2019-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    group_inv_lines_mode = fields.Selection([
        ('same', 'Move lines with same invoice lines'),
        ('group', 'Group by product'),
        ('account', 'Group by account/tax')
        ],
        defaulr = 'same',
        help="The system will try to group the accounting lines\n"
             "when generating them from invoices.\n"
             "'Group by product' works as Odoo 'Group Invoice Lines'\n"
             "'Group by account/tax' writes the minimal # of account lines."
    )

    @api.model
    def create(self, vals):
        if 'group_inv_lines_mode' in vals:
            if vals['group_inv_lines_mode'] == 'group':
                vals['group_invoice_lines'] = True
            else:
                vals['group_invoice_lines'] = False
        return super().create(vals)

    @api.multi
    def write(self, vals):
        if 'group_inv_lines_mode' in vals:
            if vals['group_inv_lines_mode'] == 'group':
                vals['group_invoice_lines'] = True
            else:
                vals['group_invoice_lines'] = False
        return super().write(vals)
