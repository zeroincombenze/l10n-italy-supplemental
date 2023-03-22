# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2021-22 librERP enterprise network <https://www.librerp.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime
from odoo import api, fields, models


class WizardAssetsGenerateDepreciations(models.TransientModel):
    _name = "wizard.asset.generate.depreciation"
    _description = "Generate Asset Depreciations"

    @api.model
    def get_default_company_id(self):
        return self.env.user.company_id

    @api.model
    def get_default_date_dep(self):

        def query_last_date(asset_id=None, final=None):
            query = (
                "SELECT MAX(date) FROM asset_depreciation_line"
                " WHERE move_type='depreciated'"
            )
            if asset_id:
                query += "and asset_id=%s" % asset_id
            if final:
                query += " and final='true'"
            self._cr.execute(query)
            return self._cr.fetchone()

        asset_id = self._context.get("active_id")
        date = query_last_date(asset_id=asset_id, final=True)
        if not date or not date[0]:
            date = query_last_date(final=False)
        if not date or not date[0]:
            query = "SELECT MIN(purchase_date) FROM asset_asset "
            if asset_id:
                query += " WHERE id=%s" % asset_id
            self._cr.execute(query)
            date = self._cr.fetchone()
        if date and date[0]:
            # Found depreciation
            last_date = date[0]
            last_date += datetime.timedelta(days=1)
        else:
            last_date = fields.Date.today()

        # search for end of fiscal year for returned last date
        fiscal_year = self.env["account.fiscal.year"].get_fiscal_year_by_date(
            last_date, company=self.env.user.company_id, miss_raise=False
        )
        if fiscal_year:
            return fiscal_year.date_to
        return fields.Date.today()

    @api.model
    def get_default_type_ids(self):
        return [(6, 0, self.env["asset.depreciation.type"].search([]).ids)]

    @api.depends("asset_ids")
    def _compute_asset_ids(self):
        for r in self:
            r.has_asset_ids = len(r.asset_ids) > 0
        # end for

    asset_ids = fields.Many2many(
        "asset.asset",
        string="Assets",
    )

    category_ids = fields.Many2many(
        "asset.category",
        string="Categories",
    )

    company_id = fields.Many2one(
        "res.company",
        default=get_default_company_id,
        string="Company",
    )

    date_dep = fields.Date(
        default=get_default_date_dep,
        required=True,
        string="Depreciation Date",
    )

    type_ids = fields.Many2many(
        "asset.depreciation.type",
        default=get_default_type_ids,
        required=True,
        string="Depreciation Types",
    )

    final = fields.Boolean(
        string="Final",
        default=False,
    )

    has_asset_ids = fields.Boolean(string="Has asset ids", compute="_compute_asset_ids")

    @api.multi
    def do_generate(self):
        """
        Launches the generation of new depreciation lines for the retrieved
        assets.
        Reloads the current window if necessary.
        """
        self.ensure_one()
        # Add depreciation date in context just in case
        deps = self.get_depreciations().with_context(
            dep_date=self.date_dep, final=self.final
        )
        dep_lines = deps.generate_depreciation_lines(self.date_dep)
        # deps.post_generate_depreciation_lines(dep_lines)
        if self._context.get("reload_window"):
            return {"type": "ir.actions.client", "tag": "reload"}

    def get_depreciations(self):
        self.ensure_one()
        domain = self.get_depreciations_domain()
        return self.env["asset.depreciation"].search(domain)

    def get_depreciations_domain(self):
        domain = [
            ("amount_residual", ">", 0.0),
            ("date_start", "!=", False),
            ("date_start", "<", self.date_dep),
            ("type_id", "in", self.type_ids.ids),
        ]
        if self.asset_ids:
            domain += [("asset_id", "in", self.asset_ids.ids)]
        if self.category_ids:
            domain += [("asset_id.category_id", "in", self.category_ids.ids)]
        if self.company_id:
            domain += [("company_id", "=", self.company_id.id)]
        return domain

    @api.multi
    def do_warning(self):
        self.ensure_one()
        wizard = self

        if self.final:
            lines = list()
            # mapping  warnings
            # default
            lines.append(
                (0, 0, {"reason": "ATTENZIONE: l'operazione è irreversibile!"})
            )

            # current_year = datetime.date.today().year
            year = self.date_dep.year
            end_year = datetime.date(year, 12, 31)
            current_date_str = self.date_dep.strftime("%d-%m-%Y")
            end_year_str = end_year.strftime("%d-%m-%Y")

            # check date
            if self.date_dep < end_year:
                lines.append(
                    (
                        0,
                        0,
                        {
                            "reason": "ATTENZIONE: la data inserita per l'ammortamento {curr}"
                            " è fuori esercizio (inferiore a quella usuale "
                            "per l'anno indicato {endy} ).".format(
                                curr=current_date_str, endy=end_year_str
                            )
                        },
                    )
                )

            if self.date_dep > end_year:
                lines.append(
                    (
                        0,
                        0,
                        {
                            "reason": "ATTENZIONE: la data inserita per l'ammortamento"
                            " {curr} è fuori esercizio (superiore a quella "
                            "usuale per l'anno indicato {endy}).".format(
                                curr=current_date_str, endy=end_year_str
                            )
                        },
                    )
                )

            # get assets
            deps = self.get_depreciations().with_context(
                dep_date=self.date_dep, final=self.final
            )
            for dep in deps:
                extra = dep.line_ids.filtered(
                    lambda ln: ln.move_type != "depreciated" and ln.final is False
                )
                if extra:
                    for ln in extra:
                        tipo = ln.depreciation_line_type_id.display_name
                        asset = ln.depreciation_id.display_name
                        lines.append(
                            (
                                0,
                                0,
                                {
                                    "reason": 'ATTENZIONE: il movimento "{movimento}" '
                                    'di tipo {tipo} per il bene "{asset}" '
                                    "risulta non consolidato".format(
                                        movimento=ln.name, asset=asset, tipo=tipo
                                    )
                                },
                            )
                        )

            wz_id = self.env["asset.generate.warning"].create(
                {
                    "wizard_id": wizard.id,
                    "reason_lines": lines,
                }
            )

            model = "assets_management"
            wiz_view = self.env.ref(model + ".asset_generate_warning")
            return {
                "type": "ir.actions.act_window",
                "name": "Richiesta conferma",
                "res_model": "asset.generate.warning",
                "view_type": "form",
                "view_mode": "form",
                "view_id": wiz_view.id,
                "target": "new",
                "res_id": wz_id.id,
                "context": {"active_id": wizard},
            }

        if self._context.get("depreciated"):
            return self.do_generate().with_context(depreciated=True)
        else:
            return self.do_generate()
