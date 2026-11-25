# Part of the l10n_it_coa module.
import logging

from odoo import Command, models

from . import tax_config_data as cfg

_logger = logging.getLogger(__name__)


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------
    def l10n_it_coa_configure_taxes(self, company=None, tax_ids=None):
        """Complete VAT configuration of the it_coa taxes, tax grids included.

        Callable at any time after the chart has been loaded, e.g. from a shell:
            env["account.chart.template"].l10n_it_coa_configure_taxes()

        For every it_coa tax of the company it sets:
        * the tax grids (tags) of base and tax repartition lines, refunds with the
          opposite sign; the tags are created when the Italian tax report of
          ``l10n_it`` is not installed;
        * the VAT accounts of the repartition lines, invoices and refunds;
        * the cash basis exigibility and transition account (VAT per cassa);
        * the exemption reason and law reference, when ``l10n_it`` is installed;
        * the tax group accounts and the known data fixes of the CSV.

        The function is idempotent and never deletes repartition lines, so it is
        safe on a database with posted entries.

        :param company: res.company to configure (default: current company)
        :param tax_ids: optional list of it_coa tax ids (CSV ids) to restrict to
        :return: dict {tax id: True} of the configured taxes
        """
        company = company or self.env.company
        self = self.with_company(company)
        done = {}
        self._l10n_it_coa_configure_tax_groups()
        for tax_id, vals in self._l10n_it_coa_tax_config().items():
            if tax_ids and tax_id not in tax_ids:
                continue
            tax = self.ref(tax_id, raise_if_not_found=False)
            if not tax:
                continue
            if not self._l10n_it_coa_apply_tax_config(tax, vals):
                continue
            done[tax_id] = True
        _logger.info("l10n_it_coa: %d taxes configured for %s", len(done), company.name)
        return done

    # ------------------------------------------------------------------
    # Configuration table
    # ------------------------------------------------------------------
    def _l10n_it_coa_tax_config(self):
        """Return {tax id: config} built from tax_config_data.

        config keys: base_tags, tax_tags, account, tax_vals (fields of the tax)
        and optionally exemption (reason, law).
        """
        res = {}

        def add(tax_id, base, tax, account, exemption=None, **tax_vals):
            res[tax_id] = {
                "base_tags": base,
                "tax_tags": tax,
                "account": account,
                "exemption": exemption,
                "tax_vals": tax_vals,
            }

        for tid, (base, tax, account) in cfg.STANDARD_TAXES.items():
            add(tid, base, tax, account)
        for tid, (base, tax, account, transit) in cfg.CASH_BASIS_TAXES.items():
            add(
                tid,
                base,
                tax,
                account,
                tax_exigibility="on_payment",
                cash_basis_transition_account_id=transit,
            )
        for tid, (base, tax) in cfg.REVERSE_CHARGE_PURCHASE.items():
            add(tid, base, tax, cfg.REVERSE_CHARGE_PURCHASE_ACCOUNT)
        base, tax = cfg.REVERSE_CHARGE_SALE_TAGS
        for tid in cfg.REVERSE_CHARGE_SALE:
            add(tid, base, tax, cfg.REVERSE_CHARGE_SALE_ACCOUNT)
        for key, (reason, law, sale, purchase) in cfg.ZERO_RATE_TAXES.items():
            for suffix, tags in (("v", sale), ("a", purchase)):
                if tags is not None:
                    add(key + suffix, tags, [], False, (reason, law))
        for prefix in cfg.PARTIAL_DEDUCTIBLE_PREFIXES:
            add(prefix + "a", [], [], False)
            exemption = None
            if prefix.endswith("0"):  # 0% deductible part, no VAT amount
                exemption = cfg.PARTIAL_ZERO_REASON
            add(
                prefix + "b",
                ["+03"],
                ["+5v"],
                cfg.PARTIAL_DEDUCTIBLE_ACCOUNT,
                exemption,
            )
        for tid, fixes in cfg.TAX_FIXES.items():
            res.setdefault(
                tid,
                {
                    "base_tags": None,
                    "tax_tags": None,
                    "account": None,
                    "exemption": None,
                    "tax_vals": {},
                },
            )["tax_vals"].update(fixes)
        return res

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _l10n_it_coa_configure_tax_groups(self):
        for group_id, accounts in cfg.TAX_GROUPS.items():
            group = self.ref(group_id, raise_if_not_found=False)
            if not group:
                continue
            vals = {}
            for field, code in accounts.items():
                account = self.ref(code, raise_if_not_found=False)
                if account and field in group._fields:
                    vals[field] = account.id
            group.write(vals)

    def _l10n_it_coa_get_tag(self, name):
        """Return the tax grid tag named like '+02' / '-02' of Italy.

        Missing tags are created in the same way as the tax report expressions do.
        """
        country = self.env.ref("base.it")
        tag_model = self.env["account.account.tag"]
        tag_name, negate = name[1:], name[0] == "-"
        tags = tag_model._get_tax_tags(tag_name, country.id)
        if len(tags) < 2:
            expression = self.env["account.report.expression"]
            tag_model.create(
                expression._get_tags_create_vals(tag_name, country.id, tags[:1])
            )
            tags = tag_model._get_tax_tags(tag_name, country.id)
        return tags.filtered(lambda t: t.tax_negate == negate)[:1]

    @staticmethod
    def _l10n_it_coa_flip(tags):
        return [("-" if t[0] == "+" else "+") + t[1:] for t in tags]

    def _l10n_it_coa_apply_tax_config(self, tax, config):
        """Apply the config; return False when the tax is not an it_coa one.

        Other Italian charts (e.g. core ``it``) reuse some tax ids: a tax whose VAT
        account is missing in the company is left untouched.
        """
        if config["account"] and not self.ref(config["account"], False):
            return False
        vals = {}
        for field, value in config["tax_vals"].items():
            if field.endswith("_id") and isinstance(value, str):
                value = self.ref(value).id
            vals[field] = value
        exemption = config["exemption"]
        if exemption and "l10n_it_exempt_reason" in tax._fields:
            vals["l10n_it_exempt_reason"], vals["l10n_it_law_reference"] = exemption
        if config["base_tags"] is not None:
            account = (
                self.ref(config["account"], raise_if_not_found=False)
                if config["account"]
                else self.env["account.account"]
            )
            for doc, lines in (
                ("invoice", tax.invoice_repartition_line_ids),
                ("refund", tax.refund_repartition_line_ids),
            ):
                sign_fn = (lambda t: t) if doc == "invoice" else self._l10n_it_coa_flip
                commands = self._l10n_it_coa_line_commands(
                    lines,
                    sign_fn(config["base_tags"]),
                    sign_fn(config["tax_tags"]),
                    account,
                )
                vals[f"{doc}_repartition_line_ids"] = commands
        tax.write(vals)
        return True

    def _l10n_it_coa_line_commands(self, lines, base_tags, tax_tags, account):
        """Update the existing base/tax lines in place (never unlink them)."""
        commands = []
        for rtype, tags in (("base", base_tags), ("tax", tax_tags)):
            tag_ids = [self._l10n_it_coa_get_tag(t).id for t in tags]
            vals = {"tag_ids": [Command.set(tag_ids)]}
            if rtype == "tax":
                vals["account_id"] = account.id or False
            line = lines.filtered(lambda ln: ln.repartition_type == rtype)[:1]
            if line:
                commands.append(Command.update(line.id, vals))
        return commands
