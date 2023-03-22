# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2021 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2021 Didotech s.r.l. <https://www.didotech.com>
# Copyright 2021 Odoo Community Association (OCA) <https://odoo-community.org>
#
import logging
from odoo import api, SUPERUSER_ID
from odoo.exceptions import UserError


logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    The objective of this hook is to detect the installation
    of the module 'account_invoice_constraint_chronology' on an
    existing Odoo instance.
    """

    env = api.Environment(cr, SUPERUSER_ID, {})
    installed_module = env['ir.module.module'].search([
        ('name', '=', 'l10n_it_intrastat_statement')
    ])
    if installed_module and installed_module.state == 'installed':
        raise UserError('Questo modulo non è installabile poichè è '
                        'presente un\'altra versione simile '
                        '(l10n_it_intrastat_statement).')
