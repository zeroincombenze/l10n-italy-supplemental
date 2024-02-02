# © 2021-2022 SHS-AV srl (www.shs-av.com)
{
    "name": "Import partner opening",
    "version": "12.0.0.1.0",
    "category": "Tools",
    "summary": "Import partner opening from Excel file",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/fatturazione-elettronica",
    "development_status": "Alpha",
    "license": "LGPL-3",
    "depends": ["base"],
    "external_dependencies": {'python': ['openpyxl']},
    "data": [
        "wizard/wizard_file_import_view.xml",
        "security/ir.model.access.csv",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
}
