# -*- coding: utf-8 -*-
#
# Copyright 2018-24 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        fiscalposition = env["account.fiscal.position"]
        for fpos in fiscalposition.search([]):
            if fpos.rc_type_id:
                fpos.rc_fiscal_document_type_id = (
                    fpos.rc_type_id.fiscal_document_type_id.id)
