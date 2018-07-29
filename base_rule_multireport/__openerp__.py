# -*- coding: utf-8 -*-
# Copyright 2016-2018 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                     Odoo Italia Associazione
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "base_rule_multireport",

    'summary': """Manage dcocuments multiple reports""",

    'description': """
(en) Manage document multiple reports
-------------------------------------

Install this module if you wish to set rules to selecr
graphical document model to print, depending by:

* Journal
* Customer (some partner can have the own document model)
* Date (special model at specific time)
* Company
* Partner language
* Fiscal position
* Team

You can build your own customized report and add it to document report list.
You can find an customized invoice report example in this module.


(it) Gestisci modelli di stampa multipli
----------------------------------------

Installate questo modulo per stampare modelli multipli di documenti basati su:

* Sezionale (utile per gestire le fatture accompagnatorie)
* Partner (alcuni partner posso avare documenti persolizzati)
* Date (modelli speciali in particolai periodi dell'anno)
* Azienda
* Lingua partner
* Posizione fiscale
* Team

Potete anche costruire un vostro modulo di fattura personalizzata da aggiungere
alla lista dei modelli.
Trovate un esempio di fattura in questo modulo.
    """,

    'author': "SHS-AV s.r.l.",
    'website': "https://www.zeroincombenze.it/",

    'category': 'Generic Modules/Accounting',
    'version': '8.0.0.2.0',

    # any module necessary for this one to work correctly
    'depends': ['account',
                'sale',
                'purchase'],

    # always loaded
    'data': [
        # 'views/base_rule_reportname_view.xml'
        # 'data/base_rule.reportname.csv',
        # 'rule_multireport.xml',
        'report/header-footer.xml',
        # 'report/invoice-report.xml',
        # 'report/invoice-delivery-report.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        # 'views/account_invoice_view.xml',
        # 'security/ir.model.access.csv',
    ],
    'installable': True
}
