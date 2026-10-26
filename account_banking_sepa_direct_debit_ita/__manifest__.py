# Copyright 2021-26 Zeroincombenze srls <https://www.zeroincombenze.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Banking Sepa Direct Debit ITA",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "summary": "SEPA Direct Debit CBI file (Italy) for payment orders",
    "author": "Zeroincombenze srls, LibrErp enterprise network and other partners",
    "website": "https://www.zeroincombenze.it",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_banking_pain_base",
        "account_banking_mandate",
        "account_banking_sepa_direct_debit",
    ],
    "external_dependencies": {"python": ["fintech"]},
    "data": [
        "data/account_payment_method.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
