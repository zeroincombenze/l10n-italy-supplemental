# Copyright 2022 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021-23 Didotech s.r.l. <https://www.didotech.com>
#
# License OPL-1 or later
# (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    "name": "Account RiBa CBI",
    "version": "12.0.4.5.34",
    "category": "Banking addons",
    "summary": "Gestione Ri.Ba.",
    "author": "LibrERP enterprise network and other partners",
    "website": "https://www.librerp.it",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
        "account_duedates",
        "account_payment_order",
        "account_payment_mode",
        "account_banking_common",
        "account_banking_pain_base",
        "l10n_it_fiscalcode",
        "l10n_it_validations",
    ],
    "external_dependencies": {"python": ["ribalta"]},
    "version_depends": ["account_banking_common>12.0.3.7.49"],
    "version_external_dependencies": ["ribalta>=0.4.0"],
    "data": [
        "views/res_config.xml",
        # 'views/account_payment_mode.xml',
        "data/account_payment_method.xml",
        "wizard/wizard_payment_riba_supplier.xml",
    ],
    "installable": True,
    "pre_init_hook": "check_4_depending",
}
