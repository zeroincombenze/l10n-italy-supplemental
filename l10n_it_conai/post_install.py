#
# Copyright 2019-23 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import SUPERUSER_ID, api


def set_company_conai_product(cr):
    """Set the default CONAI product

    Args:
        cr (obj): sql cursor

    Returns:
        None
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        company_model = env["res.company"]
        for company in company_model.search([]):
            company.conai_product_id = env["product.product"].search(
                [("product_tmpl_id", "=", env.ref("l10n_it_conai.product_conai").id)]
            )


def set_company_conai_product_post(cr, registry):
    set_company_conai_product(cr)
