# -*- coding: utf-8 -*-
#
# Copyright 2018-20 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
import os
# from datetime import datetime

import requests

from odoo import _, api, fields, models

from odoo.addons.l10n_it_einvoice_send2sdi.models.attachment import Evolve


class ItalyAdeSender(models.Model):
    _inherit = "italy.ade.sender"

    def _compute_available(self):
        for chn in self:
            chn.avail_invoices_ctr = (
                chn.max_invoices_ctr
                - chn.used_invoices_ctr
                - chn.bonus_invoices_ctr
                - 10
            )
            # if (
            #     chn.avail_invoices_ctr < 0
            #     and datetime.today() < datetime(2022, 6, 26)
            #     and chn.bonus_invoices_ctr == 0
            # ):
            #     chn.bonus_invoices_ctr = 5 - chn.avail_invoices_ctr
            #     chn.avail_invoices_ctr = (
            #         chn.max_invoices_ctr
            #         - chn.used_invoices_ctr
            #         - chn.bonus_invoices_ctr
            #         - 10
            #     )
        if chn.avail_invoices_ctr <= 0:                                          # noqa
            chn.avail_message = _(
                "You cannot send invoices. Please buy a new invoices pack!"
            )                                                                    # noqa
        elif chn.avail_invoices_ctr <= 20:                                       # noqa
            chn.avail_message = _("Not many invoices!")                          # noqa
        else:
            chn.avail_message = ""

    max_invoices_ctr = fields.Integer(
        string="Max invoices",
        readonly=True,
        help="Total # of invoices to send or receive",
    )
    used_invoices_ctr = fields.Integer(
        string="Sent/Received invoices",
        readonly=True,
        help="Total # of invoices sent and received",
    )
    bonus_invoices_ctr = fields.Integer(
        string="# of bonus invoices",
        readonly=True,
        help="Total # of bonus invoices",
    )
    avail_invoices_ctr = fields.Integer(
        string="# of invoices available",
        readonly=True,
        compute="_compute_available",
        help="Total # of invoices you can still send or receive",
    )
    avail_message = fields.Char(
        string="Availability message",
        readonly=True,
        compute="_compute_available",
    )

    @api.multi
    def count_xml_invoice(self):
        for channel in self:
            if not channel.sender_url:
                channel.used_invoices_ctr = 0
                channel._compute_available()
                return
            headers = Evolve.header(channel)
            url = os.path.join(channel.sender_url, "Cerca")
            chn_inv_in = int(channel.param2) if channel.param2 else 2
            chn_inv_out = int(channel.param1) if channel.param1 else 1

            data = {
                "IdAzienda": int(channel.sender_company_id),
                "IdArchivio": chn_inv_in,
                "Filtri": [],
            }
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(data, ensure_ascii=False)
                )
            except BaseException:
                return
            if not (200 <= response.status_code < 300):
                return
            try:
                documenti = response.json()
                if documenti["EsitoChiamata"] > 0:
                    return
            except BaseException:
                return
            in_invs = len(documenti["Documenti"])

            data = {
                "IdAzienda": int(channel.sender_company_id),
                "IdArchivio": chn_inv_out,
                "Filtri": [],
            }
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(data, ensure_ascii=False)
                )
            except BaseException:
                return
            if not (200 <= response.status_code < 300):
                return
            try:
                documenti = response.json()
                if documenti["EsitoChiamata"] > 0:
                    return
            except BaseException:
                return

            out_invs = len(documenti["Documenti"])
            channel.used_invoices_ctr = in_invs + out_invs
            channel._compute_available()

        return

    def incr_invoice_counter(self):
        for channel in self:
            channel.used_invoices_ctr = channel.used_invoices_ctr + 1
            channel._compute_available()
