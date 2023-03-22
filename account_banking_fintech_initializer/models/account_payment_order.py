# Copyright 2022 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2022 Didotech s.r.l. <https://www.didotech.com>

import logging
import sys

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

if 'fintech' not in sys.modules:
    try:
        import fintech
        fintech.register()
        _logger.debug('Modulo fintech inizializzato.')
    except ImportError:
        _logger.debug('Cannot `import fintech`.')
