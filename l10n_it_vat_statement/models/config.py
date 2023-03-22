# Copyright 2015 Alessandro Camilli <a.camilli@openforce.it>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    of_account_end_vat_statement_interest = fields.Boolean(
        'Interest on End Vat Statement',
        help="Apply interest on end vat statement")
    of_account_end_vat_statement_interest_percent = fields.Float(
        'Interest on End Vat Statement - %',
        help="Apply interest on end vat statement")
    of_account_end_vat_statement_interest_account_id = fields.Many2one(
        'account.account', 'Interest on End Vat Statement - Account',
        help="Apply interest on end vat statement")
