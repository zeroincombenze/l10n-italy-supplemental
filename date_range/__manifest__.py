# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License OPL-1.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Date Range',
    'version': '12.0.1.0.1',
    'category': 'Uncategorized',
    'summary': 'Manage all kind of date range',
    'author': 'powERP enterprise network, Acsone SA/NV',
    'website': 'https://www.powerp.it',
    'development_status': 'Mature',
    'license': 'OPL-1',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'security/date_range_security.xml',
        'views/assets.xml',
        'views/date_range_view.xml',
        'wizard/date_range_generator.xml',
    ],
    'installable': True,
    'maintainers': ['lmignon'],
    'qweb': ['static/src/xml/date_range.xml'],
}
