# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
{
    'name': 'Assets Management Plus',
    'version': '12.0.1.0.9',
    'category': 'Accounting & Finance',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'assets_management',
        # 'account_asset_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/asset.xml',
        'views/asset_asset_service.xml',
        'views/asset_depreciation_deduction.xml',
        'data/asset_asset_service_data.xml',
        'data/asset_depreciation_deduction_data.xml',
        'views/asset_depreciation_line.xml',
    ],
    'installable': True,
}
