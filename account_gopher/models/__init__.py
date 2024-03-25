# -*- coding: utf-8 -*-
#
# Copyright 2020-24 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from . import account_tax
from . import account_account

try:
    from . import account_rc_type
except ImportError:
    pass
from . import account_fiscal_position
