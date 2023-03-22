# Copyright 2020-16 Powerp Enterprise Network
# Copyright 2021 powERP enterprise network <https://www.powerp.it>
import logging
import re

logger = logging.getLogger(__name__)


def cuc_code_valid(cuc_code):
    """Check if Codice Univoco CBI is valid
    @param cuc_code: CUC code as string
    @return: True if valid, False otherwise
    """
    if re.match(r'[A-Z0-9]{8}', cuc_code):
        return True
    else:
        return False
    # end if
# end sia_code_valid
