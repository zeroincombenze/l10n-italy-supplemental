# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2021-22 librERP enterprise network <https://www.librerp.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    asset_accounting_info_ids = fields.One2many(
        "asset.accounting.info", "invoice_id", string="Assets Accounting Info"
    )

    asset_ids = fields.Many2many(
        "asset.asset", compute="_compute_asset_data", store=True, string="Assets"
    )

    dep_line_ids = fields.Many2many(
        "asset.depreciation.line",
        compute="_compute_asset_data",
        store=True,
        string="Depreciation Lines",
    )

    hide_link_asset_button = fields.Boolean(
        compute="_compute_hide_link_asset_button",
        default=True,
        string="Hide Asset Button",
    )

    @api.constrains("company_id")
    def check_company(self):
        for inv in self:
            comp = inv.get_linked_aa_info_records().mapped("company_id")
            if len(comp) > 1 or (comp and comp != inv.company_id):
                raise ValidationError(
                    _(
                        "`{}`: cannot change invoice's company once it's already"
                        " related to an asset."
                    ).format(inv.name_get()[0][-1])
                )

    @api.multi
    def action_invoice_cancel(self):
        res = super().action_invoice_cancel()
        if self:
            asset = False
            # Remove every a.a.info related to current invoices, and delete
            # related depreciation lines
            aa_infos = self.mapped(lambda i: i.get_linked_aa_info_records())
            if aa_infos:
                asset = aa_infos[0].asset_id
            dep_lines = aa_infos.mapped("dep_line_id")
            aa_infos.unlink()
            # Filtering needed: cannot delete dep lines with a.a.info
            percentages = dep_lines.filtered(
                lambda ln: (
                    ln.move_type == "depreciated"
                    and ln.partial_dismissal is True
                    and ln.percentage > 0
                )
            )
            if percentages:
                percentage = percentages[0].percentage
            else:
                percentage = 0

            dep_lines.filtered(lambda l: not l.asset_accounting_info_ids).unlink()
            # clean sale data into asset
            if asset:
                if self.type in ("in_refund", "out_invoice"):
                    asset.sale_amount = 0.0
                    asset.sold = False
                    asset.sale_date = False
                    asset.sale_invoice_id = False
                    asset.customer_id = False
                    if percentage and asset.partial_dismiss_percentage >= percentage:
                        asset.partial_dismiss_percentage -= percentage
                elif self.type in ("in_invoice", "out_refund"):
                    asset.purchase_amount = 0.0
                    asset.purchase_date = False
                    asset.purchase_invoice_id = False
                    asset.supplier_id = False
                    asset.supplier_ref = False
        return res

    @api.multi
    @api.depends(
        "asset_accounting_info_ids",
        "asset_accounting_info_ids.asset_id",
        "asset_accounting_info_ids.dep_line_id",
    )
    def _compute_asset_data(self):
        for inv in self:
            aa_info = inv.get_linked_aa_info_records()
            assets = aa_info.mapped("asset_id")
            dep_lines = aa_info.mapped("dep_line_id")
            if dep_lines:
                assets += dep_lines.mapped("asset_id")
            inv.update(
                {
                    "asset_ids": [(6, 0, assets.ids)],
                    "dep_line_ids": [(6, 0, dep_lines.ids)],
                }
            )

    @api.multi
    def _compute_hide_link_asset_button(self):
        valid_account_ids = self.get_valid_accounts()
        if not valid_account_ids:
            self.update({"hide_link_asset_button": True})
        else:
            for inv in self:
                inv.hide_link_asset_button = not any(
                    [
                        ln.account_id.id in valid_account_ids.ids
                        for ln in inv.invoice_line_ids
                    ]
                ) or inv.state in ("draft", "cancel")

    @api.multi
    def open_wizard_manage_asset(self):
        """Wizard to connect invoice lines to asset"""
        self.ensure_one()
        lines = self.invoice_line_ids.filtered(
            lambda l: not l.asset_accounting_info_ids
        )
        if not lines:
            raise ValidationError(_("Every line is already linked to an asset."))

        xmlid = "assets_management.action_wizard_invoice_manage_asset"
        act = self.env.ref(xmlid).read()[0]
        ctx = dict(self._context)
        ctx.update(
            {
                "default_company_id": self.company_id.id,
                "default_dismiss_date": self.date_invoice or self.date_due,
                "default_purchase_date": self.date_invoice or self.date_due,
                "default_invoice_ids": [(6, 0, self.ids)],
                "default_invoice_line_ids": [(6, 0, lines.ids)],
                "invoice_ids": self.ids,
            }
        )
        act.update({"context": ctx})
        return act

    def get_linked_aa_info_records(self):
        self.ensure_one()
        return self.env["asset.accounting.info"].search(
            [
                "|",
                ("invoice_id", "=", self.id),
                ("invoice_line_id.invoice_id", "=", self.id),
            ]
        )

    def get_valid_accounts(self):
        return self.env["asset.category"].search([]).mapped("asset_account_id")
