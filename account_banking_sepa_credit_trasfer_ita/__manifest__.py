# Copyright 2022-26 Zeroincombenze srls <https://www.zeroincombenze.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account SEPA Credit Transfer ITA CBI",
    "version": "18.0.1.0.0",
    "category": "Banking addons",
    "summary": "SEPA Credit Transfer CBI file (Italy) for payment orders",
    "author": "Zeroincombenze srls, Librerp and other partners",
    "website": "https://www.zeroincombenze.it",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_banking_pain_base",
    ],
    "external_dependencies": {"python": ["fintech"]},
    "data": [
        "data/account_payment_method.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
