# Copyright 2019 Simone Rubino - Agile Business Group
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-2021 Odoo Community Association (OCA) <https://odoo-community.org>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
{
    'name': 'ITA - Dichiarazione Intrastat Plus',
    'version': '12.0.1.2.4_13',
    'category': 'Account',
    'summary': 'Dichiarazione Intrastat Plus per l"Agenzia delle Dogane',
    'author': 'Odoo Community Association (OCA) and other partners',
    'website': 'https://odoo-community.org',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_costs_allocation',
        'l10n_it_intrastat_plus',
    ],
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'wizard/export_file_view.xml',
        'views/config.xml',
        'views/intrastat.xml',
        'report/report_intrastat_mod1.xml',
        'report/intrastat_mod1_bis.xml',
        'report/intrastat_mod1_ter.xml',
        'report/report_intrastat_mod2.xml',
        'report/report_intrastat_mod2_bis.xml',
        'report/reports.xml',
    ],
    'installable': True,
    'pre_init_hook': 'pre_init_hook',
}
