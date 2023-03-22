# -*- coding: utf-8 -*-
from odoo import http
import odoo.addons.web.controllers.main as main
from odoo.http import request, Controller
import odoo

class Home(main.Action, Controller):

    # Show Full Accounting Features to block

    MENU_ID_BLOCK = [
        'account_move_template.account_move_template_run_action',
        'account.action_move_journal_line',
        'account.action_account_moves_all_a',
        'analytic.account_analytic_line_action_entries',
        'account.action_manual_reconciliation',
        'account.tax_adjustments_form',
        'l10n_it_intrastat.view_invoice_intrastat_report_action',
        'l10n_it_intrastat_statement.account_intrastat_statement_action',
        'l10n_it_vat_statement.action_account_vat_period_end_statement',
        'account_due_list.action_invoice_payments',
        'account_payment_order.account_payment_order_inbound_action',
        'account_payment_order.bank_payment_line_action',
        'account_payment_order.account_payment_order_outbound_action',
        'account.action_account_invoice_report_all',
        'account_financial_report.action_journal_ledger_wizard',
        'account_financial_report.action_trial_balance_wizard',
        'account_financial_report.action_open_items_wizard',
        'account_financial_report.action_aged_partner_balance_wizard',
        'account_financial_report.action_vat_report_wizard',
        'account_financial_report.action_general_ledger_wizard',
        'account_tax_balance.action_open_tax_balances',
        'l10n_it_central_journal.action_giornale',
        'l10n_it_vat_registries.action_registro_iva',
        'account.actions_account_fiscal_year',
        'account.action_account_bank_journal_form',
        'account.action_account_bank_journal_form',
        'account.action_account_journal_form',
        'account.action_incoterms_tree',
        'l10n_it_vat_registries.action_account_tax_registry_form',
        'date_range.date_range_type_action',
        'date_range.date_range_generator_action',
        'base.action_currency_form',
        'account.action_account_form',
        'account.action_tax_form',
        'l10n_it_fiscal_document_type.action_view_fiscal_document_type',
        'l10n_it_fatturapa.fatturapa_related_document_type_action',
        'l10n_it_account_tax_kind.view_account_tax_kind_action',
        'account.action_account_fiscal_position_form',
        'account.action_account_type_form',
        'account.action_account_reconcile_model',
        'account_move_template.account_move_template_action',
        'l10n_it_coa_base.action_profile_account'
    ]

    @http.route('/web/action/load', type='json', auth="user")
    def load(self, *args, **kw):
        main.ensure_db()
        response = super(Home, self).load(*args, **kw)
        if response['xml_id'] in self.MENU_ID_BLOCK:
            http.request.env['license_verification'].sudo().search([]).verify_license()
        return response
