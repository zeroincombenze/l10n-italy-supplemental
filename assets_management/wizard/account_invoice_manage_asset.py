# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2021-22 librERP enterprise network <https://www.librerp.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class WizardInvoiceManageAsset(models.TransientModel):
    _name = "wizard.invoice.manage.asset"
    _description = "Manage Assets from Invoices"

    @api.model
    def get_default_company_id(self):
        return self.env.user.company_id

    @api.model
    def get_default_invoice_ids(self):
        return self._context.get("invoice_ids")

    asset_id = fields.Many2one("asset.asset", string="Asset")

    asset_purchase_amount = fields.Monetary(string="Purchase Amount")

    category_id = fields.Many2one(
        "asset.category",
        string="Category",
    )

    code = fields.Char(
        default="",
        string="Code",
    )

    company_id = fields.Many2one(
        "res.company",
        default=get_default_company_id,
        string="Company",
    )

    currency_id = fields.Many2one(
        "res.currency",
        readonly=True,
        related="company_id.currency_id",
        string="Currency",
    )

    depreciated_fund_amount = fields.Monetary(string="Depreciated Fund Amount")

    partial_dismiss_percentage = fields.Float(
        string="Percentage of partial dismiss",
        default=0.0,
    )

    depreciation_type_ids = fields.Many2many(
        "asset.depreciation.type", string="Depreciation Types"
    )

    dismiss_date = fields.Date(
        string="Dismiss Date",
    )

    invoice_ids = fields.Many2many(
        "account.invoice",
        default=get_default_invoice_ids,
        string="Invoices",
    )

    invoice_line_ids = fields.Many2many(
        "account.invoice.line",
        string="Invoice Lines",
    )

    is_invoice_state_ok = fields.Boolean(
        string="Invoice State",
    )

    invoice_type = fields.Selection(
        [
            ("out_invoice", "Customer Invoice"),
            ("in_invoice", "Vendor Bill"),
            ("out_refund", "Customer Credit Note"),
            ("in_refund", "Vendor Credit Note"),
            ("wrong", "Wrong"),
        ],
        string="Invoice Type",
    )

    management_type = fields.Selection(
        [
            ("create", "Create New"),
            ("update", "Update Existing"),
            ("partial_dismiss", "Partial Dismiss"),
            ("dismiss", "Dismiss Asset"),
        ],
        string="Management Type",
    )

    name = fields.Char(
        string="Name",
    )

    purchase_date = fields.Date(
        default=fields.Date.today(),
        string="Purchase Date",
    )

    used = fields.Boolean(
        string="Used",
    )

    # Mapping between invoice type and depreciation line type
    _invoice_type_2_dep_line_type = {
        "in_invoice": "purchase",
        "out_invoice": "out",
        "in_refund": "out",
        "out_refund": "in",
    }

    # Every method used in here must return an asset
    _management_type_2_method = {
        "create": lambda w: w.create_asset(),
        "dismiss": lambda w: w.dismiss_asset(),
        "partial_dismiss": lambda w: w.partial_dismiss_asset(),
        "update": lambda w: w.update_asset(),
    }

    @api.onchange("asset_id", "management_type")
    def onchange_depreciation_type_ids(self):
        if self.management_type == "update":
            if self.asset_id:
                self.depreciation_type_ids = self.asset_id.mapped(
                    "depreciation_ids.type_id"
                )
            else:
                self.depreciation_type_ids = False
        else:
            self.depreciation_type_ids = False

    @api.onchange("invoice_ids")
    def onchange_invoices(self):
        if self.invoice_ids:
            invoices = self.invoice_ids
            invoice_type = invoices[0].type

            if any([inv.type != invoice_type for inv in invoices]):
                invoice_type = "wrong"
            self.invoice_type = invoice_type

            if invoice_type in ("in_invoice", "out_refund"):
                self.management_type = "create"
            elif invoice_type in ("in_refund", "out_invoice"):
                self.management_type = "dismiss"
            else:
                self.management_type = False

            is_invoice_state_ok = False
            if all([inv.state in ("open", "paid") for inv in invoices]):
                is_invoice_state_ok = True
            self.is_invoice_state_ok = is_invoice_state_ok

            valid_account_ids = invoices.get_valid_accounts()
            self.invoice_line_ids = invoices.mapped("invoice_line_ids").filtered(
                lambda ln: (not ln.asset_accounting_info_ids and
                            ln.account_id.id in valid_account_ids.ids)
            )

    # @api.onchange("partial_dismiss_percentage", "asset_id")
    # def onchange_partial_dismiss_percentage(self):
    #     for record in self:
    #         if record.percentage > 0:
    #             record.asset_purchase_amount = (
    #                 record.asset_id.purchase_amount * record.percentage / 100
    #             )
    #         else:
    #             record.asset_purchase_amount = 0.0

    @api.multi
    def link_asset(self):
        self.ensure_one()
        self.check_pre_link_asset()

        method = self.get_management_type_2_method().get(self.management_type)
        if not method:
            raise ValidationError(
                _(
                    "Could not determine how to link invoice lines to asset"
                    " in mode `{}`."
                ).format(self.management_type)
            )
        # As written above: method defined in here must return an asset
        asset = method(self)

        if self._context.get("show_asset"):
            act_xmlid = "assets_management.action_asset"
            act = self.env.ref(act_xmlid).read()[0]
            form_xmlid = "assets_management.asset_form_view"
            form = self.env.ref(form_xmlid)
            act.update(
                {
                    "res_id": asset.id,
                    "view_id": form.id,
                    "view_mode": "form",
                    "view_type": "form",
                    "views": [(form.id, "form")],
                }
            )
            return act

        return asset

    def check_pre_create_asset(self):
        self.ensure_one()
        if not self.invoice_line_ids:
            raise ValidationError(
                _("At least one invoice line is mandatory to create" " a new asset!")
            )

        if not len(self.invoice_line_ids.mapped("invoice_id")) == 1:
            raise ValidationError(
                _("Cannot create asset if lines come from different invoices!")
            )

        valid_account_ids = self.invoice_ids.get_valid_accounts()
        if not all(
            [
                ln.account_id.id in valid_account_ids.ids
                for ln in self.invoice_line_ids
            ]
        ):
            categ_name = self.category_id.name_get()[0][-1]
            acc_name = self.category_id.asset_account_id.name_get()[0][-1]
            raise ValidationError(
                _(
                    "You need to choose invoice lines with account `{}`"
                    " if you need them to create an asset for"
                    " category `{}`!"
                ).format(acc_name, categ_name)
            )

    def check_pre_dismiss_asset(self):
        self.ensure_one()
        if not self.asset_id:
            raise ValidationError(_("Please choose an asset before continuing!"))

        valid_account_ids = self.invoice_ids.get_valid_accounts()
        self.invoice_line_ids = self.invoice_line_ids.filtered(
            lambda ln: ln.account_id.id in valid_account_ids.ids
        )

        if not self.invoice_line_ids:
            raise ValidationError(
                _("At least one invoice line is mandatory to dismiss" " an asset!")
            )

        if not len(self.invoice_line_ids.mapped("invoice_id")) == 1:
            raise ValidationError(
                _("Cannot dismiss asset if lines come from different" " invoices!")
            )

    def check_pre_link_asset(self):
        self.ensure_one()
        if len(self.invoice_line_ids.mapped("account_id")) > 1:
            raise ValidationError(_("Every invoice line must share the same account!"))

        if not self.management_type:
            raise ValidationError(_("Couldn't determine which action should be done."))

    def check_pre_partial_dismiss_asset(self):
        self.ensure_one()
        if not self.asset_id:
            raise ValidationError(_("Please choose an asset before continuing!"))

        if not self.invoice_line_ids:
            raise ValidationError(
                _("At least one invoice line is mandatory to dismiss" " an asset!")
            )

        if not len(self.invoice_line_ids.mapped("invoice_id")) == 1:
            raise ValidationError(
                _("Cannot dismiss asset if lines come from different" " invoices!")
            )

        if not all(
            [
                ln.account_id == self.asset_id.category_id.asset_account_id
                for ln in self.invoice_line_ids
            ]
        ):
            ass_name = self.asset_id.make_name()
            ass_acc = self.asset_id.category_id.asset_account_id.name_get()[0][-1]
            raise ValidationError(
                _(
                    "You need to choose invoice lines with account `{}`"
                    " if you need them to dismiss asset `{}`!"
                ).format(ass_acc, ass_name)
            )

    def check_pre_update_asset(self):
        self.ensure_one()
        if not self.asset_id:
            raise ValidationError(_("Please choose an asset before continuing!"))

        if not self.depreciation_type_ids:
            raise ValidationError(_("Please choose at least one depreciation type!"))

        if not self.invoice_line_ids:
            raise ValidationError(
                _("At least one invoice line is mandatory to update" " an asset!")
            )

        if not all(
            [
                ln.account_id == self.asset_id.category_id.asset_account_id
                for ln in self.invoice_line_ids
            ]
        ):
            ass_name = self.asset_id.make_name()
            ass_acc = self.asset_id.category_id.asset_account_id.name_get()[0][-1]
            raise ValidationError(
                _(
                    "You need to choose invoice lines with account `{}`"
                    " if you need them to update asset `{}`!"
                ).format(ass_acc, ass_name)
            )

    def create_asset(self):
        """Creates asset and returns it"""
        self.ensure_one()
        self.check_pre_create_asset()
        return self.env["asset.asset"].create(self.get_create_asset_vals())

    def dismiss_asset(self):
        """ Dismisses asset and returns it """
        self.ensure_one()
        currency = self.asset_id.currency_id
        digits = self.env["decimal.precision"].precision_get("Account")
        invoice = self.invoice_line_ids.mapped("invoice_id")
        if not self.dismiss_date:
            self.dismiss_date = self.invoice.date_invoice
        self.check_pre_dismiss_asset()
        amount = 0
        for ln in self.invoice_line_ids:
            amount += ln.currency_id.compute(ln.price_subtotal, currency)
        amount = round(amount, digits)
        vals = {
            "customer_id": invoice.partner_id.id,
            "asset_id": self.asset_id.id,
            "amount": amount,
            "date": self.dismiss_date.strftime("%Y-%m-%d")
        }
        self.env["asset.depreciation"].generate_dismiss_line(
            vals, invoice_line_ids=self.invoice_line_ids)

        vals = {
            'customer_id': invoice.partner_id.id,
            'sale_amount': amount,
            'sale_date': invoice.date,
            'sale_invoice_id': invoice.id,
            'sold': True,
            "partial_dismiss_percentage": 100.0,
        }
        self.asset_id.write(vals)

        return self.asset_id

    def get_create_asset_vals(self):
        self.ensure_one()
        purchase_amount = self.invoice_line_ids.get_asset_purchase_amount(
            currency=self.currency_id
        )
        purchase_invoice = self.invoice_line_ids.mapped("invoice_id")
        return {
            "asset_accounting_info_ids": [
                (
                    0,
                    0,
                    {"invoice_line_id": ln.id, "relation_type": self.management_type},
                )
                for ln in self.invoice_line_ids
            ],
            "category_id": self.category_id.id,
            "code": self.code,
            "company_id": self.company_id.id,
            "currency_id": self.currency_id.id,
            "name": self.name,
            "purchase_amount": purchase_amount,
            "purchase_date": self.purchase_date,
            "purchase_invoice_id": purchase_invoice.id,
            "supplier_id": purchase_invoice.partner_id.id,
            "supplier_ref": purchase_invoice.reference or "",
            "used": self.used,
        }

    def get_invoice_type_2_dep_line_type(self):
        self.ensure_one()
        return self._invoice_type_2_dep_line_type

    def get_management_type_2_method(self):
        self.ensure_one()
        return self._management_type_2_method

    def get_partial_dismiss_asset_percentage_vals(self):
        self.ensure_one()
        asset = self.asset_id
        currency = self.asset_id.currency_id
        dismiss_date = self.dismiss_date
        digits = self.env["decimal.precision"].precision_get("Account")
        percentage = self.partial_dismiss_percentage
        # purchase_amt = self.asset_purchase_amount

        # ammortamenti precedenti

        max_date = max(asset.depreciation_ids.mapped("last_depreciation_date"))
        if max_date and max_date > dismiss_date:
            raise ValidationError(
                _(
                    "Cannot dismiss an asset earlier than the last depreciation"
                    " date.\n"
                    "(Dismiss date: {}, last depreciation date: {})."
                ).format(dismiss_date, max_date)
            )

        invoice = self.invoice_line_ids.mapped("invoice_id")
        inv_num = invoice.number

        writeoff = 0
        for ln in self.invoice_line_ids:
            writeoff += ln.currency_id.compute(ln.price_subtotal, currency)
        writeoff = round(writeoff, digits)

        vals = {"depreciation_ids": []}
        for dep in asset.depreciation_ids:
            # residual = (dep.amount_residual / 100) * percentage
            # dep_writeoff = writeoff

            name = _("Partial dismissal from invoice(s) {}").format(inv_num)

            # Ammortamento totale fino a dismiss_date
            dep_amount = dep.get_depreciation_amount(dismiss_date)

            dep_year = fields.Date.from_string(dismiss_date).year
            dep_line_vals = {
                "asset_accounting_info_ids": [
                    (
                        0,
                        0,
                        {
                            "invoice_line_id": ln.id,
                            "relation_type": self.management_type,
                        },
                    )
                    for ln in self.invoice_line_ids
                ],
                "amount": dep_amount,
                "date": dismiss_date,
                "move_type": "depreciated",
                "name": _("{} - Depreciation").format(dep_year),
                "partial_dismissal": True,
                "partial_dismiss_percentage": percentage,
                "asset_id": asset.id,
            }

            dep_vals = {"line_ids": [(0, 0, dep_line_vals)]}

            # rettifica negativa
            # Valore residuo al momento della dismissione
            residual = dep.amount_residual - dep_amount

            # Valore residuo venduto / dismesso
            out_partial = residual * percentage / 100

            out_name = name + ": " + "Valore del venduto"
            # out_amount = min(out_partial, writeoff)
            out_line_vals = {
                "asset_accounting_info_ids": [
                    (
                        0,
                        0,
                        {
                            "invoice_line_id": ln.id,
                            "relation_type": self.management_type,
                        },
                    )
                    for ln in self.invoice_line_ids
                ],
                "amount": out_partial,
                "date": dismiss_date,
                "move_type": "out",
                "name": out_name,
                "partial_dismissal": True,
                "asset_id": asset.id,
            }

            dep_vals["line_ids"].append((0, 0, out_line_vals))

            # minusvalenza / plusvalenza?

            minus_amount = out_partial - writeoff
            if not float_is_zero(minus_amount, digits):
                loss_gain_name = "Minusvalenza" if minus_amount > 0 else "Plusvalenza"
                loss_gain_vals = {
                    "asset_accounting_info_ids": [
                        (
                            0,
                            0,
                            {
                                "invoice_line_id": ln.id,
                                "relation_type": self.management_type,
                            },
                        )
                        for ln in self.invoice_line_ids
                    ],
                    "amount": abs(minus_amount),
                    "date": dismiss_date,
                    "move_type": "loss" if minus_amount > 0 else "gain",
                    "name": name + ": " + loss_gain_name,
                    "partial_dismissal": True,
                    "asset_id": asset.id,
                }

                dep_vals["line_ids"].append((0, 0, loss_gain_vals))

            vals["depreciation_ids"].append((1, dep.id, dep_vals))

        return vals

    def get_update_asset_vals(self):
        self.ensure_one()
        asset = self.asset_id
        asset_name = asset.make_name()
        digits = self.env["decimal.precision"].precision_get("Account")

        grouped_invoice_lines = {}
        for ln in self.invoice_line_ids:
            inv = ln.invoice_id
            if inv not in grouped_invoice_lines:
                grouped_invoice_lines[inv] = self.env["account.invoice.line"]
            grouped_invoice_lines[inv] |= ln

        vals = {"depreciation_ids": []}
        for dep in asset.depreciation_ids.filtered(
            lambda d: d.type_id in self.depreciation_type_ids
        ):
            residual = dep.amount_residual
            balances = 0

            dep_vals = {"line_ids": []}
            for inv, lines in grouped_invoice_lines.items():
                inv_num, inv_type = inv.number, inv.type

                move_type = self.get_invoice_type_2_dep_line_type().get(inv_type)
                if not move_type:
                    raise ValidationError(
                        _(
                            "Could not retrieve depreciation line type from"
                            " invoice `{}` (type `{}`)."
                        ).format(inv_num, inv_type)
                    )

                # Compute amount and sign to preview how much the line
                # balance will be: if it's going to write off the
                # whole residual amount and more, making it become lower
                # than zero, raise error
                amount = 0
                for line in lines:
                    amount += line.currency_id.compute(
                        line.price_subtotal, dep.currency_id
                    )
                sign = 1
                if move_type in ["out", "depreciated", "historical", "sale"]:
                    sign = -1
                # Block updates if the amount to be written off is higher than
                # the residual amount
                if sign < 0 and float_compare(residual, amount, digits) < 0:
                    raise ValidationError(
                        _(
                            "Could not update `{}`: not enough residual amount"
                            " to write off invoice `{}`.\n"
                            "(Amount to write off: {}; residual amount: {}.)\n"
                            "Maybe you should try to dismiss this asset"
                            " instead?"
                        ).format(asset_name, inv_num, -amount, residual)
                    )
                balances += sign * amount

                dep_line_vals = {
                    "asset_accounting_info_ids": [
                        (
                            0,
                            0,
                            {
                                "invoice_line_id": ln.id,
                                "relation_type": self.management_type,
                            },
                        )
                        for ln in lines
                    ],
                    "amount": amount,
                    "date": inv.date,
                    "move_type": move_type,
                    "name": _("From invoice(s) ") + inv_num,
                    "asset_id": asset.id,
                }
                if move_type == "in":
                    dep_line_vals["move_type"] = "purchase"
                dep_vals["line_ids"].append((0, 0, dep_line_vals))

            if balances < 0 and residual + balances < 0:
                raise ValidationError(
                    _(
                        "Could not update `{}`: not enough residual amount to"
                        " write off.\n"
                        "(Amount to write off: {}; residual amount: {}.)\n"
                        "Maybe you should try to dismiss this asset instead?"
                    ).format(asset_name, balances, residual)
                )

            vals["depreciation_ids"].append((1, dep.id, dep_vals))

        purchase_amount = self.invoice_line_ids.get_asset_purchase_amount(
            currency=self.currency_id
        )
        purchase_invoice = self.invoice_line_ids.mapped("invoice_id")
        vals.update({
            "company_id": self.company_id.id,
            "currency_id": self.currency_id.id,
            "purchase_amount": purchase_amount,
            "purchase_date": self.purchase_date,
            "supplier_id": purchase_invoice.partner_id.id,
            "supplier_ref": purchase_invoice.reference or "",
        })

        return vals

    def partial_dismiss_asset(self):
        """Dismisses asset partially and returns it"""
        self.ensure_one()
        currency = self.asset_id.currency_id
        digits = self.env["decimal.precision"].precision_get("Account")
        invoice = self.invoice_line_ids.mapped("invoice_id")
        if not self.dismiss_date:
            self.dismiss_date = self.invoice.date_invoice
        self.check_pre_dismiss_asset()
        amount = 0
        for ln in self.invoice_line_ids:
            amount += ln.currency_id.compute(ln.price_subtotal, currency)
        amount = round(amount, digits)
        vals = {
            "customer_id": invoice.partner_id.id,
            "asset_id": self.asset_id.id,
            "amount": amount,
            "date": self.dismiss_date.strftime("%Y-%m-%d"),
            "partial_dismiss_percentage": self.partial_dismiss_percentage,
        }
        self.env["asset.depreciation"].generate_dismiss_line(
            vals, invoice_line_ids=self.invoice_line_ids)

        vals = {
            'customer_id': invoice.partner_id.id,
            'sale_amount': amount,
            'sale_date': invoice.date,
            'sale_invoice_id': invoice.id,
            'sold': True,
            "partial_dismiss_percentage": 100.0,
        }
        self.asset_id.write(vals)

        return self.asset_id

    def update_asset(self):
        """Updates asset and returns it"""
        self.ensure_one()
        self.check_pre_update_asset()
        self.asset_id.write(self.get_update_asset_vals())
        return self.asset_id
