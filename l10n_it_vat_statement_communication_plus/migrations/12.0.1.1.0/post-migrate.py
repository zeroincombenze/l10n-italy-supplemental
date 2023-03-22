# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2017-19 Lorenzo Battistini
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
# Copyright 2017-21 Odoo Community Association (OCA) <https://odoo-community.org>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        _logger.warning("""
            There is no previous version of the module.
            Skip the migration.
            """)

        return

    _logger.info("Set the default value on the new company field.")
    cr.execute("""
        UPDATE res_company
        SET vsc_supply_code = 'IVP18';
    """)

    _logger.info("Migration terminated.")
