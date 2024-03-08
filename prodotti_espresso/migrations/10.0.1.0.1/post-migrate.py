# -*- coding: utf-8 -*-
#
# Copyright 2022 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        product_template_model = env["product.template"]
        product_product_model = env["product.product"]
        deliver_carrier_model = env["delivery.carrier"]
        recs = product_template_model.search([("default_code", "=", "SHIP")])
        product_template = recs[0] if recs else False
        recs = product_product_model.search([("default_code", "=", "SHIP")])
        product_product = recs[0] if recs else False
        recs = deliver_carrier_model.search([("name", "=", product_template.name)])
        carrier = recs[0] if recs else False
        if not carrier:
            vals = {
                'name': product_template.name,
            }
            carrier = deliver_carrier_model.create(vals)
        vals = {
            'delivery_type': 'fixed',
            'fixed_price': 4.9,
            'free_if_more_than': True,
            'amount': 50.0,
        }
        if product_template:
            vals['product_tmpl_id'] = product_template.id
        if product_product:
            vals['product_id'] = product_product.id
        if vals:
            carrier.write(vals)
