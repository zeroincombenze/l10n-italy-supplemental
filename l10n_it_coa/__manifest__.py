# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Italy - Chart of Accounts (Zeroincombenze)',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations/Account Charts',
    'countries': ['it'],
    'summary': "Piano dei conti italiano (CoA) per Odoo 18.0",
    'description': """
Italian Chart of Accounts - l10n_it_coa
=======================================

Piano dei conti italiano completo basato sullo schema CEE/Zeroincombenze,
migrato e aggiornato alla struttura di Odoo 18.0.

Contenuto:
----------
* Piano dei conti (account.account) con i tipi conto (account_type) di Odoo 18.0
* Gruppi conto gerarchici (account.group) con prefissi di codice
* Gruppi IVA (account.tax.group) nazionali e EU-OSS
* Imposte IVA (account.tax) con repartition lines (struttura Odoo 18.0)
* Posizioni fiscali (account.fiscal.position) inclusi i regimi EU-OSS

Le imposte sono state convertite dalla vecchia struttura di Odoo 10.0
(campi `type`, `account_id`, `refund_account_id`) alla nuova struttura di
Odoo 18.0 basata su `type_tax_use` e `repartition_line_ids`.
    """,
    'author': 'Zeroincombenze, migrated to Odoo 18.0',
    'website': 'https://www.zeroincombenze.it',
    'depends': [
        'account',
        'base_iban',
        'base_vat',
        # OCA module providing extended account group features used by this CoA.
        'account_usability',
    ],
    'data': [],
    'license': 'LGPL-3',
    'installable': True,
}
