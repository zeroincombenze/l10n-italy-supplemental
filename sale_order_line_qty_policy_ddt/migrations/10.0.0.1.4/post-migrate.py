# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
"""Settle the existing free lines of "Only if 0" products.

From 10.0.0.1.4 such a line is invoiced at once, but an upgrade recomputes
no stored field: the batched resync of ``hooks.py`` does it.
"""
from odoo import api, SUPERUSER_ID

from odoo.addons.sale_order_line_qty_policy_ddt.hooks import (
    sync_policy_fields)


def migrate(cr, version):
    if not version:
        return
    sync_policy_fields(api.Environment(cr, SUPERUSER_ID, {}))
