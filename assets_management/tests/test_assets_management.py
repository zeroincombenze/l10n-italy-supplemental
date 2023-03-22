# Copyright 2021-22 librERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
# The tests of this module are based on two cases; all data are in the excel file
# in data/example.xlsx
# The code of this unit tests:
# * New asset creation
# * Depreciation for 1.st year: fixed rate (asset #1) or pro-rata-temporis (asset #2)
# * Depreciation for 2.nd year
# * In / Out for asset value update
# * Full (asset #1) and partial (asset #2) dismission
#
from datetime import datetime, date
from calendar import isleap

# from odoo import fields
from odoo.tools.float_utils import float_round
from odoo.tools.safe_eval import safe_eval
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError


#################################
###### Test values to check #####
#################################
TEST_DATA = {
    "date.eoy[-2]": date(date.today().year - 2, 12, 31),
    "date.eoy[-1]": date(date.today().year - 1, 12, 31),
    "date.eoy": date(date.today().year, 12, 31),
    "asset_1_2.date.disposal": date(date.today().year, 1, 31),
    "asset_4.date.disposal": date(date.today().year, 7, 31),
    "asset_1_3.date.disposal": date(date.today().year - 2, 12, 1),
    "asset_2_4.date.disposal": date(date.today().year - 2, 10, 1),
    "cat_1.percentage": 25,
    "cat_2.percentage": 24,
    "asset_1.purchase_amount": 1000.0,
    "asset_1.sale_amount": 1400.0,
    "asset_2.purchase_amount": 2500.0,
    "asset_2.sale_amount": 3210.0,
    "asset_4.sale_amount": 525.0,
    "asset_3.down_value": 725.0,
    "asset_4.disposal_percentage": 20,
}
TEST_DATA.update(
    {
        # Asset #1 + #3 - 1.st year depreciation amount
        "asset_1.depreciation_amount[1]": float_round(
            TEST_DATA["asset_1.purchase_amount"]
            * TEST_DATA["cat_1.percentage"]
            / 200.0,
            2,
        ),
        # Asset #2 + #4 - 1.st year depreciation amount
        "asset_2.depreciation_amount[1]": float_round(
            150.82 if isleap(date.today().year - 2) else 151.23, 2
        ),
        # Asset #1 + #3 - yearly depreciation amount
        "asset_1.depreciation_amount": float_round(
            TEST_DATA["asset_1.purchase_amount"]
            * TEST_DATA["cat_1.percentage"]
            / 100.0,
            2,
        ),
        # Asset #2 + #4 - yearly depreciation amount
        "asset_2.depreciation_amount": float_round(
            TEST_DATA["asset_2.purchase_amount"]
            * TEST_DATA["cat_2.percentage"]
            / 100.0,
            2,
        ),
        # Asset #3 - asset value after down (out) value
        "asset_3.purchase_amount[-1]": float_round(
            TEST_DATA["asset_1.purchase_amount"]
            - TEST_DATA["asset_3.down_value"],
            2,
        ),
    }
)
TEST_DATA.update(
    {
        # Asset #3 - yearly depreciation amount after down (out) value
        "asset_3.depreciation_amount[-1]": float_round(
            TEST_DATA["asset_3.purchase_amount[-1]"]
            * TEST_DATA["cat_1.percentage"]
            / 100.0,
            2,
        ),
    }
)
TEST_DATA.update(
    {
        # Asset #1 - Total depreciated amount year-1
        "asset_1.amount_depreciated[-1]": float_round(
            TEST_DATA["asset_1.depreciation_amount[1]"]
            + TEST_DATA["asset_1.depreciation_amount"],
            2,
        ),
        # Asset #2 - Total depreciated amount year-1
        "asset_2.amount_depreciated[-1]": float_round(
            TEST_DATA["asset_2.depreciation_amount[1]"]
            + TEST_DATA["asset_2.depreciation_amount"],
            2,
        ),
        # Asset #3 - Total depreciated amount year-1
        "asset_3.amount_depreciated[-1]": float_round(
            TEST_DATA["asset_1.depreciation_amount[1]"]
            + TEST_DATA["asset_2.depreciation_amount"],
            2,
        ),
    }
)


class TestAssets(TransactionCase):
    def setUp(self):
        super().setUp()
        self.data_account_type_current_assets = self.env.ref(
            "account.data_account_type_current_assets"
        )
        self.data_account_type_current_liabilities = self.env.ref(
            "account.data_account_type_current_liabilities"
        )
        account_model = self.env["account.account"]
        self.account_fixed_assets = account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_fixed_assets").id,
                )
            ],
            limit=1,
        )[0]
        self.account_depreciation = account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_expenses").id,
                ),
                ("name", "ilike", "Expenses"),
            ],
        )[-1]
        self.account_depreciation.name = "Depreciations"
        self.account_fund = account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_non_current_assets").id,
                )
            ],
            limit=1,
        )[0]
        self.account_fund.name = "Asset Fund"
        self.account_gain = account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_revenue").id,
                ),
                ("name", "ilike", "Gain"),
            ],
            limit=1,
        )[0]
        self.account_loss = account_model.search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_expenses").id,
                ),
                ("name", "ilike", "Loss"),
            ],
            limit=1,
        )[0]
        self.journal = self.env["account.journal"].search([("code", "=", "ADJ")])[0]

        self.asset_category_1 = self._create_category(1)
        self.asset_category_2 = self._create_category(2)
        self.asset_1 = self._create_asset(1)
        self.asset_2 = self._create_asset(2)
        self.asset_3 = self._create_asset(3)
        self.asset_4 = self._create_asset(4)
        for year in range(date.today().year - 2, date.today().year + 1):
            self.env["account.fiscal.year"].create(
                {
                    "name": "%s" % year,
                    "date_from": date(year, 1, 1),
                    "date_to": date(year, 12, 31),
                }
            )

    # TODO> Remove before publish final code
    def tearDown(self):
        super().tearDown()
        self.env.cr.commit()  # pylint: disable=invalid-commit

    def envtest_wizard_start_by_act_name(
        self, module, action_name, default=None, ctx=None
    ):
        """Start a wizard from an action name.
        It validates the action name from xml view file, then calls envtest_wizard_start

        Example.

        XML view file:
            <record id="action_example" model="ir.actions.act_window">
                <field name="name">Example</field>
                <field name="res_model">wizard.example</field>
                [...]
            </record>

        Python code:
            act_windows = self.envtest_wizard_start_by_act_name(
                "module_example",   # Module name
                "action_example",   # Action name from xml file
            )
        """
        act_model = "ir.actions.act_window"
        act_windows = self.env[act_model].for_xml_id(module, action_name)
        return self.envtest_wizard_start(act_windows, default=default, ctx=ctx)

    def envtest_wizard_start(
        self, act_windows, default=None, ctx=None, windows_break=None
    ):
        """Start a wizard from an action.
        This function simulates web interface wizard starting; it serves to test:
        * view names
        * wizard structure
        """
        res_model = act_windows["res_model"]
        vals = default or {}
        wizard = self.env[res_model].create(vals)
        act_windows["res_id"] = wizard.id
        if isinstance(act_windows.get("context"), str):
            act_windows["context"] = safe_eval(act_windows["context"])
        if ctx:
            if isinstance(act_windows.get("context"), dict):
                act_windows["context"].update(ctx)
            else:
                act_windows["context"] = ctx
        if windows_break:
            return act_windows, wizard
        if act_windows.get("view_id"):
            self.env["ir.ui.view"].browse(act_windows["view_id"][0])
        return act_windows

    def envtest_wizard_edit(self, wizard, field, value, onchange=None):
        """Simulate view editing of a field.
        It called with triple (field_name, value, onchange function)
        This function is called by envtest_wizard_exec on web_changes parameter
        """
        setattr(wizard, field, value)
        if onchange:
            return getattr(wizard, onchange)()

    def envtest_wizard_exec(
        self,
        act_windows,
        button_name=None,
        web_changes=None,
        button_ctx=None,
        windows_break=None,
    ):
        """Simulate wizard execution from an action.
        Wizard is created by action values.
        Onchange can be called by web_changes parameter.
        At the end the <button_name> function is executed.
        It returns the wizard result or False.

        Python example:
            act_window = self.envtest_wizard_exec(
                act_window,
                button_name="do_something",
                web_changes=[
                    ("field_a_ids", [(6, 0, [value_a.id])], "onchange_field_a"),
                    ("field_b_id", self.b.id, "onchange_field_b"),
                    ("field_c", "C"),
                ],
            )
        """
        res_model = act_windows["res_model"]
        ctx = (
            safe_eval(act_windows.get("context"))
            if isinstance(act_windows.get("context"), str)
            else act_windows.get("context", {})
        )
        if isinstance(ctx.get("active_id"), int):
            wizard = self.env[res_model].with_context(ctx).browse(ctx["active_id"])
        elif ctx.get("active_id"):
            wizard = ctx["active_id"]
        elif isinstance(act_windows.get("res_id"), int):
            wizard = self.env[res_model].with_context(ctx).browse(act_windows["res_id"])
        else:
            raise (TypeError, "Invalid object/model")
        # Set default values
        for default_value in [x for x in ctx.keys() if x.startswith("default_")]:
            field = default_value[8:]
            setattr(wizard, field, ctx[default_value])
        # Get all onchange method names
        for field in wizard._onchange_methods.values():
            for method in field:
                getattr(wizard, method.__name__)()
        # Now simulate user update action
        web_changes = web_changes or []
        for args in web_changes:
            method = args[2] if len(args) > 2 else None
            self.envtest_wizard_edit(wizard, args[0], args[1], method)
            if not method and args[0] in wizard._onchange_methods:
                for method in wizard._onchange_methods[args[0]]:
                    getattr(wizard, method.__name__)()
        # Now simulate user confirmation
        button_name = button_name or "process"
        if hasattr(wizard, button_name):
            act = getattr(wizard, button_name)()
            if isinstance(act, dict) and act.get("type") != "":
                act.setdefault("type", "ir.actions.act_window_close")
                if isinstance(button_ctx, dict):
                    act.setdefault("context", button_ctx)
            if windows_break:
                return act, wizard
            return act
        if windows_break:
            return False, wizard
        return False

    def envtest_is_action(self, act_windows):
        return isinstance(act_windows, dict) and act_windows.get(
            "type", "ir.actions.act_window"
        ) in ("ir.actions.act_window", "ir.actions.client")

    #######################
    #####  Test code  #####
    #######################
    def _create_category(self, cat_nr):
        """Create category for test
        * Category #1: 25% + fixed rate + mode=material
        * Category #2: 24% + pro-rata-temporis + mode=immaterial
        """
        vals = {
            "name": "Asset category #%s" % cat_nr,
            "asset_account_id": self.account_fixed_assets.id,
            "depreciation_account_id": self.account_depreciation.id,
            "fund_account_id": self.account_fund.id,
            "gain_account_id": self.account_gain.id,
            "loss_account_id": self.account_loss.id,
        }
        if cat_nr == 1:
            vals["journal_id"] = self.env.ref(
                "assets_management.asset_account_journal"
            ).id
        category = self.env["asset.category"].create(vals)
        type_model = self.env["asset.category.depreciation.type"]
        for rec in type_model.search([("category_id", "=", category.id)]):
            rec.write(
                {
                    "percentage": TEST_DATA["cat_%s.percentage" % (2 - (cat_nr % 2))],
                    "pro_rata_temporis": (cat_nr == 2),
                    "mode_id": self.env.ref(
                        "assets_management.ad_mode_materiale"
                        if cat_nr == 1
                        else "assets_management.ad_mode_immateriale"
                    ).id,
                }
            )
        return category

    def _create_asset(self, asset_nr):
        """Create asset for test
        * Asset odd (#1 #3): 1000€ + Category #1, since 2020-12-01
        * Asset even (#2 #4): 2500€ + Category #1, since 2020-10-01 (92 days)
        """
        vals = {
            "name": "Test asset #%s" % asset_nr,
            "category_id": self.asset_category_1.id
            if (asset_nr % 2)
            else self.asset_category_2.id,
            "currency_id": self.env.ref("base.main_company").currency_id.id,
            "purchase_amount": TEST_DATA[
                "asset_%s.purchase_amount" % (2 - (asset_nr % 2))
            ],
            "purchase_date": date(date.today().year - 2, 12, 1)
            if (asset_nr % 2)
            else date(date.today().year - 2, 10, 1),
        }
        if asset_nr == 1:
            vals["company_id"] = self.env.ref("base.main_company").id
            vals["code"] = "One"
        elif asset_nr == 2:
            vals["code"] = "Two"
        return self.env["asset.asset"].create(vals)

    def get_sale_tax(self):
        return self.env["account.tax"].search(
            [
                ("type_tax_use", "=", "sale"),
                ("amount", ">", 0.0),
                ("company_id", "=", self.env.ref("base.main_company").id),
            ]
        )[0]

    def get_purchase_tax(self):
        return self.env["account.tax"].search(
            [
                ("type_tax_use", "=", "purchase"),
                ("amount", ">", 0.0),
                ("company_id", "=", self.env.ref("base.main_company").id),
            ]
        )[0]

    def set_purchase_invoice_asset_1(self):
        tax = self.get_purchase_tax()
        vals = {
            "partner_id": self.env.ref("base.res_partner_1").id,
            "type": "in_invoice",
            "date_invoice":TEST_DATA["asset_1_3.date.disposal"].strftime('%Y-%m-%d'),
            "reference": "20-012-001",
            "invoice_line_ids": [],
        }
        vals["invoice_line_ids"].append((
            0,
            0,
            {
                "name": "Asset One",
                "account_id": self.asset_1.category_id.asset_account_id.id,
                "price_unit": TEST_DATA["asset_1.purchase_amount"],
                "quantity": 1.0,
                "invoice_line_tax_ids": [(6, 0, [tax.id])],
            },
        ))
        vals["invoice_line_ids"].append((
            0,
            0,
            {
                "name": "Asset Three",
                "account_id": self.asset_1.category_id.asset_account_id.id,
                "price_unit": TEST_DATA["asset_1.purchase_amount"],
                "quantiy": 1.0,
                "invoice_line_tax_ids": [(6, 0, [tax.id])],
            },
        ))
        self.purchase_invoice = self.env["account.invoice"].create(vals)
        self.purchase_invoice.journal_id.update_posted = True  # Assure invoice cancel
        self.purchase_invoice.action_invoice_open()

    def set_purchase_invoice_asset_2(self):
        tax = self.get_purchase_tax()
        vals = {
            "partner_id": self.env.ref("base.res_partner_3").id,
            "type": "in_invoice",
            "date_invoice":TEST_DATA["asset_2_4.date.disposal"].strftime('%Y-%m-%d'),
            "reference": "20-010-001",
            "invoice_line_ids": [],
        }
        vals["invoice_line_ids"].append((
            0,
            0,
            {
                "name": "Asset Two",
                "account_id": self.asset_2.category_id.asset_account_id.id,
                "price_unit": TEST_DATA["asset_2.purchase_amount"],
                "quantity": 1.0,
                "invoice_line_tax_ids": [(6, 0, [tax.id])],
            },
        ))
        vals["invoice_line_ids"].append((
            0,
            0,
            {
                "name": "Asset Four",
                "account_id": self.asset_2.category_id.asset_account_id.id,
                "price_unit": TEST_DATA["asset_2.purchase_amount"],
                "quantiy": 1.0,
                "invoice_line_tax_ids": [(6, 0, [tax.id])],
            },
        ))
        self.purchase_invoice2 = self.env["account.invoice"].create(vals)
        self.purchase_invoice2.journal_id.update_posted = True  # Assure invoice cancel
        self.purchase_invoice2.action_invoice_open()

    def set_sale_invoice_asset_1(self):
        tax = self.get_sale_tax()
        account = self.env["account.account"].search(
            [
                ("user_type_id", "=", self.env.ref("account.data_account_type_revenue").id),
                ("company_id", "=", self.env.ref("base.main_company").id),
            ]
        )[0]
        vals = {
            "partner_id": self.env.ref("base.res_partner_18").id,
            "type": "out_invoice",
            "date_invoice":TEST_DATA["asset_1_2.date.disposal"].strftime('%Y-%m-%d'),
            "invoice_line_ids": [],
        }
        vals["invoice_line_ids"].append((
            0,
            0,
            {
                "name": "Asset One",
                "account_id": self.asset_1.category_id.asset_account_id.id,
                "price_unit": TEST_DATA["asset_1.sale_amount"],
                "quantiy": 1.0,
                "invoice_line_tax_ids": [(6, 0, [tax.id])],
            },
        ))
        vals["invoice_line_ids"].append((
            0,
            0,
            {
                "name": "Asset Two",
                "account_id": account.id,
                "price_unit": TEST_DATA["asset_2.sale_amount"],
                "quantiy": 1.0,
                "invoice_line_tax_ids": [(6, 0, [tax.id])],
            },
        ))
        self.sale_invoice = self.env["account.invoice"].create(vals)
        self.sale_invoice.journal_id.update_posted = True  # Assure invoice cancel
        self.sale_invoice.action_invoice_open()

    def set_sale_invoice_asset_2(self):
        self.sale_invoice.action_invoice_cancel()
        self.sale_invoice.action_invoice_draft()
        for line in self.sale_invoice.invoice_line_ids:
            if line.account_id != self.asset_1.category_id.asset_account_id:
                line.account_id = self.asset_1.category_id.asset_account_id.id
        self.sale_invoice.action_invoice_open()

    def set_sale_invoice_asset_4(self):
        tax = self.get_sale_tax()
        vals = {
            "partner_id": self.env.ref("base.res_partner_2").id,
            "type": "out_invoice",
            "date_invoice":TEST_DATA["asset_4.date.disposal"].strftime('%Y-%m-%d'),
            "invoice_line_ids": [],
        }
        vals["invoice_line_ids"].append((
            0,
            0,
            {
                "name": "Asset Four",
                "account_id": self.asset_1.category_id.asset_account_id.id,
                "price_unit": TEST_DATA["asset_4.sale_amount"],
                "quantiy": 1.0,
                "invoice_line_tax_ids": [(6, 0, [tax.id])],
            },
        ))
        self.sale_invoice4 = self.env["account.invoice"].create(vals)
        self.sale_invoice4.journal_id.update_posted = True  # Assure invoice cancel
        self.sale_invoice4.action_invoice_open()

    def _day_rate(self, date_from, date_to, is_leap=None):
        return ((date_to - date_from).days + 1) / (365 if not is_leap else 366)

    def _remove_depreciation_lines(self, asset=None, date_from=None):
        date_from = date_from or date(date.today().year, 1, 1)
        self._get_depreciation_lines(asset=asset, date_from=date_from).unlink()

    def _get_depreciation_lines(
        self, asset=None, move_type=None, date_from=None, date_to=None
    ):
        dep_line_model = self.env["asset.depreciation.line"]
        move_type = move_type or "depreciated"
        domain = [("move_type", "=", move_type)]
        if asset:
            domain.append(("asset_id", "=", asset.id))
        if date_from:
            if isinstance(date_from, date):
                date_from = date_from.strftime("%Y-%m-%d")
            domain.append(("date", ">=", date_from))
        if date_to:
            if isinstance(date_to, date):
                date_to = date_to.strftime("%Y-%m-%d")
            domain.append(("date", "<=", date_to))
        return dep_line_model.search(domain)

    def _check_4_move_depreciated(self, dep):
        for line in dep.move_id.line_ids:
            if line.account_id == self.account_fund:
                self.assertEqual(
                    dep.amount,
                    line.credit,
                    "Invalid credit amount for fund move %s" % dep.move_id.id,
                )
            elif line.account_id == self.account_depreciation:
                self.assertEqual(
                    dep.amount,
                    line.debit,
                    "Invalid debit amount for fund move %s" % dep.move_id.id,
                )
            else:
                raise (
                    TypeError,
                    "Invalid line account for fund move %s" % dep.move_id.id,
                )

    def _check_4_move_gain(self, dep):
        for line in dep.move_id.line_ids:
            if line.account_id == self.account_gain:
                self.assertEqual(
                    dep.amount,
                    line.credit,
                    "Invalid credit amount for gain move %s" % dep.move_id.id,
                )
            elif line.account_id == self.account_fixed_assets:
                self.assertEqual(
                    dep.amount,
                    line.debit,
                    "Invalid debit amount for gain move %s" % dep.move_id.id,
                )
            else:
                raise (
                    TypeError,
                    "Invalid line account for gain move %s" % dep.move_id.id,
                )

    def _check_4_move_out(self, dep):
        for line in dep.move_id.line_ids:
            if line.account_id == self.account_fixed_assets:
                self.assertEqual(
                    dep.amount,
                    line.credit,
                    "Invalid credit amount for out move %s" % dep.move_id.id,
                )
            elif line.account_id == self.account_loss:
                self.assertEqual(
                    dep.amount,
                    line.debit,
                    "Invalid debit amount for out move %s" % dep.move_id.id,
                )
            else:
                raise (
                    TypeError,
                    "Invalid line account for out move %s" % dep.move_id.id,
                )

    def _check_4_move(self, dep):
        if dep.move_id:
            method = "_check_4_move_%s" % dep.move_type
            if hasattr(self, method):
                return getattr(self, method)(dep)

    def _check_4_depreciation_line(
        self, date_dep, dep, asset, amount=None, depreciation_nr=None, final=None
    ):
        """Run sequential tests on single line for amount, asset_id, date, number"""
        if amount:
            self.assertEqual(
                float_round(dep.amount, 2),
                float_round(amount, 2),
                "Invalid depreciation amount!",
            )
        self.assertEqual(dep.asset_id, asset, "Invalid asset id!")
        self.assertEqual(dep.date, date_dep, "Invalid date!")
        if depreciation_nr:
            self.assertEqual(
                dep.depreciation_nr, depreciation_nr, "Invalid depreciation number!"
            )
        if final is not None:
            self.assertEqual(dep.final, final, "Invalid final flag!")
        self._check_4_move(dep)

    def _test_all_depreciation_lines(
        self,
        date_dep,
        asset,
        amount=None,
        depreciation_nr=None,
        final=None,
        no_test_ctr=None,
    ):
        """Run tests for all depreciation type values + count for moves"""
        ctr = 0
        for dep in self._get_depreciation_lines(asset=asset, date_from=date_dep):
            self._check_4_depreciation_line(
                date_dep,
                dep,
                asset,
                amount=amount,
                depreciation_nr=depreciation_nr,
                final=final,
            )
            ctr += 1
        if not no_test_ctr:
            self.assertEqual(
                ctr, len(asset.depreciation_ids), "Missed depreciation move!"
            )

    def _test_depreciation_all_assets_y2(self, final):
        """Run 1.st year test on all assets"""
        date_dep = TEST_DATA["date.eoy[-2]"]
        act_window = self._run_wizard_4_depreciation(date_dep=date_dep, final=final)
        self.assertTrue(self.envtest_is_action(act_window))
        if final:
            self.assertEqual(
                act_window["res_model"],
                "asset.generate.warning",
                "Invalid response for 'Final depreciations'",
            )
            self.envtest_wizard_exec(act_window, button_name="do_generate")
        nr = 0
        for asset in self.asset_1, self.asset_2, self.asset_3, self.asset_4:
            nr += 1
            if not final:
                self.assertEqual(
                    asset.state,
                    "partially_depreciated",
                    "Asset is not in 'partially_depreciated' state!",
                )
            self._test_all_depreciation_lines(
                date_dep,
                asset,
                amount=TEST_DATA["asset_%s.depreciation_amount[1]" % (2 - (nr % 2))],
                depreciation_nr=1,
                final=final,
            )
            for dep in asset.depreciation_ids:
                self.assertEqual(
                    float_round(dep.amount_depreciated, 2),
                    TEST_DATA["asset_%s.depreciation_amount[1]" % (2 - (nr % 2))],
                    "Invalid depreciation amount!",
                )

    def _test_depreciation_all_assets_y1(self, final):
        """Run 2.nd year test on all assets"""
        date_dep = TEST_DATA["date.eoy[-1]"]
        act_window = self._run_wizard_4_depreciation(date_dep=date_dep, final=final)
        if final:
            self.envtest_wizard_exec(act_window, button_name="do_generate")
        nr = 0
        for asset in self.asset_1, self.asset_2, self.asset_3, self.asset_4:
            nr += 1
            self._test_all_depreciation_lines(
                date_dep,
                asset,
                amount=TEST_DATA["asset_%s.depreciation_amount" % (2 - (nr % 2))],
                depreciation_nr=2,
                final=final,
            )
            for dep in asset.depreciation_ids:
                self.assertEqual(
                    float_round(dep.amount_depreciated, 2),
                    TEST_DATA["asset_%s.amount_depreciated[-1]" % (2 - (nr % 2))],
                    "Invalid depreciated amount!",
                )

    def _run_wizard_4_depreciation(
        self, date_dep=None, asset=None, final=False, windows_break=None
    ):
        date_dep = date_dep or TEST_DATA["date.eoy[-2]"]
        if asset:
            vals = {"asset_ids": [(6, 0, [asset.id])]}
        else:
            vals = {}
        web_changes = [("date_dep", datetime.strftime(date_dep, "%Y-%m-%d"))]
        if final:
            web_changes.append(("final", final))
        act_windows = self.envtest_wizard_start_by_act_name(
            "assets_management",
            "action_wizard_asset_generate_depreciation",
            default=vals,
            ctx={} if final else {"reload_window": True},
        )
        return self.envtest_wizard_exec(
            act_windows,
            button_name="do_warning",
            web_changes=web_changes,
            windows_break=windows_break,
        )

    def run_buy_asset_1_3(self):
        act_window = self.purchase_invoice.open_wizard_manage_asset()
        act_window = self.envtest_wizard_start(act_window)
        self.envtest_wizard_exec(
            act_window,
            button_name="link_asset",
            button_ctx={"show_asset": 0},
            web_changes=[
                ("invoice_ids", [(6, 0, [self.purchase_invoice.id])]),
                ("invoice_line_ids",
                 [(6, 0, [self.purchase_invoice.invoice_line_ids[0].id])]),
                ("asset_id", self.asset_1.id),
                ("management_type", "update"),
            ],
        )
        act_window = self.purchase_invoice.open_wizard_manage_asset()
        act_window = self.envtest_wizard_start(act_window)
        self.envtest_wizard_exec(
            act_window,
            button_name="link_asset",
            button_ctx={"show_asset": 0},
            web_changes=[
                ("invoice_ids", [(6, 0, [self.purchase_invoice.id])]),
                ("invoice_line_ids",
                 [(6, 0, [self.purchase_invoice.invoice_line_ids[1].id])]),
                ("asset_id", self.asset_3.id),
                ("management_type", "update"),
            ],
        )

    def run_buy_asset_2_4(self):
        act_window = self.purchase_invoice2.open_wizard_manage_asset()
        act_window = self.envtest_wizard_start(act_window)
        self.envtest_wizard_exec(
            act_window,
            button_name="link_asset",
            button_ctx={"show_asset": 0},
            web_changes=[
                ("invoice_ids", [(6, 0, [self.purchase_invoice2.id])]),
                ("invoice_line_ids",
                 [(6, 0, [self.purchase_invoice2.invoice_line_ids[0].id])]),
                ("asset_id", self.asset_2.id),
                ("management_type", "update"),
            ],
        )
        act_window = self.purchase_invoice2.open_wizard_manage_asset()
        act_window = self.envtest_wizard_start(act_window)
        self.envtest_wizard_exec(
            act_window,
            button_name="link_asset",
            button_ctx={"show_asset": 0},
            web_changes=[
                ("invoice_ids", [(6, 0, [self.purchase_invoice2.id])]),
                ("invoice_line_ids",
                 [(6, 0, [self.purchase_invoice2.invoice_line_ids[1].id])]),
                ("asset_id", self.asset_4.id),
                ("management_type", "update"),
            ],
        )

    def run_dismis_asset_1(self):
        asset = self.asset_1
        act_window = self.sale_invoice.open_wizard_manage_asset()
        act_window = self.envtest_wizard_start(act_window)
        self.envtest_wizard_exec(
            act_window,
            button_name="link_asset",
            button_ctx={"show_asset": 0},
            web_changes=[
                ("management_type", "dismiss"),
                ("invoice_ids", [(6, 0, [self.sale_invoice.id])]),
                ("asset_id", self.asset_1.id),
            ],
        )
        year = date.today().year
        dismis_date = TEST_DATA["asset_1_2.date.disposal"]
        rate = self._day_rate(date(year, 1, 1), dismis_date, is_leap=isleap(year))
        depreciation_amount = float_round(
            TEST_DATA["asset_1.depreciation_amount"] * rate, 2
        )
        depreciated_amount = float_round(
            TEST_DATA["asset_1.amount_depreciated[-1]"] + depreciation_amount, 2
        )
        self._test_all_depreciation_lines(
            dismis_date, asset, amount=depreciation_amount, depreciation_nr=3
        )
        for dep in self._get_depreciation_lines(
            asset=asset,
            move_type="out",
            date_from=dismis_date,
            date_to=dismis_date,
        ):
            down_value = float_round(
                TEST_DATA["asset_1.purchase_amount"] - depreciated_amount, 2
            )
            self.assertEqual(
                float_round(dep.amount, 2), down_value, "Invalid dismiss amount!"
            )
            self._check_4_move(dep)
        for dep in self._get_depreciation_lines(
            asset=asset,
            move_type="gain",
            date_from=dismis_date,
            date_to=dismis_date,
        ):
            down_value = float_round(
                TEST_DATA["asset_1.sale_amount"]
                - (TEST_DATA["asset_1.purchase_amount"] - depreciated_amount),
                2,
            )
            self.assertEqual(
                float_round(dep.amount, 2), down_value, "Invalid gain amount!"
            )
            self._check_4_move(dep)

    def run_dismis_asset_2(self):
        asset = self.asset_2
        act_window = self.sale_invoice.open_wizard_manage_asset()
        act_window = self.envtest_wizard_start(act_window)
        self.envtest_wizard_exec(
            act_window,
            button_name="link_asset",
            button_ctx={"show_asset": 0},
            web_changes=[
                ("management_type", "dismiss"),
                ("invoice_ids", [(6, 0, [self.sale_invoice.id])]),
                ("invoice_line_ids",
                 [(6, 0, [self.sale_invoice.invoice_line_ids[-1].id])]),
                ("asset_id", self.asset_2.id),
            ],
        )
        year = date.today().year
        dismis_date = TEST_DATA["asset_1_2.date.disposal"]
        rate = self._day_rate(date(year, 1, 1), dismis_date, is_leap=isleap(year))
        depreciation_amount = float_round(
            TEST_DATA["asset_2.depreciation_amount"] * rate, 2
        )
        depreciated_amount = float_round(
            TEST_DATA["asset_2.amount_depreciated[-1]"] + depreciation_amount, 2
        )
        self._test_all_depreciation_lines(
            dismis_date, asset, amount=depreciation_amount, depreciation_nr=3
        )
        for dep in self._get_depreciation_lines(
            asset=asset,
            move_type="out",
            date_from=dismis_date,
            date_to=dismis_date,
        ):
            down_value = float_round(
                TEST_DATA["asset_2.purchase_amount"] - depreciated_amount, 2
            )
            self.assertEqual(
                float_round(dep.amount, 2), down_value, "Invalid dismiss amount!"
            )
            self._check_4_move(dep)
        for dep in self._get_depreciation_lines(
            asset=asset,
            move_type="gain",
            date_from=dismis_date,
            date_to=dismis_date,
        ):
            down_value = float_round(
                TEST_DATA["asset_2.sale_amount"]
                - (TEST_DATA["asset_2.purchase_amount"] - depreciated_amount),
                2,
            )
            self.assertEqual(
                float_round(dep.amount, 2), down_value, "Invalid gain amount!"
            )
            self._check_4_move(dep)

    def _test_asset_1(self):
        # Basic test #1
        #
        # We test 3 years depreciations of 1000.0€ asset #1:
        # Test (setup)   : Test (A1)          | Test (A2)         | Test (A3)
        # (year-2)-10-01 : (year-2)-12-31     | (year-1)-12-31    | Today
        # start -> 1000€ : depr.50% -> 125.0€ | depr.100% -> 250€ | depr -> 0..250.0€
        #
        asset = self.asset_1
        #
        # (A1) Year #1: Generate 50% depreciation -> 1000.00€ * 25% * 50% = 125.0€
        # Depreciation for year-2 is run before starting this test
        #
        #
        # (A2) Year #2: Depreciation amount is 250€ (1000€ * 25%)
        # Depreciation for year-1 is run before starting this test
        #
        # (A3) Year #3: Current depreciation amount depends on today
        date_dep = date.today()
        year = date_dep.year
        rate = self._day_rate(date(year, 1, 1), date_dep, is_leap=isleap(year))
        self._run_wizard_4_depreciation(date_dep=date_dep, asset=asset)
        depreciation_amount = float_round(
            TEST_DATA["asset_1.depreciation_amount"] * rate, 2
        )
        depreciated_amount = float_round(
            TEST_DATA["asset_1.amount_depreciated[-1]"] + depreciation_amount, 2
        )
        self._test_all_depreciation_lines(
            date_dep,
            asset,
            amount=depreciation_amount,
            depreciation_nr=3,
            final=False,
        )
        for dep in asset.depreciation_ids:
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                depreciated_amount,
                "Invalid depreciated amount!",
            )
        #
        # (A3.b) Year #3: Repeat depreciation and prior data will be removed
        date_dep = TEST_DATA["date.eoy"]
        self._run_wizard_4_depreciation(date_dep=date_dep, asset=asset)
        depreciation_amount = TEST_DATA["asset_1.depreciation_amount"]
        depreciated_amount = float_round(
            TEST_DATA["asset_1.amount_depreciated[-1]"] + depreciation_amount, 2
        )
        self._test_all_depreciation_lines(
            date_dep,
            asset,
            amount=depreciation_amount,
            depreciation_nr=3,
            final=False,
        )
        for dep in asset.depreciation_ids:
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                depreciated_amount,
                "Invalid depreciated amount!",
            )
        #
        # (A3.c) Year #3: Repeat depreciation
        # One day depreciation -> 1000.00€ * 25% * / 365 = 0,68€
        date_dep = date(year, 1, 1)
        rate = self._day_rate(date(year, 1, 1), date_dep, is_leap=isleap(year))
        self._run_wizard_4_depreciation(date_dep=date_dep, asset=asset)
        depreciation_amount_1day = float_round(
            TEST_DATA["asset_1.depreciation_amount"] * rate, 2
        )
        depreciated_amount = float_round(
            TEST_DATA["asset_1.amount_depreciated[-1]"] + depreciation_amount_1day,
            2,
        )
        self._test_all_depreciation_lines(
            date_dep,
            asset,
            amount=depreciation_amount_1day,
            depreciation_nr=3,
            final=False,
        )
        for dep in asset.depreciation_ids:
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                depreciated_amount,
                "Invalid depreciated amount!",
            )
        #
        # (A4) Special test: cannot generate depreciation on (year-2)
        date_dep = TEST_DATA["date.eoy[-2]"]
        with self.assertRaises(ValidationError):
            self._run_wizard_4_depreciation(date_dep=date_dep, asset=asset)
        #
        # (A9) Dismiss
        self.set_sale_invoice_asset_1()
        self.run_dismis_asset_1()

    def _test_asset_2(self):
        # Basic test #2
        #
        # We test 3 years depreciations of 2500.0€ asset #2:
        # Test (setup)   : Test (B1)         | Test (B2)         | Test (B3)
        # (year-2)-10-01 : (year-2)-12-31    | (year-1)-12-31    | Today
        # start -> 2500€ : 92/365 -> 150.82€ | depr.100% -> 600€ | depr -> 0..600.0€
        #
        asset = self.asset_2
        #
        # (B1) Year #1: Generate 92 days depreciation -> 2500.00€ * 24% * 92 / 365 = 151.23€
        # If year-2 is leap depreciation value is 150.82€
        # Depreciation for year-2 is run before starting this test
        #
        # (B2) Year #2: Depreciation amount is 600€ (2500€ * 24%)
        # Depreciation for year-1 is run before starting this test
        #
        # (B3) Year #3: Current depreciation amount depends on today: value is <= 600€
        date_dep = date.today()
        year = date_dep.year
        rate = self._day_rate(date(year, 1, 1), date_dep, is_leap=isleap(year))
        self._run_wizard_4_depreciation(date_dep=date_dep, asset=asset)
        depreciation_amount = float_round(
            TEST_DATA["asset_2.depreciation_amount"] * rate, 2
        )
        depreciated_amount = float_round(
            TEST_DATA["asset_2.amount_depreciated[-1]"] + depreciation_amount, 2
        )
        self._test_all_depreciation_lines(
            date_dep,
            asset,
            amount=depreciation_amount,
            depreciation_nr=3,
            final=False,
        )
        for dep in asset.depreciation_ids:
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                depreciated_amount,
                "Invalid depreciated amount!",
            )
        #
        # (B9) Dismiss
        self.set_sale_invoice_asset_2()
        self.run_dismis_asset_2()
        #
        # In order to run dismission tests on asset #2 we used the same sale invoice
        # We set invoice state to cancel and this action unlinked asset #1 from invoice
        # So now we have to relink line #2 of invoice to asset #1
        # (A9.b) Check for deleted out & ganin lines
        dismis_date = TEST_DATA["asset_1_2.date.disposal"]
        self.assertFalse(
            self._get_depreciation_lines(
                asset=self.asset_1,
                move_type="out",
                date_from=dismis_date,
                date_to=dismis_date
            ),
            "Found out undelede out moves"
        )
        self.assertFalse(
            self._get_depreciation_lines(
                asset=self.asset_1,
                move_type="gain",
                date_from=dismis_date,
                date_to=dismis_date
            ),
            "Found out undelede out moves"
        )
        self.run_dismis_asset_1()

    def _test_asset_3(self):
        # Out + Dismiss tests asset #3 (that is #1 copy)
        #
        # Current depreciable amount is 1000.0€ * 25% = 250.0€
        # Prior test (A1) | Test (C3) 90-91 days : Test (C2)      : (C4) 275 days
        # (year-2)-03-31  | (year-1)-03-31       : (year-1)-03-31 : (year-1)-12-31
        #                 | Depr.ble = 250.0€    : Depr.ble amt 275.0€ * 25% = 68.75€
        # depr. 125.0€    | depr -> 61.64€       : 'out' -> -725€ : depr -> 51.80€
        #
        # (C2) Asset #1, year #2: depreciation moves removed, then value will be reduced
        asset = self.asset_3
        #
        # (C1) Year #1: Generate 50% depreciation -> 1000.00€ * 25% * 50% = 125.0€
        # Depreciation for year-2 is run before starting this test
        #
        #
        # (C2) Year #2: we have to repeat test for thi year
        #
        year = date.today().year - 1
        date_dep = date(year, 3, 31)
        self._remove_depreciation_lines(asset=asset, date_from=date(year, 1, 1))
        down_value = TEST_DATA["asset_3.down_value"]
        dep_line_model = self.env["asset.depreciation.line"]
        for dep in asset.depreciation_ids:
            vals = {
                "amount": down_value,
                "asset_id": asset.id,
                "depreciation_line_type_id": self.env.ref(
                    "assets_management.adpl_type_sva"
                ).id,
                "date": date_dep.strftime("%Y-%m-%d"),
                "depreciation_id": dep.id,
                "move_type": "out",
                "type_id": dep.type_id.id,
                "name": "Asset loss",
            }
            dep_line_model.with_context(depreciated_by_line=True).create(vals)
            self.assertEqual(
                float_round(dep.amount_depreciable_updated, 2),
                float_round(TEST_DATA["asset_1.purchase_amount"] - down_value, 2),
                "Invalid asset updated value!",
            )
        # (C3) Now check for depreciation amount, 90 or 91 days (leap year)
        rate = self._day_rate(date(year, 1, 1), date_dep, is_leap=isleap(year))
        depreciation_amount = float_round(
            TEST_DATA["asset_1.depreciation_amount"] * rate, 2
        )
        depreciated_amount = float_round(
            TEST_DATA["asset_1.depreciation_amount[1]"] + depreciation_amount, 2
        )
        self._test_all_depreciation_lines(
            date_dep,
            asset,
            amount=depreciation_amount,
            depreciation_nr=2,
            final=False,
        )
        for dep in asset.depreciation_ids:
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                depreciated_amount,
                "Invalid depreciated amount!",
            )
        for dep in self._get_depreciation_lines(
            asset=asset,
            move_type="out",
            date_from=date_dep,
            date_to=date_dep,
        ):
            self.assertEqual(
                float_round(dep.amount, 2),
                down_value,
                "Invalid out amount!"
            )
            self._check_4_move(dep)
        #
        # (C4) Now we do an end of year depreciation
        date_dep = TEST_DATA["date.eoy[-1]"]
        self._run_wizard_4_depreciation(date_dep=date_dep)
        rate = self._day_rate(date(year, 4, 1), date_dep, is_leap=isleap(year))
        depreciation_amount = float_round(
            TEST_DATA["asset_3.depreciation_amount[-1]"] * rate, 2
        )
        depreciated_amount = float_round(
            depreciated_amount + depreciation_amount, 2
        )
        self._test_all_depreciation_lines(
            date_dep,
            asset,
            amount=depreciation_amount,
            depreciation_nr=3,
            final=False,
        )
        for dep in asset.depreciation_ids:
            self.assertEqual(
                float_round(dep.amount_depreciated, 2),
                depreciated_amount,
                "Invalid depreciated amount!",
            )
        return


        #
        # Dismis Asset #1 price 150.0€
        # Current depreciable amount is 275.0€ * 25% = 68.75€
        # Prior test (C4) | Test (C5) 31 days : Test (C6)        : (C7)
        # (year-1)-12-31  | (year-1)-01-31    : (year-1)-01-31   : (year-1)-01-31
        # Residual 36.56€ | depr -> 5.84€     : 'out' -> -30.72€ : gain -> 119.28€
        #
        dismis_date = TEST_DATA["asset_1_2.date.disposal"]
        rate = self._day_rate(date(year, 1, 1), dismis_date, is_leap=isleap(year))
        depreciation_amount = float_round(
            TEST_DATA["asset_1.depreciation_amount"]
            * rate
            * (TEST_DATA["cat_1.percentage"] / 100),
            2,
        )
        vals = {
            "amount": 150.0,
            "asset_id": asset.id,
            "date": dismis_date.strftime("%Y-%m-%d"),
        }
        self.env["asset.depreciation"].generate_dismiss_line(vals)
        # (C5) Dismiss asset on 2022-01-31, depreciation amount, 31 days
        # 68.75€ * 31 / 365 * 25% = 5.84€ or 68.75€ * 31 / 366 * 25% = 5.82€
        self._test_all_depreciation_lines(
            wiz.date_dep,
            asset,
            amount=depreciation_amount,
            depreciation_nr=4,
            no_test_ctr=True,
        )
        self.assertEqual(
            asset.state, "totally_depreciated", "Asset is not in non depreciated state!"
        )
        # (C6)
        dep_amount = float_round(dep_residual - depreciation_amount, 2)
        for dep in self._get_depreciation_lines(
            asset=asset, date_from=wiz.date_dep, move_type="out"
        ):
            self._check_4_depreciation_line(wiz, dep, asset, amount=dep_amount)
        # (C7)
        dep_amount = float_round(150.0 - depreciation_amount, 2)
        for dep in self._get_depreciation_lines(
            asset=asset, date_from=wiz.date_dep, move_type="gain"
        ):
            self._check_4_depreciation_line(wiz, dep, asset, amount=dep_amount)

    def _test_asset_4(self):
        # Partial Dismiss tests asset #4 (that is #2 copy)
        #
        # Current depreciable amount is 2500.0€ * 24% = 600.0€
        # We test 3 years depreciations of 2500.0€
        # Residual 2.500€ (initial) - 150.82€ (1.depr) - 600€ (2.nd depr) = 1749.18€
        # Prior test (B2)     | Test (D3): dismis 20% for 500€
        # (year-1)-12-31      | (year)-07-31
        # depr.100% -> 600€   | Depr.amt 600€ * 24% * 212 / 365 = 348.49€
        # Residual = 1749.18€ | Residual = 1749.18€ - 348.49€ = 1400.69€
        # Rate 20% fo dismis -> 1400.69€ * 20% = 280.14€
        # Sale price: 500€ -> Gain 500€ - 280.14€ = 219.86€
        asset = self.asset_4
        self.set_sale_invoice_asset_4()
        act_window = self.sale_invoice4.open_wizard_manage_asset()
        act_window = self.envtest_wizard_start(act_window)
        self.envtest_wizard_exec(
            act_window,
            button_name="link_asset",
            button_ctx={"show_asset": 0},
            web_changes=[
                ("invoice_ids", [(6, 0, [self.sale_invoice4.id])]),
                ("invoice_line_ids",
                 [(6, 0, [x.id for x in self.sale_invoice4.invoice_line_ids])]),
                ("asset_id", self.asset_4.id),
                ("management_type", "partial_dismiss"),
                ("partial_dismiss_percentage",
                 TEST_DATA["asset_4.disposal_percentage"]),
            ],
        )
        year = date.today().year
        dismis_date = TEST_DATA["asset_4.date.disposal"]
        rate = self._day_rate(date(year, 1, 1), dismis_date, is_leap=isleap(year))
        depreciation_amount = float_round(
            TEST_DATA["asset_2.depreciation_amount"] * rate, 2
        )
        depreciated_amount = float_round(
            TEST_DATA["asset_2.amount_depreciated[-1]"] + depreciation_amount, 2
        )
        # (D3)
        self._test_all_depreciation_lines(
            dismis_date, asset, amount=depreciation_amount, depreciation_nr=3
        )
        for dep in self._get_depreciation_lines(
            asset=asset,
            move_type="out",
            date_from=dismis_date,
            date_to=dismis_date,
        ):
            down_value = float_round(
                (TEST_DATA["asset_2.purchase_amount"] - depreciated_amount)
                * TEST_DATA["asset_4.disposal_percentage"] / 100, 2
            )
            self.assertEqual(
                float_round(dep.amount, 2), down_value, "Invalid dismiss amount!"
            )
            self._check_4_move(dep)
        for dep in self._get_depreciation_lines(
            asset=asset,
            move_type="gain",
            date_from=dismis_date,
            date_to=dismis_date,
        ):
            down_value = float_round(
                TEST_DATA["asset_4.sale_amount"]
                - (TEST_DATA["asset_2.purchase_amount"] - depreciated_amount)
                * TEST_DATA["asset_4.disposal_percentage"] / 100,
                2,
            )
            self.assertEqual(
                float_round(dep.amount, 2), down_value, "Invalid gain amount!"
            )
            self._check_4_move(dep)

    def _test_asset_8(self):
        # Wizard tests
        #
        # Delete all records
        self._remove_depreciation_lines()
        self._test_depreciation_all_assets_y2(True)

        # Now we search for last invoice recorded
        invs = self.env["account.invoice"].search(
            [("type", "=", "out_invoice")], order="number"
        )
        invoice = invs[0]
        invoice.journal_id.update_posted = True  # Assure invoice cancel
        invoice.action_invoice_cancel()
        invoice.action_invoice_draft()
        for line in invoice.invoice_line_ids:
            line.account_id = self.asset_1.category_id.asset_account_id.id
            break
        year = date.today().year - 1
        invoice.date_invoice = date(year, 12, 31)
        invoice.action_invoice_open()
        act_window = invoice.open_wizard_manage_asset()
        act_window = self.envtest_wizard_start(act_window)
        self.envtest_wizard_exec(
            act_window,
            button_name="link_asset",
            button_ctx={"show_asset": 0},
            web_changes=[
                ("management_type", "dismiss"),
                ("invoice_ids", [(6, 0, [invoice.id])]),
                ("asset_id", self.asset_1.id),
            ],
        )

    def _test_asset_9(self):
        # Special final tests
        #
        # Check for journal unlink is impossible when journal use in asset
        with self.assertRaises(UserError):
            self.journal.unlink()
        self.assertEqual(
            self.journal.id,
            self.env.ref("assets_management.asset_account_journal").id,
            "Invalid asset journal",
        )

    def test_asset(self):
        self.set_purchase_invoice_asset_1()
        self.set_purchase_invoice_asset_2()
        for asset in self.asset_1, self.asset_2, self.asset_3:
            self.assertEqual(
                asset.state, "non_depreciated", "Asset is not in non depreciated state!"
            )
        self.run_buy_asset_1_3()
        self.run_buy_asset_2_4()
        self._test_depreciation_all_assets_y2(False)
        self._test_depreciation_all_assets_y2(True)
        self._test_depreciation_all_assets_y1(False)
        self._test_asset_1()
        self._test_asset_2()
        self._test_asset_3()
        self._test_asset_4()
        # self._test_asset_8()
        # self._test_asset_9()
