# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#

import ribalta

from . import models
from . import wizard

REQUIRED_RIBALTA_VERSION = '0.4'

if not ribalta.__version__.startswith(REQUIRED_RIBALTA_VERSION):
    raise RuntimeError(
        f'Module "account_banking_riba" requires '
        f'ribalta library version {REQUIRED_RIBALTA_VERSION}.x, '
        f'detected version is {ribalta.__version__}'
    )
