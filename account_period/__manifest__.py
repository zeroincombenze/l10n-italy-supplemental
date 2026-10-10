# -*- coding: utf-8 -*-
# Copyright 2017 Jarvis (www.odoomod.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Period",
    "summary": "Account Period",
    "version": "10.0.0.1.0",
    "category": "Accounting",
    "website": "https://github.com/OCA/l10n-italy",
    "description": """
Account Period
""",
    "author": "Jarvis (www.odoomod.com)",
    "license": "AGPL-3",
    "depends": [
        "account",
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "data": [
        "security/account_security.xml",
        "security/ir.model.access.csv",
        "views/account_menuitem.xml",
        "views/account_views.xml",
        "views/account_end_fy.xml",
    ],
    "qweb": [],
    "demo": [],
    "css": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
