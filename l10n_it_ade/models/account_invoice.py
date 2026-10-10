# -*- coding: utf-8 -*-
#
# Copyright 2018-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
import logging
from xml.sax.saxutils import escape

from odoo import fields, models

_logger = logging.getLogger(__name__)

try:
    from unidecode import unidecode
except ImportError as err:                                           # pragma: no cover
    _logger.debug(err)


XML_ESCAPE = {
    # u'\'': u' ',
    "\n": " ",
    "\r": " ",
    "\t": " ",
    "€": "EUR",
    "©": "(C)",
    "®": "(R)",
    "«": '"',
    "»": '"',
    "Ø": "&Oslash;",
    "ø": "&oslash;",
    "ß": "ss",
    "\u2019": "'",
}


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fiscal_document_type_id = fields.Many2one(
        "italy.ade.invoice.type",
        string="Fiscal Document Type",
        oldname="invoice_type_id",
        copy=False,
        help="Tag 2.1.1.1 <TipoDocumento>\n"
             "Tipo documento fiscale."
    )

    def wep_text(self, text):
        """ "Do xml escape to avoid error StringLatinType"""
        return unidecode(escape(text, XML_ESCAPE)).strip() if text else text
