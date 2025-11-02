# -*- coding: utf-8 -*-

import base64
import tempfile
from odoo.modules import get_module_resource
from odoo.tests.common import SingleTransactionCase


class FatturapaCommon(SingleTransactionCase):

    def getFile(self, filename, module_name=None):
        if module_name is None:
            module_name = "l10n_it_einvoice_in"
        path = get_module_resource(module_name, "tests", "data", filename)
        with open(path) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return path, out.read()

    def create_tax_22a(self):
        AccountTax = self.env["account.tax"]
        tax_id = AccountTax.search([("description", "=", "22a")])
        if tax_id:
            return tax_id
        account_id = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_current_assets").id,
                    )
                ],
                limit=1,
            )
            .id
        )
        return AccountTax.create(
            {
                "company_id": self.env.user.company_id.id,
                "name": "22% e-bill",
                "description": "22a",
                "type_tax_use": "purchase",
                "amount_type": "percent",
                "amount": 22.0,
                "account_id": account_id,
                "refund_account_id": account_id,
                "sequence": 1,
            }
        )

    def create_tax_10a(self):
        AccountTax = self.env["account.tax"]
        tax_id = AccountTax.search([("description", "=", "10a")])
        if tax_id:
            return tax_id
        account_id = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_current_assets").id,
                    )
                ],
                limit=1,
            )
            .id
        )
        return AccountTax.create(
            {
                "company_id": self.env.user.company_id.id,
                "name": "10% e-bill",
                "description": "10a",
                "type_tax_use": "purchase",
                "amount_type": "percent",
                "amount": 10.0,
                "account_id": account_id,
                "refund_account_id": account_id,
                "sequence": 10,
            }
        )

    def create_tax_a27a(self):
        AccountTax = self.env["account.tax"]
        tax_id = AccountTax.search([("description", "=", "a27a")])
        if tax_id:
            return tax_id
        kind_id = (
            self.env["italy.ade.tax.nature"]
            .search(
                [
                    (
                        "code",
                        "=",
                        "N2.2"
                    )
                ],
                limit=1,
            )
            .id
        )
        return AccountTax.create(
            {
                "company_id": self.env.user.company_id.id,
                "name": "art. 27 regime minimi",
                "description": "a27a",
                "type_tax_use": "purchase",
                "amount_type": "percent",
                "amount": 0.0,
                "kind_id": kind_id,
            }
        )

    def create_tax_a10a(self):
        AccountTax = self.env["account.tax"]
        tax_id = AccountTax.search([("description", "=", "a10a")])
        if tax_id:
            return tax_id
        kind_id = (
            self.env["italy.ade.tax.nature"]
            .search(
                [
                    (
                        "code",
                        "=",
                        "N4"
                    )
                ],
                limit=1,
            )
            .id
        )
        return AccountTax.create(
            {
                "company_id": self.env.user.company_id.id,
                "name": "art. 10",
                "description": "a10a",
                "type_tax_use": "purchase",
                "amount_type": "percent",
                "amount": 0.0,
                "kind_id": kind_id,
            }
        )

    def create_tax_a17c2a(self):
        AccountTax = self.env["account.tax"]
        tax_id = AccountTax.search([("description", "=", "a17c2a")])
        if tax_id:
            return tax_id
        kind_id = (
            self.env["italy.ade.tax.nature"]
            .search(
                [
                    (
                        "code",
                        "=",
                        "N6.9"
                    )
                ],
                limit=1,
            )
            .id
        )
        return AccountTax.create(
            {
                "company_id": self.env.user.company_id.id,
                "name": "art. 17 comma 2",
                "description": "a17c2a",
                "type_tax_use": "purchase",
                "amount_type": "percent",
                "amount": 0.0,
                "kind_id": kind_id,
                "rc": True,
            }
        )

    def create_wt_85(self):
        WithholdingTax = self.env["withholding.tax"]
        wh_id = WithholdingTax.search([("code", "=", "850")])
        if wh_id:
            return wh_id
        return WithholdingTax.create(
            {
                "name": "850",
                "code": "850",
                "account_receivable_id": self.payable_account_id,
                "account_payable_id": self.payable_account_id,
                "journal_id": self.journal_misc.id,
                "payment_term": self.env.ref("account.account_payment_term").id,
                "rate_ids": [(0, 0, {"tax": 8.50})],
                "causale_pagamento_id": self.env.ref("l10n_it_causali_pagamento.r").id,
            }
        )

    def create_wt_115(self):
        WithholdingTax = self.env["withholding.tax"]
        wh_id = WithholdingTax.search([("code", "=", "1150")])
        if wh_id:
            return wh_id
        return WithholdingTax.create(
            {
                "name": "1150",
                "code": "1150",
                "account_receivable_id": self.payable_account_id,
                "account_payable_id": self.payable_account_id,
                "journal_id": self.journal_misc.id,
                "payment_term": self.env.ref("account.account_payment_term").id,
                "rate_ids": [(0, 0, {"tax": 11.50})],
                "causale_pagamento_id": self.env.ref("l10n_it_causali_pagamento.r").id,
            }
        )

    def create_wt_23_20q(self):
        WithholdingTax = self.env["withholding.tax"]
        wh_id = WithholdingTax.search([("code", "=", "2320q")])
        if wh_id:
            return wh_id
        return WithholdingTax.create(
            {
                "name": "2320q",
                "code": "2320q",
                "account_receivable_id": self.payable_account_id,
                "account_payable_id": self.payable_account_id,
                "journal_id": self.journal_misc.id,
                "payment_term": self.env.ref("account.account_payment_term").id,
                "rate_ids": [(0, 0, {"tax": 23.0, "base": 0.2})],
                "causale_pagamento_id": self.env.ref("l10n_it_causali_pagamento.q").id,
            }
        )

    def create_wt_4q(self):
        WithholdingTax = self.env["withholding.tax"]
        wh_id = WithholdingTax.search([("code", "=", "4q")])
        if wh_id:
            return wh_id
        return WithholdingTax.create(
            {
                "name": "4q",
                "code": "4q",
                "wt_types": "enasarco",
                "account_receivable_id": self.payable_account_id,
                "account_payable_id": self.payable_account_id,
                "journal_id": self.journal_misc.id,
                "payment_term": self.env.ref("account.account_payment_term").id,
                "rate_ids": [(0, 0, {"tax": 4.0, "base": 1.0})],
                "causale_pagamento_id": self.env.ref("l10n_it_causali_pagamento.q").id,
            }
        )

    def create_partner_with_rea(self):
        ResPartner = self.env["res.partner"]
        partner_id = ResPartner.search([("rea_code", "=", "1580695")])
        if partner_id:
            return partner_id
        return ResPartner.create(
            {
                "is_company": True,
                "name": "TIM SPA",
                "street": "Via Gaetano Negri, 1",
                "city": "Milano",
                "zip": "20123",
                "state_id": self.env.ref("base.state_it_mi").id,
                "country_id": self.env.ref("base.it").id,
                "vat": "IT00488410010",
                "supplier": True,
                "rea_office": self.env.ref("base.state_it_mi").id,
                "rea_code": "1580695",
                "rea_capital": 11677002855.10,

            }
        )

    def run_wizard(
        self,
        name,
        file_name,
        datas_fname=None,
        mode="import",
        wiz_values=None,
        module_name=None,
    ):
        module_name = module_name or "l10n_it_einvoice_in"
        datas_fname = datas_fname or file_name
        attachment = self.attach_model.create(
            {
                "name": name,
                "datas": self.getFile(file_name, module_name=module_name)[1],
                "datas_fname": datas_fname,
            }
        )
        # Test for duplicate
        attachment.onchange_datas_fname()
        attach_id = attachment.id
        if mode == "import":
            wizard = self.wizard_model.with_context(
                active_ids=[attach_id], active_model=self.attach_model_name
            ).create(wiz_values or {})
            return wizard.importFatturaPA()
        if mode == "link":
            wizard = self.wizard_link_model.with_context(
                active_ids=[attach_id], active_model=self.attach_model_name
            ).create(wiz_values or {})
            return wizard.link()

    def run_wizard_multi(self, file_name_list, module_name=None):
        if module_name is None:
            module_name = "l10n_it_rinvoice_in"
        active_ids = []
        for file_name in file_name_list:
            active_ids.append(
                self.attach_model.create(
                    {
                        "name": file_name,
                        "datas": self.getFile(file_name, module_name)[1],
                        "datas_fname": file_name,
                    }
                ).id
            )
        wizard = self.wizard_model.with_context(active_ids=active_ids).create({})
        return wizard.importFatturaPA()

    def setUp(self):
        super(FatturapaCommon, self).setUp()
        self.wizard_model = self.env["wizard.import.fatturapa"]
        self.wizard_link_model = self.env["wizard.link.to.invoice"]
        self.data_model = self.env["ir.model.data"]
        self.attach_model_name = "fatturapa.attachment.in"
        self.attach_model = self.env[self.attach_model_name]
        self.invoice_model = self.env["account.invoice"]
        self.journal_misc = self.env["account.journal"].search(
            [("type", "=", "general")]
        )[0]
        self.payable_account_id = self.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_payable").id,
                )
            ],
            limit=1,
        ).id
        self.headphones = self.env.ref("product.product_product_7_product_template")
        self.imac = self.env.ref("product.product_product_8_product_template")
        self.service = self.env.ref("l10n_it_einvoice_in.cassa_previdenziale")
        self.env.user.company_id.cassa_previdenziale_product_id = self.service.id
        self.env.user.company_id.tax_calculation_rounding_method = "round_globally"
        # Set both active and passive account rounding
        arrotondamenti_attivi_account_id = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_other_income").id,
                    )
                ],
                limit=1,
            )
            .id
        )
        arrotondamenti_passivi_account_id = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_direct_costs").id,
                    )
                ],
                limit=1,
            )
            .id
        )
        arrotondamenti_tax_id = self.env["account.tax"].search(
            [("type_tax_use", "=", "purchase"), ("amount", "=", 0.0)],
            order="sequence",
            limit=1,
        )
        self.env.user.company_id.arrotondamenti_attivi_account_id = (
            arrotondamenti_attivi_account_id
        )
        self.env.user.company_id.arrotondamenti_passivi_account_id = (
            arrotondamenti_passivi_account_id
        )
        self.env.user.company_id.arrotondamenti_tax_id = arrotondamenti_tax_id
