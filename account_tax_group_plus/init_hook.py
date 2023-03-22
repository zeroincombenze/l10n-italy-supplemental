# Copyright 2020-21 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-21 Didotech s.r.l. <https://www.didotech.com>
#
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#
import logging
from odoo import api, SUPERUSER_ID


logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """
    The objective of this hook is to update account tax group new field
    with the default value.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    country_ita = env['res.country'].search([('code', '=', 'IT')])

    company_country_id = country_ita.id

    logger.info("Company ID Country {id}".format(id=company_country_id))

    if company_country_id:
        logger.info("Update tax groups")
        taxes_group = env['account.tax.group'].search([])
        for record in taxes_group:
            record.write({
                'country_id': company_country_id,
            })
        # end for
# end post_init_hook

