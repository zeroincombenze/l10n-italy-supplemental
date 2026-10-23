# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
"""Close the delivery notes their sale order already billed.

From 10.0.0.1.5 a delivery note line is invoiced when its order line
already invoiced everything it shipped, i.e. an order invoiced before the
delivery; an upgrade recomputes no stored field: the batched resync of
``hooks.py`` does it.
"""
from odoo import api, SUPERUSER_ID

from odoo.addons.sale_order_line_qty_policy_ddt.hooks import (
    sync_policy_fields)


def migrate(cr, version):
    if not version:
        return
    sync_policy_fields(api.Environment(cr, SUPERUSER_ID, {}))
