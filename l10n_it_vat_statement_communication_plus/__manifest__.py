# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2017-19 Lorenzo Battistini
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
# Copyright 2017-21 Odoo Community Association (OCA) <https://odoo-community.org>
#
# License OPL-1.0 or later (https://www.gnu.org/licenses/agpl).
#
{
    'name': 'ITA - Comunicazione liquidazione IVA plus',
    'version': '12.0.1.5.8',
    'category': 'Account',
    'summary': 'Comunicazione liquidazione IVA ed esportazione file xmlconforme alle specifiche dell"Agenzia delle Entrate',
    'author': 'Odoo Community Association (OCA) and other partners',
    'website': 'https://odoo-community.org',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_vat_statement',
        'l10n_it_codici_carica',
        'l10n_it_fiscalcode',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/comunicazione_liquidazione.xml',
        'views/config.xml',
        'views/account.xml',
        'wizard/export_file_view.xml',
        'security/security.xml',
    ],
    'installable': True,
}
