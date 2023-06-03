# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#

import logging
import re

logger = logging.getLogger(__name__)


def sia_code_valid(sia_code):
    """Check if SEPA Creditor Identifier is valid
    @param sia_code: SIA code as string
    @return: True if valid, False otherwise
    """
    if re.match(r"[A-Z0-9]{5}", sia_code):
        return True
    else:
        return False
    # end if
