# Copyright 2015-2017 See manifest
# Copyright 2018 Raf Ven <raf.ven@dynapps.be>
# Copyright 2019 Akretion France (http://www.akretion.com/)
# License OPL-1 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Account Move Template',
    'version': '12.0.1.0.1',
    'category': 'Accounting',
    'summary': 'Templates for recurring Journal Entries',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'OPL-1',
    'depends': ['account'],
    'data': [
        'security/account_move_template_security.xml',
        'security/ir.model.access.csv',
        'wizard/account_move_template_run_view.xml',
        'view/account_move_template.xml',
    ],
    'installable': True,
}
