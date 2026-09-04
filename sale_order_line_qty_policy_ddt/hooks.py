# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
"""Bring the stored fields of the policy up to date on existing documents.

This module owns three stored fields - line_invoiced on the delivery note
line, invoice_status on the delivery note, and the computation of
to_be_invoiced, whose column belongs to l10n_it_ddt - and **none of them is
guaranteed to be computed on the documents already in the database**. Odoo
recomputes a stored field only when it *creates* its column (``models.py``,
_auto_init: the field is appended to ``stored_fields`` in the "the column
doesn't exist in database" branch alone, and init_models then recomputes
that list only). Three situations follow, and only the first repairs itself:

* **installation on a database whose columns do not exist yet** - Odoo
  creates them, computes line_invoiced and invoice_status, and the
  ``modified()`` cascade started by writing line_invoiced recomputes
  to_be_invoiced as well. Nothing is left to do, and this hook confirms it;
* **installation on a database which still carries the columns** - a module
  uninstalled without dropping them, or a database prepared by flipping its
  state. ``stored_fields`` is empty, so **nothing at all** is computed:
  every delivery note written meanwhile keeps line_invoiced false and
  invoice_status null, and the policy is simply not applied to its history;
* **upgrade** - the columns are all there, so again nothing is recomputed.
  This is how 10.0.0.1.1 left 5738 delivery notes out of 6881 on
  ``litoservice`` with to_be_invoiced still raised: the override of
  _compute_to_be_invoiced never reached them, and the trigger on
  line_ids.line_invoiced only fires when a line is written again, which on a
  closed delivery note never happens.

The work is therefore done here, once, and Odoo keeps the two ways in which
it is reached strictly apart: ``post_init_hook`` runs only on installation
(``loading.py``: ``if new_install``), while migration scripts are skipped
altogether while the state is ``to install`` (``migration.py``: ``if ...
state == 'to install': return``). Neither can run twice, neither can stand
in for the other, and everything below is idempotent in any case.

**How each field is recomputed, and why not all the same way.**

line_invoiced goes through the ORM. Its verdict reaches into
``sale_line_id._is_line_invoiced()``, which is sale_order_line_qty_policy's
own policy - the declaration on the order, the product flag, the delivered
threshold - so restating it in SQL would copy that module's rules here and
let the copy drift. It is read in batches instead, each one dropped from the
cache before the next: searching a whole production table and iterating it
prefetches everything into the ORM cache and dies against
limit_memory_hard, which is how an earlier backfill took an upgrade down.
Only the lines whose verdict actually changed are written.

invoice_status and to_be_invoiced are done in SQL, because by then
line_invoiced is correct and the rest of both computations is readable from
the tables. Their expressions below were checked against
``_get_invoice_status()`` and ``_compute_to_be_invoiced()`` on the whole of
``litoservice`` - 6881 delivery notes, every edge shape included - with no
disagreement.

No chunk is committed: installation and upgrade stay atomic, so a failure
further on rolls this back with everything else.
"""
import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

CHUNK_SIZE = 500

DDT_TABLE = "stock_picking_package_preparation"
LINE_TABLE = "stock_picking_package_preparation_line"

# _get_invoice_status(), as the tables tell it. _is_invoiceable() reads the
# reason for transportation - not the flag which mirrors it - and it gates
# the whole thing before the lines are looked at: that order is what keeps a
# delivery note "not to be invoiced" from ever reporting itself invoiced.
INVOICE_STATUS = """
    SELECT ddt.id,
           CASE
               WHEN ddt.invoice_id IS NOT NULL THEN 'invoiced'
               WHEN NOT (COALESCE(reason.to_be_invoiced, FALSE)
                         AND (ddt.state = 'done'
                              OR (ddt.state = 'in_pack'
                                  AND company.delivery_price_policy
                                      = 'delivery')))
                 OR NOT EXISTS (SELECT 1 FROM {line} line
                                 WHERE line.package_preparation_id = ddt.id)
                   THEN 'no'
               WHEN NOT EXISTS (SELECT 1 FROM {line} line
                                 WHERE line.package_preparation_id = ddt.id
                                   AND COALESCE(line.line_invoiced, FALSE)
                                       = FALSE) THEN 'invoiced'
               ELSE 'to invoice'
           END AS expected
      FROM {ddt} ddt
      LEFT JOIN stock_picking_transportation_reason reason
             ON reason.id = ddt.transportation_reason_id
      LEFT JOIN res_company company ON company.id = ddt.company_id
""".format(ddt=DDT_TABLE, line=LINE_TABLE)

# _compute_to_be_invoiced(): the reason for transportation first - the flag
# mirrors it - then False as soon as the delivery note is fully invoiced,
# which _is_fully_invoiced() reads as "it carries an invoice, or it has
# lines and none of them is left to invoice".
TO_BE_INVOICED = """
    SELECT ddt.id,
           CASE
               WHEN NOT COALESCE(reason.to_be_invoiced, FALSE) THEN FALSE
               WHEN ddt.invoice_id IS NOT NULL THEN FALSE
               WHEN EXISTS (SELECT 1 FROM {line} line
                             WHERE line.package_preparation_id = ddt.id)
                AND NOT EXISTS (SELECT 1 FROM {line} line
                                 WHERE line.package_preparation_id = ddt.id
                                   AND COALESCE(line.line_invoiced, FALSE)
                                       = FALSE) THEN FALSE
               ELSE TRUE
           END AS expected
      FROM {ddt} ddt
      LEFT JOIN stock_picking_transportation_reason reason
             ON reason.id = ddt.transportation_reason_id
""".format(ddt=DDT_TABLE, line=LINE_TABLE)


def _chunks(ids):
    for start in range(0, len(ids), CHUNK_SIZE):
        yield ids[start:start + CHUNK_SIZE]


def _sync_line_invoiced(env):
    """Recompute line_invoiced through the ORM, one bounded batch at a time.

    _is_line_invoiced() is the module's own predicate and it is the only
    thing which knows the policy of the sale order line, so it is asked
    rather than reimplemented. The verdict is written back in SQL, and the
    two delivery note fields are swept afterwards, so the ORM never has to
    carry a cascade across the whole table.
    """
    cr = env.cr
    cr.execute("SELECT id FROM %s ORDER BY id" % LINE_TABLE)
    ids = [row[0] for row in cr.fetchall()]
    if not ids:
        return 0

    lines_model = env["stock.picking.package.preparation.line"]
    changed = 0
    for chunk in _chunks(ids):
        cr.execute(
            "SELECT id, COALESCE(line_invoiced, FALSE) FROM %s"
            " WHERE id IN %%s" % LINE_TABLE, (tuple(chunk),))
        stored = dict(cr.fetchall())
        raise_, lower = [], []
        for line in lines_model.browse(chunk).exists():
            expected = line._is_line_invoiced()
            if expected != stored[line.id]:
                (raise_ if expected else lower).append(line.id)
        for value, todo in ((True, raise_), (False, lower)):
            if todo:
                cr.execute(
                    "UPDATE %s SET line_invoiced = %%s WHERE id IN %%s"
                    % LINE_TABLE, (value, tuple(todo)))
                changed += len(todo)
        # Keep the cache from growing over the whole table
        env.invalidate_all()
    return changed


def _sync_column(cr, table, column, expression):
    """Write ``column`` wherever the stored value disagrees with the rule."""
    cr.execute("""
        SELECT stale.id, stale.expected
          FROM (%s) AS stale
          JOIN %s target ON target.id = stale.id
         WHERE target.%s IS DISTINCT FROM stale.expected
         ORDER BY stale.id
    """ % (expression, table, column))
    todo = cr.fetchall()
    if not todo:
        return 0
    by_value = {}
    for record_id, expected in todo:
        by_value.setdefault(expected, []).append(record_id)
    for value, ids in by_value.items():
        for chunk in _chunks(ids):
            cr.execute(
                "UPDATE %s SET %s = %%s WHERE id IN %%s" % (table, column),
                (value, tuple(chunk)))
    return len(todo)


ORDER_LINE_FIELDS = ("qty_ddt_declared", "qty_to_invoice", "invoice_status")

# The order lines a delivery note declaration has something to say about,
# and the ones which stored a declared quantity that may no more hold. The
# whole point of the filter is that it is *small*: the sale order line table
# is the one an unbatched backfill must never walk.
DECLARED_ORDER_LINES = """
    SELECT DISTINCT sol.id
      FROM sale_order_line sol
      LEFT JOIN {line} ddt
             ON ddt.sale_line_id = sol.id
            AND ddt.force_invoiced IS TRUE
            AND ddt.invoice_line_id IS NULL
     WHERE ddt.id IS NOT NULL
        OR COALESCE(sol.qty_ddt_declared, 0) <> 0
     ORDER BY sol.id
""".format(line=LINE_TABLE)


def _sync_order_lines(env):
    """Recompute what the delivery note declarations owe the order lines.

    qty_ddt_declared, and with it the quantity left to invoice and the
    invoicing state, are recomputed through Odoo's own machinery: the two
    standard fields are computed by sale and by sale_order_line_qty_policy,
    and restating either in SQL would copy rules this module does not own.
    The candidates are picked in SQL first, so the ORM only ever sees the
    handful of order lines a declaration actually touches.
    """
    cr = env.cr
    cr.execute(DECLARED_ORDER_LINES)
    ids = [row[0] for row in cr.fetchall()]
    if not ids:
        return 0

    model = env["sale.order.line"]
    fields_to_do = [model._fields[name] for name in ORDER_LINE_FIELDS]
    for chunk in _chunks(ids):
        lines = model.browse(chunk).exists()
        if not lines:
            continue
        for field in fields_to_do:
            lines._recompute_todo(field)
        lines.recompute()
        env.invalidate_all()
    return len(ids)


def sync_policy_fields(env):
    """Recompute every stored field of the policy on existing documents."""
    lines = _sync_line_invoiced(env)
    status = _sync_column(env.cr, DDT_TABLE, "invoice_status",
                          INVOICE_STATUS)
    flag = _sync_column(env.cr, DDT_TABLE, "to_be_invoiced", TO_BE_INVOICED)
    orders = _sync_order_lines(env)
    if not (lines or status or flag or orders):
        _logger.info(
            "sale_order_line_qty_policy_ddt: the invoicing state of every"
            " delivery note is up to date, nothing to recompute")
    else:
        _logger.info(
            "sale_order_line_qty_policy_ddt: recomputed line_invoiced on %s"
            " delivery note lines, invoice_status on %s and to_be_invoiced"
            " on %s delivery notes, and the declared quantity of %s sale"
            " order lines", lines, status, flag, orders)
    return lines, status, flag, orders


def create_qty_ddt_declared_column(cr):
    """Create qty_ddt_declared before Odoo notices it is missing.

    Odoo mass-computes a stored field over the **whole** table when it
    creates its column, and it does so in one transaction: ``recompute()``
    walks every record of sale.order.line, and reading qty_ddt_declared
    prefetches each line's delivery note lines into the ORM cache. That is
    the shape which died against limit_memory_hard on 2026-08-29 and took an
    upgrade down with it - and it would be spent to write 0 nearly
    everywhere, since only a line a delivery note declaration points at can
    hold anything else.

    Creating the column here - empty, which Odoo reads as 0.0 - makes
    _auto_init find it in place and skip that pass entirely. The real values
    are then written by _sync_order_lines(), over the handful of order lines
    picked in SQL. `numeric` is the column type Odoo gives a Float carrying
    a decimal precision, the same one qty_to_invoice has.

    Called before the schema is built, from both ways in: pre_init_hook on
    installation, and migrations/*/pre-migrate.py on upgrade - the only two
    moments which come before _auto_init.
    """
    cr.execute("""
        SELECT 1 FROM information_schema.columns
         WHERE table_name = 'sale_order_line'
           AND column_name = 'qty_ddt_declared'
    """)
    if cr.fetchone():
        return False
    cr.execute("ALTER TABLE sale_order_line ADD COLUMN qty_ddt_declared"
               " numeric")
    _logger.info(
        "sale_order_line_qty_policy_ddt: created sale_order_line"
        ".qty_ddt_declared empty, to spare a recomputation of the whole"
        " table")
    return True


def pre_init_hook(cr):
    """Prepare the schema before the module is installed."""
    create_qty_ddt_declared_column(cr)


def post_init_hook(cr, registry):
    """Apply the policy to the delivery notes which predate the module.

    A database which never had this module still has its history, and the
    policy has an opinion on every document in it from the moment the module
    is installed. Odoo computes the new fields by itself only when it
    creates their columns, which an installation over surviving columns does
    not do - see the module docstring.
    """
    sync_policy_fields(api.Environment(cr, SUPERUSER_ID, {}))
