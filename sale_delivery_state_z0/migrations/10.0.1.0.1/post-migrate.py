# -*- coding: utf-8 -*-
#
# Copyright 2024 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        SaleOrder = env["sale.order"]
        for order in SaleOrder.search([]):
            order._compute_delivery_state()
