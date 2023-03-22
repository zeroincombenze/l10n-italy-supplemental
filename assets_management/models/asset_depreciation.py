# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2021-22 librERP enterprise network <https://www.librerp.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero
import datetime


class AssetDepreciation(models.Model):
    _name = "asset.depreciation"
    _description = "Assets depreciation type summary"

    amount_depreciable = fields.Monetary(string="Depreciable Amount")

    amount_depreciable_updated = fields.Monetary(
        compute="_compute_amounts",
        store=True,
        string="Updated Amount",
    )

    amount_depreciated = fields.Monetary(
        compute="_compute_amounts",
        store=True,
        string="Depreciated Amount",
    )

    amount_gain = fields.Monetary(
        compute="_compute_amounts",
        string="Capital Gain",
        store=True,
    )

    amount_historical = fields.Monetary(
        compute="_compute_amounts",
        store=True,
        string="Historical Amount",
    )

    amount_in = fields.Monetary(
        compute="_compute_amounts",
        store=True,
        string="In Amount",
    )

    amount_loss = fields.Monetary(
        compute="_compute_amounts",
        store=True,
        string="Capital Loss",
    )

    amount_out = fields.Monetary(
        compute="_compute_amounts",
        store=True,
        string="Out Amount",
    )

    amount_residual = fields.Monetary(
        compute="_compute_amounts",
        store=True,
        string="Residual Amount",
    )

    asset_id = fields.Many2one(
        "asset.asset",
        ondelete="cascade",
        readonly=True,
        required=True,
        string="Asset",
    )

    base_coeff = fields.Float(
        default=1,
        help="Coeff to compute amount depreciable from purchase amount",
        string="Depreciable Base Coeff",
    )

    company_id = fields.Many2one(
        "res.company", readonly=True, related="asset_id.company_id", string="Company"
    )

    currency_id = fields.Many2one(
        "res.currency", readonly=True, related="asset_id.currency_id", string="Currency"
    )

    date_start = fields.Date(string="Date Start")

    dismiss_move_id = fields.Many2one("account.move", string="Dismiss Move")

    first_dep_nr = fields.Integer(
        default=1,
        string="First Dep. Num",
    )

    force_all_dep_nr = fields.Boolean(string="Force All Dep. Num")

    force_first_dep_nr = fields.Boolean(string="Force First Dep. Num")

    last_depreciation_date = fields.Date(
        compute="_compute_amounts",
        store=True,
        string="Last Dep.",
    )

    line_ids = fields.One2many(
        "asset.depreciation.line", "depreciation_id", string="Lines"
    )

    mode_id = fields.Many2one(
        "asset.depreciation.mode",
        required=True,
        string="Mode",
    )

    partial_dismiss_percentage = fields.Float(
        compute="_compute_amounts",
        store=True,
        string="Percentage of partial dismiss",
        default=0.0,
    )

    percentage = fields.Float(string="Depreciation (%)")

    pro_rata_temporis = fields.Boolean(string="Pro-rata Temporis")

    requires_account_move = fields.Boolean(
        readonly=True,
        related="type_id.requires_account_move",
        string="Requires Account Move",
    )

    state = fields.Selection(
        [
            ("non_depreciated", "Non Depreciated"),
            ("partially_depreciated", "Partially Depreciated"),
            ("totally_depreciated", "Depreciated"),
        ],
        compute="_compute_state",
        default="non_depreciated",
        store=True,
        string="State",
    )

    type_id = fields.Many2one("asset.depreciation.type", string="Depreciation Type")

    zero_depreciation_until = fields.Date(string="Zero Depreciation Up To")

    @api.model
    def create(self, vals):
        dep = super().create(vals)
        dep.normalize_first_dep_nr()
        if dep.line_ids:
            num_lines = dep.line_ids.filtered("requires_depreciation_nr")
            if num_lines:
                num_lines.normalize_depreciation_nr()
        return dep

    @api.multi
    def write(self, vals):
        if "line_ids" in vals:
            for line in vals["line_ids"]:
                if len(line) == 3 and line[2] and "asset_id" not in line[2]:
                    line[2].update({"asset_id": self.asset_id.id})
        res = super().write(vals)
        need_norm = self.filtered(lambda d: d.need_normalize_first_dep_nr())
        if need_norm:
            need_norm.normalize_first_dep_nr(force=True)
        for dep in self:
            num_lines = dep.line_ids.filtered("requires_depreciation_nr")
            if num_lines and num_lines.need_normalize_depreciation_nr():
                num_lines.normalize_depreciation_nr(force=True)
        return res

    @api.multi
    def unlink(self):
        if self.mapped("line_ids"):
            raise ValidationError(
                _(
                    "Cannot delete depreciations if there is any depreciation"
                    " line linked to it."
                )
            )
        if any([m.state != "draft" for m in self.mapped("dismiss_move_id")]):
            deps = self.filtered(
                lambda ln: ln.dismiss_move_id and ln.dismiss_move_id.state != "draft"
            )
            name_list = "\n".join([ln[-1] for ln in deps.name_get()])
            raise ValidationError(
                _(
                    "Following lines are linked to posted account moves, and"
                    " cannot be deleted:\n{}"
                ).format(name_list)
            )
        return super().unlink()

    @api.multi
    def name_get(self):
        return [(dep.id, dep.make_name()) for dep in self]

    @api.multi
    @api.depends("amount_depreciable", "amount_depreciable_updated", "amount_residual")
    def _compute_state(self):
        for dep in self:
            dep.state = dep.get_depreciation_state()

    @api.onchange("asset_id", "base_coeff")
    def onchange_base_coeff(self):
        purchase_amount = self.asset_id.purchase_amount
        self.amount_depreciable = self.base_coeff * purchase_amount

    @api.onchange("first_dep_nr")
    def onchange_normalize_first_dep_nr(self):
        if self.first_dep_nr <= 0:
            self.first_dep_nr = 1

    @api.onchange("force_all_dep_nr")
    def onchange_force_all_dep_nr(self):
        if self.force_all_dep_nr:
            self.first_dep_nr = 1

    @api.onchange("force_first_dep_nr")
    def onchange_force_first_dep_nr(self):
        if self.force_first_dep_nr and self.first_dep_nr <= 0:
            self.first_dep_nr = 1

    @api.onchange("force_all_dep_nr", "force_first_dep_nr")
    def onchange_force_dep_nrs(self):
        if self.force_all_dep_nr and self.force_first_dep_nr:
            self.force_all_dep_nr = False
            self.force_first_dep_nr = False
            title = _("Warning!")
            msg = _(
                "Fields `Force All Dep. Num` and `Force First Dep. Num`"
                " cannot be both active."
            )
            return {"warning": {"title": title, "message": msg}}
        if not self.force_all_dep_nr and self.force_first_dep_nr:
            self.first_dep_nr = 1

    @api.multi
    @api.depends(
        "amount_depreciable",
        "line_ids",
        "line_ids.amount",
        "line_ids.balance",
        "line_ids.date",
        "line_ids.move_type",
        "asset_id.purchase_amount",
        "asset_id.sale_amount",
        "asset_id.sold",
    )
    def _compute_amounts(self):
        for dep in self:
            dep.update(dep.get_computed_amounts())

    def check_before_generate_depreciation_lines(self, dep_date):
        # Check if self is a valid recordset
        if not self or not dep_date:
            raise ValidationError(
                _("Cannot create any depreciation according to current settings.")
            )

        if any([dep for dep in self if dep.state == "totally_depreciated"]):
            raise ValidationError("Cannot update totally depreciated types")

        for dep in self:
            lines = dep.mapped("line_ids")
            fiscal_year_model = self.env["account.fiscal.year"]
            fy = fiscal_year_model.get_fiscal_year_by_date(
                dep_date, company=dep.asset_id.company_id
            )
            date_from = fy.date_from
            prior_fy_date_to = fy.date_from - datetime.timedelta(1)

            newer_lines = lines.filtered(
                lambda ln: (ln.move_type == "depreciated" and ln.date > fy.date_to)
            )
            if newer_lines:
                asset_name = dep.asset_id.name
                nature_name = dep.type_id.name
                raise ValidationError(
                    _(
                        "The following asset {asset} contains depreciation newer"
                        " than end of fiscal year for nature {nature}"
                    ).format(asset=asset_name, nature=nature_name)
                )

            older_lines = lines.filtered(
                lambda ln: (
                    ln.move_type == "depreciated" and ln.date <= prior_fy_date_to
                )
            )
            last_depreciation_date = False
            if older_lines:
                last_depreciation_date = max([x.date for x in older_lines])
            if dep.asset_id.purchase_date <= prior_fy_date_to and (
                not last_depreciation_date or last_depreciation_date != prior_fy_date_to
            ):
                asset_name = dep.asset_id.name
                nature_name = dep.type_id.name
                raise ValidationError(
                    "Last fiscal year of following asset {asset} without valid"
                    " depreciation for nature {nature}".format(
                        asset=asset_name, nature=nature_name
                    )
                )

            extra_lines = lines.filtered(
                lambda ln: (
                    ln.move_type in lines.get_update_move_types()
                    and fy.date_from <= ln.date <= dep_date
                )
            )
            if extra_lines:
                prior_fy_date_to = max([x.date for x in extra_lines])
                date_from = prior_fy_date_to + datetime.timedelta(1)

            confirmed_lines = lines.filtered(
                lambda ln: (
                    ln.move_type == "depreciated"
                    and ln.date >= date_from
                    and ln.final is True
                )
            )
            if confirmed_lines:
                asset_name = dep.asset_id.name
                nature_name = dep.type_id.name
                raise ValidationError(
                    _(
                        "The following asset {} contains final depreciation newer"
                        " than depreciation date for nature {}"
                    ).format(asset=asset_name, nature=nature_name)
                )

            posted_lines = lines.filtered(
                lambda ln: (
                    ln.date >= date_from and ln.move_id and ln.move_id.state != "draft"
                )
            )
            if posted_lines:
                asset_name = dep.asset_id.name
                nature_name = dep.type_id.name
                raise ValidationError(
                    _(
                        "Cannot update the following assets {} which contains"
                        " posted depreciation for the nature {}:"
                    ).format(asset=asset_name, nature=nature_name)
                )

    def delete_current_depreciation_line(self, dep_date):
        self.check_before_generate_depreciation_lines(dep_date)
        lines_to_delete = self.check_current_depreciation_lines(dep_date)
        if lines_to_delete:
            lines_to_delete.button_remove_account_move()
            lines_to_delete.unlink()

    def generate_depreciation_lines(self, dep_date):
        # Set new date within context if necessary
        self.delete_current_depreciation_line(dep_date)

        new_lines = self.env["asset.depreciation.line"]
        for dep in self:
            new_lines |= dep.generate_depreciation_lines_single(dep_date)

        return new_lines

    def generate_depreciation_lines_single_vals(self, dep_date):
        self.ensure_one()
        final = self._context.get("final")
        dep_nr = self.get_next_depreciation_nr()
        dep = self.with_context(dep_nr=dep_nr, used_asset=self.asset_id.used)
        dep_amount = dep.get_depreciation_amount(dep_date)
        dep = dep.with_context(dep_amount=dep_amount, final=final)
        return dep.prepare_depreciation_line_vals(dep_date)

    def generate_depreciation_lines_single(self, dep_date):
        self.ensure_one()

        # TODO> Merge depreciation lines
        # fiscal_year_model = self.env['account.fiscal.year']
        # fy = fiscal_year_model.get_fiscal_year_by_date(
        #     dep_date, company=self.asset_id.company_id
        # )
        line_model = self.env["asset.depreciation.line"]
        # TODO> Merge depreciation lines
        # line_move = line_model.get_depreciation_lines(
        #     date_from=fy.date_from, date_to=fy.date_to,
        #     asset_ids=self.asset_id.id, type_ids=self.type_id.id)
        vals = self.generate_depreciation_lines_single_vals(dep_date)
        # TODO> Merge depreciation lines
        # if <flag_merge>:
        #     if not line_move:
        #         return line_model.create(vals)
        #     return line_move[0].write(
        #         {'date': vals['date'], 'amount': vals['amount'] + line_move[0].amount}
        #     )
        return line_model.create(vals)

    def generate_dismiss_line(self, vals, invoice_line_ids=None):
        """Generate dismission records.
        May be calls by invoice wizard (with invoice_line_ids)
        or from asset for disposal"""
        if "date" not in vals:
            raise ValidationError(_("Missed dismiss date"))
        if "asset_id" not in vals:
            raise ValidationError(_("Missed dismiss asset"))
        if "amount" not in vals:
            raise ValidationError(_("Missed dismiss amount"))
        digits = self.env["decimal.precision"].precision_get("Account")
        dismis_amount = vals["amount"]
        if isinstance(vals["date"], str):
            dismis_date = datetime.datetime.strptime(vals["date"], "%Y-%m-%d").date()
        else:
            dismis_date = vals["date"]
        deps = self.get_depreciations(date_ref=vals["date"], asset_ids=vals["asset_id"])
        partial_dismiss_percentage = vals.get("partial_dismiss_percentage", 100)
        if "partial_dismiss_percentage" in vals and partial_dismiss_percentage < 100.0:
            vals["partial_dismissal"] = True

        # Write out lines: depreciation line will be created before 'out' write!
        out_lines = self.env["asset.depreciation.line"]
        for dep in deps:
            vals["depreciation_id"] = dep.id
            dep_percentage = 100.0 - dep.partial_dismiss_percentage
            vals["amount"] = 0.0
            out_lines |= self.generate_dismiss_line_single(
                vals, invoice_line_ids=invoice_line_ids)

        # Out amount must be evaluated based on residual and out value
        line_model = self.env["asset.depreciation.line"]
        for out_line in out_lines:
            out_line.amount = min(
                dismis_amount,
                round(dep.amount_residual
                      * (min(dep_percentage, partial_dismiss_percentage) / 100),
                      digits)
            )

        # Now evaluate gain or loss
        for dep in deps:
            dep_line = dep.env["asset.depreciation.line"].get_depreciation_lines(
                date_from=dismis_date,
                date_to=dismis_date,
                depreciation_ids=dep.id,
                move_types="out",
            )[0]
            vals["depreciation_id"] = dep.id
            balance = round(dismis_amount - dep_line.amount, digits)
            vals["amount"] = abs(balance)
            if balance > 0:
                vals["move_type"] = "gain"
                vals["name"] = "Dismiss Gain"
            else:
                vals["move_type"] = "loss"
                vals["name"] = "Dismiss Loss"
            line_model.create(vals)

        return out_lines

    def generate_dismiss_line_single(self, vals, invoice_line_ids=None):
        vals.update({"move_type": "out", "name": _("Dismiss")})
        if invoice_line_ids:
            vals["asset_accounting_info_ids"] = []
            for line in invoice_line_ids:
                vals["asset_accounting_info_ids"].append(
                    (
                        0,
                        0,
                        {
                            "asset_id": vals["asset_id"],
                            "relation_type": "update",
                            "invoice_id": line.invoice_id.id,
                            "invoice_line_id": line.id,
                        },
                    )
                )
        line_model = self.env["asset.depreciation.line"]
        return line_model.with_context(depreciated_by_line=True).create(vals)

    def generate_dismiss_account_move(self):
        self.ensure_one()
        am_obj = self.env["account.move"]

        vals = self.get_dismiss_account_move_vals()
        if "line_ids" not in vals:
            vals["line_ids"] = []

        line_vals = self.get_dismiss_account_move_line_vals()
        for v in line_vals:
            vals["line_ids"].append((0, 0, v))

        self.dismiss_move_id = am_obj.create(vals)

    def get_computed_amounts(self, date_to=None, ext=None):
        """Evaluate all depreciation amounts:
        - amount_depreciated_updated: asset initial value + 'in' & 'out' lines
        - last_depreciated_date: last date with 'in' & 'out' lines (only if ext)
        - last_depreciation_date: last date of depreciation line
        - amount_depreciated: sum of 'depreciated' lines
        - amount_historical: sum of 'historical' lines
        - amount_gain: sum of 'gain' lines
        - amount_loss: sum of 'loss' lines
        - amount_in: sum of 'in' lines
        - amount_out: sum of 'out' lines
        - amount_residual: asset initial values + 'gain' & 'loss' lines
        - amount_depreciable: amount_depreciable field value (only if ext)
        """
        self.ensure_one()
        vals = {
            "amount_{}".format(k): abs(v)
            for k, v in self.line_ids.get_balances_grouped(date_to=date_to).items()
            if "amount_{}".format(k) in self._fields
        }

        amt_dep = self.amount_depreciable
        if self.asset_id.sold:
            vals.update(
                {
                    "amount_depreciable_updated": 0,
                    "amount_residual": 0,
                    "partial_dismiss_percentage": 100.0,
                }
            )
            if ext:
                vals.update(
                    {
                        "last_depreciable_date": False,
                        "amount_depreciable": amt_dep,
                    }
                )
        else:
            non_residual_types = self.line_ids.get_non_residual_move_types()
            update_move_types = self.line_ids.get_update_move_types()
            amt_residual = amt_update = percentage = 0.0
            last_depreciable_date = False
            last_depreciation_date = False
            for ln in self.line_ids:
                if date_to and ln.date > date_to:
                    continue
                if ln.move_type not in non_residual_types:
                    amt_residual += ln.balance
                if ln.move_type in update_move_types:
                    amt_update += ln.balance
                    if ln.partial_dismissal:
                        percentage += ln.partial_dismiss_percentage
                    if not last_depreciable_date or ln.date > last_depreciable_date:
                        last_depreciable_date = ln.date
                if ln.move_type == "depreciated":
                    if not last_depreciation_date or ln.date > last_depreciation_date:
                        last_depreciation_date = ln.date

            vals.update(
                {
                    "amount_depreciable_updated": amt_dep + amt_update,
                    "amount_residual": amt_dep + amt_residual,
                    "partial_dismiss_percentage": percentage,
                    "last_depreciation_date": last_depreciation_date,
                }
            )
            if ext:
                vals.update(
                    {
                        "last_depreciable_date": last_depreciable_date,
                        "amount_depreciable": amt_dep,
                    }
                )
        return vals

    def get_depreciable_amount(self, dep_date=None):
        return self.get_computed_amounts(date_to=dep_date)["amount_depreciable_updated"]

    def get_depreciation_amount(self, dep_date):
        self.ensure_one()
        zero_dep_date = self.zero_depreciation_until
        if zero_dep_date and dep_date <= zero_dep_date:
            return 0

        # Get depreciable amount, multiplier and digits
        amount = self.get_depreciable_amount(dep_date)
        multiplier = self.get_depreciation_amount_multiplier(dep_date)
        digits = self.env["decimal.precision"].precision_get("Account")
        dep_amount = round(amount * multiplier, digits)

        return min(dep_amount, self.amount_residual)

    def get_depreciation_amount_multiplier(self, dep_date):
        self.ensure_one()

        # Base multiplier
        multiplier = self.percentage / 100

        # Update multiplier from depreciation mode data
        multiplier *= self.mode_id.get_depreciation_amount_multiplier()

        # Update multiplier from pro-rata temporis
        date_start = self.date_start
        if dep_date < date_start:
            dt_start_str = fields.Date.from_string(date_start).strftime("%d-%m-%Y")
            raise ValidationError(
                _("Depreciations cannot start before {}.").format(dt_start_str)
            )

        fiscal_year_obj = self.env["account.fiscal.year"]
        fy_dep = fiscal_year_obj.get_fiscal_year_by_date(
            dep_date, company=self.company_id
        )
        last_depreciable_date = self.get_computed_amounts(
            date_to=fy_dep.date_to, ext=True
        )["last_depreciable_date"]

        if dep_date < fields.Date.from_string(fy_dep.date_to):
            # Partial depreciation
            multiplier *= self.get_pro_rata_temporis_multiplier(dep_date, "std")
        elif last_depreciable_date and last_depreciable_date != fy_dep.date_from:
            # asset with 'in' / 'out' moves
            multiplier *= self.get_pro_rata_temporis_multiplier(
                last_depreciable_date + datetime.timedelta(1), "dte"
            )
        elif self.pro_rata_temporis or self._context.get("force_prorata"):
            fy_start = fiscal_year_obj.get_fiscal_year_by_date(
                date_start, company=self.company_id
            )
            if fy_dep == fy_start:
                # If current depreciation lines within the same fiscal year in
                # which the asset was registered, compute multiplier as a
                # difference from date_dep multiplier and start_date
                # multiplier, plus 1/lapse to avoid "skipping" one day
                fy_end = fields.Date.from_string(fy_dep.date_to)
                fy_start = fields.Date.from_string(fy_dep.date_from)
                lapse = (fy_end - fy_start).days + 1
                dep_multiplier = self.get_pro_rata_temporis_multiplier(dep_date, "dte")
                start_multiplier = self.get_pro_rata_temporis_multiplier(
                    self.date_start, "dte"
                )
                multiplier *= start_multiplier - dep_multiplier + 1 / lapse
            else:
                # Otherwise, simply compute multiplier with respect to how
                # many days have passed since the beginning of the fiscal year
                multiplier *= self.get_pro_rata_temporis_multiplier(dep_date, "std")

        return multiplier

    def get_depreciation_state(self):
        self.ensure_one()
        digits = self.env["decimal.precision"].precision_get("Account")
        depreciable = self.amount_depreciable
        residual = self.amount_residual
        updated = self.amount_depreciable_updated
        if float_is_zero(depreciable, digits):
            return "non_depreciated"
        elif float_is_zero(residual, digits):
            return "totally_depreciated"
        elif float_compare(residual, updated, digits) < 0:
            return "partially_depreciated"
        else:
            return "non_depreciated"

    def get_dismiss_account_move_line_vals(self):
        self.ensure_one()
        credit_line_vals = {
            "account_id": self.asset_id.category_id.asset_account_id.id,
            "credit": self.amount_depreciated,
            "debit": 0.0,
            "currency_id": self.currency_id.id,
            "name": _("Asset dismissal: ") + self.asset_id.make_name(),
        }
        debit_line_vals = {
            "account_id": self.asset_id.category_id.fund_account_id.id,
            "credit": 0.0,
            "debit": self.amount_depreciated,
            "currency_id": self.currency_id.id,
            "name": _("Asset dismissal: ") + self.asset_id.make_name(),
        }
        return [credit_line_vals, debit_line_vals]

    def get_dismiss_account_move_vals(self):
        self.ensure_one()
        return {
            "company_id": self.company_id.id,
            "date": self.asset_id.sale_date,
            "journal_id": self.asset_id.category_id.journal_id.id,
            "line_ids": [],
            "ref": _("Asset dismissal: ") + self.asset_id.make_name(),
        }

    def get_next_depreciation_nr(self):
        self.ensure_one()
        num_lines = self.line_ids.filtered("requires_depreciation_nr")
        nums = num_lines.mapped("depreciation_nr")
        if not nums:
            nums = [0]
        return max(nums) + 1

    def get_pro_rata_temporis_dates(self, date):
        """
        Gets useful dates for pro rata temporis computations, according to
        given date, by retrieving its fiscal year.

        :param date: given date for depreciation
        :return: date objects triplet (dt_start, dt, dt_end)
            - dt_start: fiscal year first day
            - dt: given date
            - dt_end: fiscal year last day
        """
        if not date:
            raise ValidationError(
                _("Cannot compute pro rata temporis for unknown date.")
            )

        fiscal_year_obj = self.env["account.fiscal.year"]
        fiscal_year = fiscal_year_obj.get_fiscal_year_by_date(
            date, company=self.company_id
        )
        if not fiscal_year:
            date_str = fields.Date.from_string(date).strftime("%d/%m/%Y")
            raise ValidationError(_("No fiscal year defined for date {}") + date_str)

        return (
            fields.Date.from_string(fiscal_year.date_from),
            fields.Date.from_string(date),
            fields.Date.from_string(fiscal_year.date_to),
        )

    def get_pro_rata_temporis_multiplier(self, date=None, mode="std"):
        """
        Computes and returns pro rata temporis multiplier according to given
        depreciation, date, fiscal year and mode
        :param date: given date as a fields.Date string
        :param mode: string, defines how to compute multiplier. Valid values:
            - 'std': start-to-date, computes multiplier using days from fiscal
                     year's first day to given date;
            - 'dte': date-to-end, computes multiplier using days from given
                     date to fiscal year's last day
        """
        self.ensure_one()
        # if not (self.pro_rata_temporis or self._context.get('force_prorata')):
        #     return 1

        dt_start, dt, dt_end = self.get_pro_rata_temporis_dates(date)
        lapse = (dt_end - dt_start).days + 1
        if mode == "std":
            return ((dt - dt_start).days + 1) / lapse
        elif mode == "dte":
            return ((dt_end - dt).days + 1) / lapse
        elif mode:
            raise NotImplementedError(
                _("Cannot get pro rata temporis multiplier for mode `{}`").format(mode)
            )
        raise NotImplementedError(
            _("Cannot get pro rata temporis multiplier for unspecified mode")
        )

    def make_name(self):
        self.ensure_one()
        return " - ".join((self.asset_id.make_name(), self.type_id.name or ""))

    def need_normalize_first_dep_nr(self):
        self.ensure_one()

        if self.force_all_dep_nr:
            return False

        if self.force_first_dep_nr:
            if self.first_dep_nr <= 0:
                return True

        else:
            if self.first_dep_nr != 1:
                return True

        return False

    def normalize_first_dep_nr(self, force=False):
        """
        Normalize first numbered line according to `first_dep_nr` value
        :param force: if True, force normalization
        """
        force = force or self._context.get("force_normalize_first_dep_nr")
        for d in self:
            if force or d.need_normalize_first_dep_nr():
                d.onchange_normalize_first_dep_nr()
    #
    # def post_generate_depreciation_lines(self, lines=None):
    #     lines = lines or self.env["asset.depreciation.line"]
    #     lines.filtered("requires_account_move").button_generate_account_move()

    def prepare_depreciation_line_vals(self, dep_date):
        self.ensure_one()
        if dep_date is None:
            raise ValidationError(_("Cannot create a depreciation line without a date"))
        dep_amount = self._context.get("dep_amount") or 0.0
        final = self._context.get("final") or False
        dep_year = fields.Date.from_string(dep_date).year
        return {
            "asset_id": self.asset_id.id,
            "amount": dep_amount,
            "date": dep_date,
            "depreciation_id": self.id,
            "move_type": "depreciated",
            "name": _("{} - Depreciation").format(dep_year),
            "final": final,
        }

    @api.multi
    def check_current_depreciation_lines(self, dep_date):
        res = self.env["asset.depreciation.line"]
        for dep in self:
            fiscal_year = self.env["account.fiscal.year"].get_fiscal_year_by_date(
                dep_date, company=dep.company_id
            )
            date_from = dep.get_computed_amounts(date_to=fiscal_year.date_to, ext=True)[
                "last_depreciable_date"
            ]
            if date_from and date_from > fiscal_year.date_from:
                date_from = date_from + datetime.timedelta(1)
            else:
                date_from = fiscal_year.date_from
            res += dep.env["asset.depreciation.line"].get_depreciation_lines(
                date_from=date_from,
                date_to=fiscal_year.date_to,
                final=False,
                depreciation_ids=dep.id,
                company_id=dep.company_id,
            )
        return res

    @api.model
    def get_depreciations(
        self,
        date_ref=None,
        date_from=None,
        date_to=None,
        asset_ids=None,
        type_ids=None,
        with_residual=None,
        company_id=None,
    ):
        domain = self.get_depreciations_domain(
            date_ref=date_ref,
            date_from=date_from,
            date_to=date_to,
            asset_ids=asset_ids,
            type_ids=type_ids,
            with_residual=with_residual,
            company_id=company_id,
        )
        return self.search(domain)

    def get_depreciations_domain(
        self,
        date_ref=None,
        date_from=None,
        date_to=None,
        asset_ids=None,
        type_ids=None,
        with_residual=None,
        company_id=None,
    ):
        if date_ref and (date_from == "fy.date_from" or date_to == "fy.date_to"):
            fiscal_year_model = self.env["account.fiscal.year"]
            fy = fiscal_year_model.get_fiscal_year_by_date(
                date_ref, company=self.company_id
            )
            if date_from == "fy.date_from":
                date_from = fy.date_from
            if date_to == "fy.date_to":
                date_to = fy.date_to
        asset_ids = asset_ids or []
        if not isinstance(asset_ids, (list, tuple)):
            asset_ids = [asset_ids]

        type_ids = type_ids or []
        if not isinstance(type_ids, (list, tuple)):
            type_ids = [type_ids]

        domain = []

        if with_residual:
            domain.append(("amount_residual", ">", 0.0))

        if date_ref:
            domain.append(("date_start", "<", date_ref))

        if date_from:
            domain.append(("last_depreciation_date", ">=", date_from))

        if date_to:
            domain.append(("last_depreciation_date", "<=", date_to))

        if asset_ids:
            domain.append(("asset_id", "in", asset_ids))

        if type_ids:
            domain.append(("type_id", "in", type_ids))

        if company_id:
            if isinstance(company_id, int):
                domain.append(("company_id", "=", company_id))
            else:
                domain.append(("company_id", "=", company_id.id))

        return domain
