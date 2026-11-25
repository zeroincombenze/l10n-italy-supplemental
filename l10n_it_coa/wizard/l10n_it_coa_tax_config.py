# Part of the l10n_it_coa module.
from odoo import api, fields, models
from odoo.exceptions import UserError


class L10nItCoaTaxConfig(models.TransientModel):
    _name = "l10n_it_coa.tax.config"
    _description = "Configure Italian taxes (tax grids, accounts, exemptions)"

    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )
    tax_ids = fields.Many2many(
        "account.tax",
        string="Taxes",
        domain="[('company_id', '=', company_id)]",
        help="Taxes to configure. Leave empty to configure all it_coa taxes.",
    )
    result = fields.Text(readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get("active_model") == "account.tax":
            ids = self.env.context.get("active_ids") or []
            taxes = self.env["account.tax"].browse(ids).exists()
            if taxes:
                res["tax_ids"] = [(6, 0, taxes.ids)]
                res["company_id"] = taxes[0].company_id.id
        return res

    def _csv_ids(self):
        """Map the selected taxes to the it_coa template ids (CSV ids)."""
        self.ensure_one()
        prefix = f"account.{self.company_id.id}_"
        csv_ids, skipped = [], []
        for tax in self.tax_ids:
            xmlid = tax.get_external_id().get(tax.id) or ""
            if xmlid.startswith(prefix):
                csv_ids.append(xmlid[len(prefix) :])
            else:
                skipped.append(tax.name)
        return csv_ids, skipped

    def action_configure(self):
        self.ensure_one()
        csv_ids, skipped = self._csv_ids()
        if self.tax_ids and not csv_ids:
            raise UserError(
                self.env._("None of the selected taxes comes from the it_coa chart.")
            )
        done = self.env["account.chart.template"].l10n_it_coa_configure_taxes(
            self.company_id, tax_ids=csv_ids or None
        )
        lines = [self.env._("%s taxes configured.", len(done))]
        if skipped:
            lines.append(
                self.env._("Skipped (not it_coa taxes): %s", ", ".join(skipped))
            )
        self.result = "\n".join(lines)
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }
