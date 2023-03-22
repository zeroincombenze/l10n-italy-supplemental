# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License LGPL-3 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
#
from odoo import api, SUPERUSER_ID
from odoo.addons.l10n_it_coa_base import migrate_negative_balance
import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return
    migrate_negative_balance(cr)
