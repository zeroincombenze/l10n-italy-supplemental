# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
"""Settle the existing free lines of "Only if 0" products.

From 10.0.0.1.8 such a line is invoiced at once, but an upgrade recomputes
no stored field whose column exists: qty_to_invoice and invoice_status are
recomputed here, on the lines picked in SQL, one batch at a time.
"""
import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

CHUNK_SIZE = 500
FIELDS = ("qty_to_invoice", "invoice_status")


def migrate(cr, version):
    if not version:
        return
    cr.execute("""
        SELECT sol.id
          FROM sale_order_line sol
          JOIN product_product pp ON pp.id = sol.product_id
          JOIN product_template pt ON pt.id = pp.product_tmpl_id
         WHERE pt.auto_line_invoiced = 'only0'
           AND COALESCE(sol.price_unit, 0) = 0
           AND sol.state IN ('sale', 'done')
           AND (sol.invoice_status IS DISTINCT FROM 'invoiced'
                OR COALESCE(sol.qty_to_invoice, 0) <> 0)
         ORDER BY sol.id""")
    ids = [row[0] for row in cr.fetchall()]
    env = api.Environment(cr, SUPERUSER_ID, {})
    model = env["sale.order.line"]
    fields_to_do = [model._fields[name] for name in FIELDS]
    for start in range(0, len(ids), CHUNK_SIZE):
        lines = model.browse(ids[start:start + CHUNK_SIZE]).exists()
        for field in fields_to_do:
            lines._recompute_todo(field)
        lines.recompute()
        env.invalidate_all()
        cr.commit()
    _logger.info("sale_order_line_qty_policy: settled %s free lines of"
                 " \"Only if 0\" products", len(ids))
