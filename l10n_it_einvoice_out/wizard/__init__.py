# -*- coding: utf-8 -*-
#
# Copyright 2014    - Davide Corio
# Copyright 2015-16 - Lorenzo Battistini - Agile Business Group
# Copyright 2018-19 - Odoo Italia Associazione <https://www.odoo-italia.org>
# Copyright 2018-22 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#

import logging

_logger = logging.getLogger(__name__)

try:
    from . import wizard_export_fatturapa
except ImportError:
    _logger.debug("Cannot `import pyxb`.")  # Avoid init error if not installed

from . import attachment_refresh_info
