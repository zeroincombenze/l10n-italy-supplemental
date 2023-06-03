# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    "name": "Account Banking Common",
    "version": "12.0.3.7.50",
    "category": "Accounting",
    "summary": "Common stuff for payment modules",
    "author": "powERP enterprise network and other partners",
    "website": "https://www.powerp.it",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_due_list",
        "account_duedates",
        "account_payment_order",
        "account_payment_method",
        "account_common_mixin",
        "l10n_it_coa_base",
        "l10n_it_fiscalcode",
    ],
    "data": [
        "views/res_partner_bank_view.xml",
        "wizard/wizard_insoluto.xml",
        "wizard/wizard_payment_order_confirm.xml",
        "wizard/wizard_payment_order_credit.xml",
        "wizard/wizard_payment_order_generate.xml",
        "wizard/wizard_payment_order_add_move_lines.xml",
        "wizard/wizard_set_payment_method.xml",
        "wizard/wizard_account_compensation_generate.xml",
        "wizard/wizard_account_register_payment.xml",
        "views/account_payment_order.xml",
        "views/action_order_generate.xml",
        "views/account_bank_journal_form.xml",
        "views/account_invoice_view.xml",
        "views/account_move_line_view.xml",
        "views/res_config_settings.xml",
    ],
    "maintainer": "powERP enterprise network",
    "installable": True,
}
