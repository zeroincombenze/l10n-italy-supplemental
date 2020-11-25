# -*- coding: utf-8 -*-
#
# Copyright 2020 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
{
    'name': 'Recovery last invoice number',
    'version': '10.0.0.1.0',
    'category': 'Localization/Italy',
    'summary': 'Decrement invoice sequence if unlink last invoice',
    'author': 'SHS-AV s.r.l.',
    'website': 'https://www.zeroincombenze.it/',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'sequence_recovery_last',
    ],
    'installable': False,
}
