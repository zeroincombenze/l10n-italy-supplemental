# © 2021 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Italian localization - l10n_it_fatturapa_in_improved',
    'version': '12.0.0.3.5',
    'category': 'Localisation/Italy',
    'summary': 'Corrections to official l10n_it_fatturapa_in',
    'author': 'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'l10n_it_fatturapa_in',
    ],
    'data': [
        'views/attachment_view.xml',
        'views/res_partner_view.xml',
    ],
    'demo': ['demo/demo.xml'],
}
