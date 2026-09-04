# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
"""Create qty_ddt_declared before Odoo would compute it over every order.

A pre-migration is the only moment of an upgrade which comes before
_auto_init, and _auto_init is what mass-computes a stored field on the whole
table when it creates its column. See create_qty_ddt_declared_column() in
``hooks.py`` for why that pass must not happen here.
"""
from odoo.addons.sale_order_line_qty_policy_ddt.hooks import (
    create_qty_ddt_declared_column)


def migrate(cr, version):
    if not version:
        # Fresh install: pre_init_hook does it, this is never reached
        return
    create_qty_ddt_declared_column(cr)
