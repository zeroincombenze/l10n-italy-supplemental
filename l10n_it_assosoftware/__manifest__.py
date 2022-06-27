# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'ITA - Codici IVA Assosoftware',
    'version': '12.0.1.0.0',
    'category': 'Localization/Italy',
    'summary':
        'Aggiunge la tabella dei codici IVA assosoftware '
        'per future scambio dati con fattura elettronica',
    'author': "SHS-AV s.r.l., "
              "Odoo Community Association (OCA)",
    'website':  'https://github.com/OCA/l10n-italy/tree/12.0/'
                'l10n_it_assosoftware',
    'license': 'LGPL-3',
    'depends': ['account', 'l10n_it_account_tax_kind'],
    'data': [
        'security/ir.model.access.csv',
        'data/italy_ade_tax_assosoftware.xml',
        'views/tax_assosoftware_view.xml',
        'views/account_tax_view.xml',
    ],
    'installable': True,
}
