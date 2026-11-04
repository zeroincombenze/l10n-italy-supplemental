# -*- coding: utf-8 -*-
#
# Copyright 2018-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
from odoo import SUPERUSER_ID, api

from .models.res_company import ODOO_FOOTER, Z0_FOOTER


def _replace_footer(cr, old, new):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for company in env["res.company"].search([]):
        if company.rml_header and old in company.rml_header:
            company.rml_header = company.rml_header.replace(old, new)


def post_init_hook(cr, registry):
    _replace_footer(cr, ODOO_FOOTER, Z0_FOOTER)


def uninstall_hook(cr, registry):
    _replace_footer(cr, Z0_FOOTER, ODOO_FOOTER)
