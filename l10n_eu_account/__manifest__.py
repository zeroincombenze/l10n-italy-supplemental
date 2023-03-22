# Copyright 2019-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
{
    'name': 'Transnational Account',
    'version': '12.0.0.2.6',
    'category': 'Accounting',
    'summary': 'Replace standard Odoo validation',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'OPL-1',
    'depends': [
        'account',
        'base',
    ],
    'data': [
        'views/account_view.xml',
        'report/style_invoice.xml',
        'report/report_invoice.xml',
        'report/format_report_invoice.xml',
             ],
    'installable': True,
}
