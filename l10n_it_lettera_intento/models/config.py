# -*- coding: utf-8 -*-
#
# Copyright 2019-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#

from odoo import fields, models

HELP = (
    "Testo da inserire in fattura; può essere completato con:\n"
    "%(ns.prot)s Protocollo interno\n"
    "%(ns.data)s Data interna\n"
    "%(vs.prot)s Protocollo cliente\n"
    "%(vs.data)s Data cliente\n"
    "%(aut.min)s Autorizzazione ministeriale\n"
)
DEFAULT = (
    "Operazione senza IVA Vs. lettera d'intento n. %(aut.min)s "
    "del %(vs.data)s, ns. prot. %(ns.prot)s del %(ns.data)s."
)


class ResCompany(models.Model):
    _inherit = "res.company"
    text_lettera_intento = fields.Char(
        "Note lettera intento", help=HELP, default=DEFAULT
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = "account.config.settings"

    text_lettera_intento = fields.Char(
        related="company_id.text_lettera_intento",
        string="Note lettera intento",
        help=HELP,
        default=DEFAULT,
    )
