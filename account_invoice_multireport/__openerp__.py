# -*- coding: utf-8 -*-
# Copyright 2016 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo Italian Community
#                Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "account_invoice_multireport",

    'summary': """Manage invoice multiple reports""",

    'description': """
(en) Manage invoice multiple reports
------------------------------------

Install this module if you wish to add your customized invoice report and set
the rules to select invoice graphical model to print, depending by:

* Journal
* Customer (some customer can have an own invoice model)
* Date (special model at specific time)
* Company
* Customer language
* Fiscal position

You can build your own customized report and add it to invoice report list.
You can find an customized invoice report example in this module.


(it) Gestisci modelli multipli di fattura
-----------------------------------------

Installate questo modulo per gestire modelli multipli di fattura basati su:

* Sezionale (utile per gestire le fatture accompagnatorie)
* Cliente (alcuni clienti posso avare la fattura persolizzata)
* Date (modelli speciali in particolai periodi dell'anno)
* Aziend
* Lingua cliente
* Posizione fiscale

Potete anche costruire un vostro modulo di fattura personalizzata da aggiungere
alla lista dei modelli.
Trovate un esempio di fattura in questo modulo.
    """,

    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",

    'category': 'Generic Modules/Accounting',
    'version': '8.0.0.2.0',

    # any module necessary for this one to work correctly
    'depends': ['account', 'sale'],

    # always loaded
    'data': ['account_invoice_multireport.xml',
             'report/header-footer.xml',
             'report/invoice-report.xml',
             'report/invoice-delivery-report.xml',
             'views/res_company_view.xml',
             'views/res_partner_view.xml',
             'views/account_invoice_view.xml',
             'views/account_invoice_reportname.xml',
             'data/account.invoice.reportname.csv',
             'security/ir.model.access.csv',
             ],
    "active": False,
    'installable': False
}
