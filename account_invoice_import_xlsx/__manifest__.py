# Copyright 2018-26 Zeroincombenze srls <https://www.zeroincombenze.it>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Import file Excel into invoice",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "summary": "Import invoice from Excel file",
    "author": "Zeroincombenze srls",
    "website": "https://www.zeroincombenze.it/",
    "development_status": "Alpha",
    "license": "LGPL-3",
    "depends": [
        "account",
    ],
    "external_dependencies": {
        "python": ["openpyxl", "unidecode"],
    },
    "data": [
        "security/ir.model.access.csv",
        "wizard/import_file_view.xml",
        "views/account_move_views.xml",
    ],
    "maintainer": "Antonio Maria Vigliotti",
    "installable": True,
}
