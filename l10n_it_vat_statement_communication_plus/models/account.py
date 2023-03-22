# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2017-19 Lorenzo Battistini
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
# Copyright 2017-21 Odoo Community Association (OCA) <https://odoo-community.org>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    vsc_exclude_operation = fields.Boolean(
        string='Exclude from active / passive operations')

    vsc_exclude_vat = fields.Boolean(
        string='Exclude from VAT payable / deducted')
