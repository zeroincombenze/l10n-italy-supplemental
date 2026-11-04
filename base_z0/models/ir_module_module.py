# -*- coding: utf-8 -*-
#
# Copyright 2018-26 Zeroincombenze srls <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    @api.depends("name", "description")
    def _get_desc(self):
        # A broken description (bad RST, bad translation) must not break
        # the Apps list: render each module alone and catch its error.
        for module in self:
            try:
                super(IrModuleModule, module)._get_desc()
            except Exception:
                _logger.warning(
                    "Cannot render the description of module %s",
                    module.name,
                    exc_info=True,
                )
                module.description_html = "Error in Description"
