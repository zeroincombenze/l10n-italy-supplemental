# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
"""Apply the policy to the delivery notes an upgrade leaves behind.

10.0.0.1.1 overrode _compute_to_be_invoiced, but an upgrade recomputes no
stored field whose column already exists, so the override never reached the
documents already in the database. The work, and the reason it is split
between SQL and the ORM, is in ``hooks.py``: the first installation needs
the very same repair, through post_init_hook, and the two paths never
overlap.
"""
from odoo import api, SUPERUSER_ID

from odoo.addons.sale_order_line_qty_policy_ddt.hooks import (
    sync_policy_fields)


def migrate(cr, version):
    if not version:
        # Fresh install: post_init_hook does it, this is never reached
        return
    sync_policy_fields(api.Environment(cr, SUPERUSER_ID, {}))
