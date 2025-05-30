#
# Copyright 2018-25 - SHS-AV s.r.l. <https://www.zeroincombenze.it/>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# import json
# import os

# from datetime import datetime

# import requests

from odoo import _, api, fields, models

# from odoo.addons.l10n_it_einvoice_evolve.models.attachment import Evolve


class SdiChannel(models.Model):
    _inherit = "sdi.channel"

    channel_type = fields.Selection(
        selection_add=[
            ("evolve", "Import by Evolve"),
        ])

    client_id = fields.Char("Client ID", help="Client ID assigned by Evolve")
    client_key = fields.Char(
        "Client key", help="Client key assigned by Evolve"
    )
    sender_url = fields.Char("Sender url", help="Evolve URL to connect")
    sender_company_id = fields.Char(
        "Company ID", help="Company Identification assigned by Evolve"
    )
    hub_ip_addr = fields.Char("Hub IP Address", help="IP Address to connect")
    active = fields.Boolean(string="Active", default=True)
    param1 = fields.Char(
        string="Custom value 1",
        help="Out invoices storage id, usually 1",
    )
    param2 = fields.Char(
        string="Custom value 2",
        help="In invoices storage id, usually 2",
    )
    param3 = fields.Char(
        string="Custom value 3",
        help="Sent invoices storage id, usually 3",
    )
    param4 = fields.Char(
        string="Custom value 4",
        help="# of prior days to read to update invoice state",
    )
    param5 = fields.Char(
        string="Custom value 5",
        help="Custom value to issue for communication, if required",
    )
    param6 = fields.Char(
        string="Custom value 6",
        help="Custom value to issue for communication, if required",
    )

    def _compute_available(self):
        for chn in self:
            chn.avail_invoices_ctr = (
                chn.max_invoices_ctr
                - chn.used_invoices_ctr
                - chn.bonus_invoices_ctr
                - 10
            )
        if chn.avail_invoices_ctr <= 0:  # noqa
            chn.avail_message = _(
                "You cannot send invoices. Please buy a new invoices pack!"
            )  # noqa
        elif chn.avail_invoices_ctr <= 20:  # noqa
            chn.avail_message = _("Not many invoices!")  # noqa
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
    #         headers = Evolve.header(channel)
    #         url = os.path.join(channel.sender_url, "Cerca")
    #         chn_inv_in = int(channel.param2) if channel.param2 else 2
    #         chn_inv_out = int(channel.param1) if channel.param1 else 1
    #
    #         data = {
    #             "IdAzienda": int(channel.sender_company_id),
    #             "IdArchivio": chn_inv_in,
    #             "Filtri": [],
    #         }
    #         try:
    #             response = requests.post(
    #                 url, headers=headers, data=json.dumps(data, ensure_ascii=False)
    #             )
    #         except BaseException:
    #             return
    #         if not (200 <= response.status_code < 300):
    #             return
    #         try:
    #             documenti = response.json()
    #             if documenti["EsitoChiamata"] > 0:
    #                 return
    #         except BaseException:
    #             return
    #         in_invs = len(documenti["Documenti"])
    #
    #         data = {
    #             "IdAzienda": int(channel.sender_company_id),
    #             "IdArchivio": chn_inv_out,
    #             "Filtri": [],
    #         }
    #         try:
    #             response = requests.post(
    #                 url, headers=headers, data=json.dumps(data, ensure_ascii=False)
    #             )
    #         except BaseException:
    #             return
    #         if not (200 <= response.status_code < 300):
    #             return
    #         try:
    #             documenti = response.json()
    #             if documenti["EsitoChiamata"] > 0:
    #                 return
    #         except BaseException:
    #             return
    #
    #         out_invs = len(documenti["Documenti"])
    #         channel.used_invoices_ctr = in_invs + out_invs
    #         channel._compute_available()
    #
    #     return
    #
    # def incr_invoice_counter(self):
    #     for channel in self:
    #         channel.used_invoices_ctr = channel.used_invoices_ctr + 1
    #         channel._compute_available()

    def send_viaevolve(attachment_out_ids):
        pass
