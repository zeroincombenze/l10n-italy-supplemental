#
# Copyright 2016-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from datetime import date, datetime

from odoo import models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class MultireportMixin(models.AbstractModel):
    _name = "multireport.mixin"
    _description = "Multireport common functions"

    def code_2_print(self, style_mode=None):
        if not style_mode:
            style_mode = self.company_id.report_model_style.description_mode
        return (
            self.product_id.default_code
            if self.product_id and style_mode == "print"
            else ""
        )

    def description_2_print(self, style_mode=None):
        if not style_mode:
            style_mode = self.company_id.report_model_style.description_mode
        value = self.name
        if style_mode in ("line1", "nocode1"):
            value = value.split("\n")[0]
        if style_mode in ("nocode", "nocode1"):
            i = value.find("]")
            if value[0] == "[" and i >= 0:
                value = value[i + 1 :].lstrip()
        return value

    def _fmt_date_macro(self, value, date_format):
        """Format a date/datetime value read from a Date/Datetime field
        for use in one of the `%(...)s`-style report macros below.

        The ORM returns real `date`/`datetime` objects (not strings) for
        such fields; kept tolerant of a plain string too (in the
        `DEFAULT_SERVER_DATETIME_FORMAT` shape the pre-13.0 code assumed)
        in case a caller passes one through some other path.
        """
        if not value:
            return ""
        if isinstance(value, (date, datetime)):
            return value.strftime(date_format)
        return datetime.strptime(value, DEFAULT_SERVER_DATETIME_FORMAT).strftime(
            date_format
        )
