import logging
from odoo import api, SUPERUSER_ID
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    The objective of this hook is to detect the installation
    of the module 'l10n_it_split_payment' on an
    existing Odoo instance.
    """

    env = api.Environment(cr, SUPERUSER_ID, {})

    # incompatibility check
    parameter = env['ir.config_parameter'].search(
        [('key', '=', 'disable_oca_incompatibility')]
    )

    if not parameter or not eval(parameter.value):
        installed_module = env['ir.module.module'].search(
            [('name', '=', 'l10n_it_split_payment')]
        )
        if (
            installed_module
            and installed_module.maintainer.lower()
            != 'powerp enterprise network'
        ):
            raise UserError(
                'Questo modulo non è installabile poichè è '
                'presente un\'altra versione di '
                '(l10n_it_split_payment).'
            )
        # end if
    # end if
