# -*- coding: utf-8 -*-

from odoo import models, _


class AccountTax(models.Model):
    _inherit = "account.tax"

    def search_tax_by_code_kind(
        self,
        company_id,
        tax_rate_int,
        tax_kind,
        partner=None,
        type_tax_use="purchase",
    ):
        """Tax matching rate and nature of an e-invoice line.

        type_tax_use tells apart a received bill ("purchase", the default and
        the historical behaviour) from an issued invoice ("sale"), imported by
        l10n_it_einvoice_import.
        """
        TaxNature = self.env["italy.ade.tax.nature"]
        IrValues = self.env["ir.values"]
        tax_rate = float(tax_rate_int)
        default_field = (
            "taxes_id" if type_tax_use == "sale" else "supplier_taxes_id"
        )
        default_taxes_ids = IrValues.get_default(
            "product.product", default_field, company_id=company_id
        )
        def_purchase_tax = False
        # Reverse charge is a purchase-side mechanism: on a sale invoice the
        # nature (N6) rides on an ordinary sale tax
        is_rc = False if type_tax_use == "sale" else self.is_rc(nature=tax_kind)
        default_tax = self.search(
            [("type_tax_use", "=", type_tax_use),
             ("amount", "!=", 0.0)], limit=1, order="sequence,id")
        if default_taxes_ids:
            def_purchase_tax = self.browse(default_taxes_ids)[0]
        domain = []
        domain.append(("company_id", "=", company_id))
        domain.append(("type_tax_use", "=", type_tax_use))
        if tax_rate != 0.0:
            domain.append(("amount", "=", tax_rate))
        elif is_rc and default_tax:
            # Some supplier use N6 w/o Vax rate!
            domain.append("|")
            domain.append(("amount", "=", default_tax[0].amount))
            domain.append(("amount", "=", 0.0))
        domain.append(("rc", "=", is_rc))
        if tax_kind:
            if "." not in tax_kind:
                # Code 2020
                kind_ids = TaxNature.search([("code", "like", tax_kind)])
                if kind_ids:
                    domain.append(("kind_id", "in", [x.id for x in kind_ids]))
            else:
                kind_id = TaxNature.search([("code", "=", tax_kind)])
                if kind_id:
                    domain.append(("kind_id", "=", kind_id.id))
        account_taxes = self.search(domain, order="sequence")
        errmsg = ""
        if not account_taxes:
            errmsg = (
                _("Nessun codice IVA con aliquota " "%s e natura %s. Inserirne uno.")
                % (tax_rate_int, tax_kind)
            )
        if len(account_taxes) > 1:
            if (
                    partner
                    and partner.register_fiscalpos.code == "RF19"
                    and tax_kind == "N2"
            ):
                domain.append(("name", "ilike", "%190%"))
                account_taxes2 = self.search(domain, order="sequence")
                if len(account_taxes2):
                    account_taxes = account_taxes2
        if len(account_taxes) > 1:
            errmsg = (
                _(
                    "Rilevati troppi codici IVA con aliquota %s "
                    "e natura %s. Eventualmente selezionare il codice corretto."
                )
                % (tax_rate_int, tax_kind)
            )
        if def_purchase_tax and def_purchase_tax.amount == tax_rate:
            account_tax_id = def_purchase_tax.id
        elif account_taxes:
            account_tax_id = account_taxes[0].id
        else:
            account_tax_id = False
        return account_tax_id, errmsg
