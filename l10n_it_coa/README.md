# l10n_it_coa — Italian Chart of Accounts for Odoo 18.0

Italian localization module providing a complete chart of accounts (Piano dei
Conti) based on the CEE / Zeroincombenze scheme, **migrated to the Odoo 18.0
accounting template architecture**.

## What it installs

| Model | File | Records |
|-------|------|---------|
| `account.account` | `data/template/account.account-it_coa.csv` | 737 accounts |
| `account.group` | `data/template/account.group-it_coa.csv` | 53 hierarchical groups |
| `account.tax.group` | `data/template/account.tax.group-it_coa.csv` | 27 VAT groups (IT + EU-OSS) |
| `account.tax` | `data/template/account.tax-it_coa.csv` | 171 taxes (incl. 9 group taxes) |
| `account.fiscal.position` | `data/template/account.fiscal.position-it_coa.csv` | 29 fiscal positions (incl. EU-OSS) |

The chart template is registered through `models/template_it_coa.py` using the
Odoo 17+/18 `@template('it_coa')` decorator API.

## Important: architecture change vs. the source files

The uploaded CSVs used the **legacy Odoo 10.0** template models
(`account.account.template`, `account.tax.template`,
`account.fiscal.position.template`, …). **Those models no longer exist in
Odoo 17.0+/18.0** — the chart-of-accounts system was rewritten. A literal
XML conversion using `*.template` models would therefore **fail to install**
in Odoo 18.0.

This module is built the way Odoo 18.0 actually loads localizations:

* a Python `AbstractModel` inheriting `account.chart.template` with
  `@template`-decorated methods (`models/template_it_coa.py`);
* CSV data files in `data/template/` named `<model>-it_coa.csv`, using the
  **real** model field names (not the removed `*.template` models).

### Key field migrations performed

* **Accounts**: `user_type_id` (e.g. `account.data_account_type_current_assets`)
  → `account_type` selection (`asset_current`, `asset_fixed`,
  `expense_depreciation`, `liability_payable`, `equity_unaffected`, …).
  Account-to-group linking is now automatic via code prefixes.
* **Groups**: `code_prefix` → `code_prefix_start` / `code_prefix_end`.
* **Taxes** (the major change): the Odoo 10 fields `type`, `account_id`,
  `refund_account_id`, `price_include` were replaced by
  `type_tax_use` + **`repartition_line_ids`**. Each percentage tax now emits
  four repartition lines (base/tax for invoice and refund), with the VAT
  account placed on the `tax` repartition lines. `price_include` →
  `price_include_override`. Children of `group` taxes are hidden from the tax
  selector (`type_tax_use = none`).
* **Tax groups**: the EU-OSS `account.tax.group` records must keep `country_id`
  **empty**. A tax's `country_id` is computed from the company fiscal country
  (`base.it`), and Odoo's `validate_tax_group_id` constraint blocks install if a
  group's `country_id` differs from the tax using it ("The tax group must have
  the same country_id as the tax using it."). Only the Italian group keeps
  `base.it`.
* **Fiscal positions**: rebuilt as `account.fiscal.position` with
  `auto_apply`, `country_id` / `country_group_id` (EU-OSS positions auto-apply
  per country; `intra` applies to the EU country group).

## Dependencies

* `account`, `base_iban`, `base_vat` (Odoo core)
* `account_usability` (OCA — *account-financial-tools*) for the extended
  account-group features requested for this chart of accounts.

> Make sure the OCA `account_usability` module is available in your addons
> path before installing.

## Installation

1. Copy the `l10n_it_coa` folder into your Odoo 18.0 addons path.
2. Ensure the OCA `account_usability` module is in the addons path.
3. Update the apps list and install **l10n_it_coa**.
4. In Accounting → Configuration → Settings, select the
   "Italia - Piano dei conti (Zeroincombenze)" chart template for the company
   (only possible before any accounting entry exists).
