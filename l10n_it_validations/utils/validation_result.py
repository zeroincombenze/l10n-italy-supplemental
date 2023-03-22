# Copyright 2020-22 LibrERP enterprise network <https://www.librerp.it>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
import logging

from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ValidationResult:
    def __init__(self, passed: bool = True, msg: str = None, title: str = None):

        self._passed = passed
        self._msg = msg
        self._title = title

        # Parameters validation
        if self.passed and (self.msg or self.title):
            raise ValueError(
                'If validation passed the "msg" and "title" parameters'
                "should not be left None since they will never be displayed"
            )
        # end if

        if self.failed and not self._msg:
            raise ValueError(
                "If validation failed ValidationError must be"
                "initialized with the error message"
            )
        # end if

    # end init

    @property
    def title(self):
        return self._title

    # end title

    @property
    def msg(self):
        return self._msg

    # end title

    @property
    def passed(self):
        return self._passed

    # end title

    @property
    def failed(self):
        return not self._passed

    # end title

    def on_err_warn(self):
        """
        :return: a dict with a warning message to be used in onchange
        methods for showing errors. If no error returns an empty dict.
        """

        if self.failed:
            return {
                "warning": {
                    "title": self.title,
                    "message": self.msg,
                }
            }
        else:
            return {}
        # end if

    # end get_waring

    def raise_user_error(self):
        if self.failed:
            raise UserError(self.msg)
        # end if

    # end raise_validation_error

    def raise_validation_error(self):
        if self.failed:
            raise ValidationError(self.msg)
        # end if

    # end raise_validation_error

    def on_err_raise(self):
        self.raise_user_error()

    # end raise_validation_error
