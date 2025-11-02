# -*- coding: utf-8 -*-
import logging

from odoo import SUPERUSER_ID, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

THIS_MODULE = "l10n_it_einvoice_base"
MODULE_TO_CHECK = "account_invoice_partner_carrier"


def check_installed_plus(cr):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        ir_module = env["ir.module.module"]
        if not ir_module.search([("name", "=", MODULE_TO_CHECK),
                                 ("state", "=", ("installed", "to upgrade"))]):
            raise UserError(
                "Please, install module %s before upgrade module %s!"
                % (MODULE_TO_CHECK, THIS_MODULE))


def migrate(cr, version):
    if not version:
        return
    check_installed_plus(cr)
