# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this module.

## What this is

`sale_order_line_qty_policy` is an Odoo **10.0** addon (`10.0.0.1.4`, AGPL-3,
`development_status: Alpha`) that lets a sale order line be **declared** delivered or invoiced —
by hand or by a policy declared on the product — instead of being judged on quantities alone.
It lives in `/home/odoo/odoo10/l10n-italy-supplemental`, remote
`git@github.com:zeroincombenze/l10n-italy-supplemental.git`, branch `10.0`, git org
**zeroincombenze** (the user's own repo, freely modifiable). Author SHS-AV s.r.l., maintainer
Antonio Maria Vigliotti. Whole history so far is one commit, `d0d72ac510d` (2026-08-29).

The problem it solves: standard Odoo closes a line only when the invoiced quantity reaches the
ordered (or delivered) one. Two recurring cases leave an order open forever — a product whose
amount is *recomputed at invoice level* (the CONAI environmental contribution), and a product that
*cannot be delivered to the exact quantity* (bulk goods). Both are handled without ever touching
`qty_delivered`: **the customer is always invoiced for what was really delivered.**

Only `sale` is a dependency. Three files of models, two view files, no new model, no security file,
no wizard, no data, no demo, no `i18n/`.

## Field map

| Model | Field | Kind | Role |
|---|---|---|---|
| `product.template` | `delivered_threshold` | Float (`Discount` precision) | max accepted %-deviation ordered↔delivered; `0` = inherit the category |
| `product.template` | `auto_line_invoiced` | Boolean | every line of this product counts as fully invoiced |
| `product.category` | `delivered_threshold` | Float | default threshold for the whole family; `0` = policy off |
| `sale.order.line` | `force_delivered` | Boolean, `copy=False` | "declared delivered" by hand |
| `sale.order.line` | `force_invoiced` | Boolean, `copy=False` | "declared invoiced" by hand → line drops out of invoicing |
| `sale.order.line` | `line_delivered` | Boolean, **computed + stored**, readonly | the verdict: reached qty, *or* within threshold, *or* declared |
| `sale.order` | `force_delivery_state` | Boolean | **shared with `sale_delivery_state_z0`** — see below |
| `sale.order` | `force_delivery_state_manual` | Boolean, `copy=False`, readonly | ownership marker: a human wrote the flag |

Public API on `sale.order.line`: `action_declare_delivered()` / `action_undeclare_delivered()` /
`action_declare_invoiced()` / `action_undeclare_invoiced()`. Nothing outside this module calls them
yet, and **no module in the tree depends on this one** — but `force_delivered` / `force_invoiced` /
`line_delivered` are exposed in the *Sales Order Lines* list and its filters, so treat them as API.

## The three mechanisms

### 1. The delivered threshold (`_delivered_deviation_ok`)

`_get_delivered_threshold()` = product's own value **or** its category's (product wins; there is no
"0 means 0", 0 always means "inherit / off"). The deviation is `|ordered − delivered| / |ordered| *
100`, so **under and over delivery are treated alike**. Two deliberate short-circuits:

- a line with `qty_delivered == 0` is **never** within threshold, whatever the percentage;
- `_is_line_delivered()` returns True on `qty_delivered >= product_uom_qty` *before* looking at the
  threshold, so plain over-delivery closes the line even with no policy configured at all.

The comparison is `float_compare(deviation, threshold, precision_digits=2)` — hardcoded 2 digits,
while the field itself carries the `Discount` decimal precision. Fine today, a mismatch if anyone
raises that precision.

### 2. Invoice status (`_get_to_invoice_qty` / `_compute_invoice_status` overrides)

`_is_line_invoiced()` = `force_invoiced or product_id.auto_line_invoiced`, and it zeroes
`qty_to_invoice`, which is what makes `action_invoice_create` skip the line. `_compute_invoice_status`
then fixes three verdicts standard Odoo would get wrong, **in this order**:

1. line is "declared invoiced" → `invoiced`;
2. Odoo said `upselling` but the over-delivery is within threshold → `invoiced`
   (delivering 101 of 100 with a 2% threshold is not an upselling occasion);
3. Odoo said anything but `to invoice`, the line *is* delivered by threshold, something was
   invoiced, and `qty_invoiced >= qty_delivered` → `invoiced`
   (99 of 100 delivered and 99 invoiced: standard Odoo leaves it at `no` forever).

**Do not panic about the `@api.depends` on the overrides.** Odoo 10 *concatenates* the `_depends` of
every method in the MRO when `compute` is declared as a string (`odoo/fields.py:520-523`), so these
add to the base dependencies instead of replacing them. Re-declaring the base ones would duplicate,
not fix.

### 3. Order-level flag ownership — the safe-degradation design

`force_delivery_state` is declared here **with the very same definition as in
`sale_delivery_state_z0`**, on purpose: Odoo keeps a single field, both modules see it, and neither
depends on the other. `sale_delivery_state_z0` reads it to show the order as delivered; this module
writes it from `_update_force_delivery_state()` (called on `action_confirm`, `action_cancel`, line
`create`, and line `write` touching any of `QTY_POLICY_TRIGGERS`).

Ownership is carried by `force_delivery_state_manual`, and the polarity is the point:

- `SaleOrder.write()` stamps `manual=True` whenever `force_delivery_state` is written **without** the
  marker in the same `vals` — so `sale_delivery_state_z0`'s own buttons, a connector, or an import
  all claim the flag for a human;
- `_update_force_delivery_state()` writes **both** keys together, which is how the policy writes
  without claiming the flag;
- `create()` is deliberately *not* intercepted, and `force_delivery_state` is copyable — so a
  duplicated order arrives with `manual=False` and the policy simply takes the flag back.

**A NULL/unknown marker means "the policy owns this", never "a human owns this".** That is a direct
lesson from the 2026-08-29 production incident (see *History* below): a boolean must never be able to
strand records when its column is lost. `test_13_stale_flag_is_taken_back` guards exactly this.

Lines that take part in the verdict: `_is_qty_policy_line()` skips lines without a product, services,
and anything with a truthy `product_id.is_delivery`. Note that **product-level `is_delivery` only
exists when `l10n_it_ddt` is installed** — core `delivery` puts `is_delivery` on `sale.order.line`,
not on the product. This is not a bug: `sale_delivery_state_z0._is_delivery()` uses the identical
`hasattr(product_id, "is_delivery")` idiom, so the two modules genuinely agree, and carrier products
are services anyway, which are skipped one line earlier.

## The `action_draft` override

Standard `sale.order.action_draft` does `procurement_ids.write({'sale_line_id': False})`, detaching
every procurement from its line. `qty_delivered` is then frozen at the value of the last delivery —
forever, even after a return. This module recomputes it from `_get_delivered_qty()` for `consu` /
`product` lines only (for a detached line that means **0**, coherently with Odoo counting only new
procurements from now on). Services are left alone: their delivered quantity is typed by a human and
`_get_delivered_qty()` would wipe it (`test_15`).

Caveat: `_get_delivered_qty()` returns `0.0` in plain `sale` — the real implementation is in
`sale_stock`, which is **not** a dependency. On a sale-only install this override therefore zeroes
stockable lines unconditionally. That is also why the test case is `post_install`.

## Commands

Odoo 10 is Python 2.7. Interpreter `/home/odoo/odoo10/venv_odoo/bin/python`, launcher
`/home/odoo/odoo10/odoo-bin`, config `/etc/odoo/odoo10.conf`, PostgreSQL on **port 5434**, role
`odoo10`, socket `/var/run/postgresql`. **Never run tests outside the venv** — see the `testing`
skill.

`test_sale_order_line_qty_policy_10` has the module installed at 10.0.0.1.4 with demo data, plus
`sale_stock`, `stock`, `delivery`, `sale_delivery_state_z0` and `l10n_it_conai` (58 modules). Clone
it rather than working in it:

```bash
createdb -p 5434 -U odoo10 -h /var/run/postgresql \
    -T test_sale_order_line_qty_policy_10 test_solqp_scratch_10

source /home/odoo/odoo10/venv_odoo/bin/activate     # HOME becomes the venv
python /home/odoo/odoo10/odoo-bin -c /etc/odoo/odoo10.conf -d test_solqp_scratch_10 \
    --db_host=/var/run/postgresql --db_port=5434 --db_user=odoo10 \
    -u sale_order_line_qty_policy --test-enable --stop-after-init \
    --no-xmlrpc --workers=0 --max-cron-threads=0 --log-level=test --logfile=/tmp/solqp.log
deactivate
```

- **`--workers=0`** — the config sets `workers = 2`; without it `--stop-after-init` forks instead of
  running the tests in-process.
- **`--no-xmlrpc`** — port 8170 is normally taken by the running odoo10 instance.
- **The DB must have demo data.** `loading.py:183-207` gates the whole test block on `has_demo`
  (`hasattr(package,'demo') or (package.dbdemo and state != 'installed')`); this module ships no
  demo file, so it rides on `ir_module_module.demo = true`, which the template DB has. Against a
  demo-less DB `--test-enable` runs *nothing* and still exits 0 — a hollow green.
- Tests are `at_install = False` / `post_install = True` — mandatory: `sale.order` creation needs
  `picking_policy` from `sale_stock`, which is not a dependency, so at-install they die with
  `NotNullViolation`.

**Last verified run (2026-09-01, at 10.0.0.1.4, `-u` on a clone of the test DB):** `Ran 16 tests in
15.301s ... OK`, zero ERROR/FAIL lines, exit 0. The run logs
`The domain term "('product_id', '=', [40, 41, 42])" should use the 'in' operator` on every test —
that is `l10n_it_ddt`'s `mark_real_delivery_lines` defect, not this module.

Version numbering follows the `versioning` skill (`10.0.A.B.C`, bumped once per commit from git), and
every release adds a `readme/CHANGELOG.rst` entry in the `* [TAG] text` style. `README.rst` is
generated from `readme/*.rst` by `oca-gen-addon-readme` — **edit the fragments, not `README.rst`**,
and keep the `.it_IT` twin of DESCRIPTION / CONFIGURATION / USAGE in sync.

## Test suite

`tests/test_sale_order_line_qty_policy.py`, one `TransactionCase`, 16 tests, fixtures built in
`setUp` (six products covering: threshold on product, no policy, `auto_line_invoiced`, threshold with
`invoice_policy='order'`, threshold from the category, product overriding its category). Coverage map:
01 auto-invoiced · 02 force_invoiced · 03 force_delivered · 04 under-delivery · 05 over-delivery ·
06 threshold exceeded · 07 upselling · 08 category threshold · 09 product overrides category ·
10 flag set by policy · 11 manual flag kept · 12 services skipped · 13 stale flag taken back ·
14/15 reset to draft · 16 no policy → no change.

## History and the incident behind the design

`readme/CHANGELOG.rst` is the short version; what matters when editing:

- **10.0.0.1.3** renamed `force_delivery_state_auto` → `force_delivery_state_manual`, inverting the
  polarity so an unknown value hands control back to the code.
- **10.0.0.1.4** *removed the migration script altogether*. Its predecessor `search([])`-ed 26,775
  sale orders in one transaction, died of `MemoryError` against `limit_memory_hard`, failed the whole
  upgrade, and the recovery (uninstall/reinstall) **dropped every column this module owns and
  permanently destroyed the configured `delivered_threshold` values**. Odoo keeps no history of field
  values. If you ever re-add a backfill here: batch it, `env.invalidate_all()` + `cr.commit()` per
  batch, pre-filter in SQL, and verify the loop actually runs.
- Consequence of that removal, by design: orders confirmed **before** the module was installed keep
  whatever `force_delivery_state` they had until one of their lines is touched. In
  `test_sale_order_line_qty_policy_10` that is 10 orders at `t`/`manual=f` today.
- The rename also left an orphan `sale_order.force_delivery_state_auto` column in that DB — the ORM
  never drops columns. Harmless; don't be surprised by it.

## Open points (found by inspection 2026-09-01, none covered by a test)

Strike an item when you fix it rather than leaving it to be rediscovered.

1. **`SaleOrderLine.create` re-evaluates the whole order per line.** Importing or duplicating an
   order with N lines runs `_update_force_delivery_state()` N times, each mapping and filtering all
   lines. Fine interactively, quadratic on bulk imports — the same shape of cost that killed the
   migration script.
2. **The stored `line_delivered` depends on delegated fields** (`product_id.delivered_threshold`,
   `product_id.categ_id.delivered_threshold`, both `_inherits`-delegated from `product.template`).
   Editing a threshold on an existing product or category *should* retrigger the stored values on
   confirmed lines; that path is untested — verify before relying on it, and consider a small
   `write()` override on the two carriers if it turns out not to propagate.
3. **CONAI integration is configuration, not code.** Nothing sets `auto_line_invoiced`
   automatically; `l10n_it_conai`'s product (`l10n_it_conai.product_conai`, referenced as
   `company.conai_product_id`) must be flagged by hand. It is a `service`, so it is skipped by
   `_is_qty_policy_line()` on the delivery side — the two halves are coherent, but a user who forgets
   the flag gets the exact symptom the module was written to cure.
4. `force_delivery_state` is duplicated verbatim from `sale_delivery_state_z0`. If that module's
   definition ever changes (`string`, `help`, `copy`), this copy must follow, or the merged field
   silently takes whichever module loads last. **The same applies to `i18n/it.po`**: both catalogues
   translate that one field, so their two `msgstr` must stay byte-identical, or the help text changes
   with the module load order. They were briefly kept identical *including* a `"lo sato di
   consegnato"` typo; the typo was fixed in both files at once (2026-09-01, `sale_delivery_state_z0`
   10.0.1.0.2). Never fix such a string in one file only.

## Working conventions here

- Double quotes, `# -*- coding: utf-8 -*-`, AGPL-3 header naming SHS-AV, `@api.multi` / `@api.model`
  everywhere (Odoo 10 style — no bare methods).
- Every public method carries a docstring explaining the *why*; keep that up, the reasoning in those
  docstrings is the module's real documentation.
- `.pyc` files sit next to the `.py` in `models/` — untracked build artifacts, ignore them.
- The repo `.gitignore` ignores `.claude*` but **not** `CLAUDE.md`, so this file shows as untracked
  in `git status`. That matches `l10n-italy/l10n_it_ddt/CLAUDE.md`.
- There is no `_()` call anywhere: every user-facing string is a field `string`/`help` or a view
  label, all of which Odoo exports on its own.
- `i18n/it.po` is the Italian catalogue (26 entries, complete). Re-export the `.pot` with
  `--i18n-export` when strings change — Odoo 10 refuses a `.pot` extension, so export to `.po` and
  rename. The model name `sale.order.line` is translated here as **"Riga d'Ordine di Vendita"**,
  matching Odoo core `sale`; note `sale_delivery_state_z0` says "Riga ordine di vendita" for the same
  single `ir.model` record, so that one label depends on module load order. Core wins on volume, and
  this module sides with core.
